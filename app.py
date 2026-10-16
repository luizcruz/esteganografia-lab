from __future__ import annotations

import contextlib
import importlib
import io
import json
import mimetypes
import subprocess
import sys
import tempfile
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from examples.registry import EXAMPLES

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
HOST = "127.0.0.1"
PORT = 5000

# Runner executado em subprocesso isolado. Bloqueia rede e captura JSON.
_SANDBOX_RUNNER = r"""
import sys, json, io, contextlib, traceback, importlib.util

sys.path.insert(0, __BASE_DIR__)

# Bloqueia qualquer conexão de rede dentro do sandbox
import socket as _sock
class _NoNetwork:
    def __init__(self, *a, **kw):
        raise OSError("Conexões de rede são bloqueadas no sandbox didático")
    def __getattr__(self, n):
        return self
_sock.socket = _NoNetwork

buf = io.StringIO()
try:
    spec = importlib.util.spec_from_file_location("_sandbox_example", __TMP_FILE__)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with contextlib.redirect_stdout(buf):
        payload = mod.run()
    meta = getattr(mod, "META", {})
    out = {"ok": True, "stdout": buf.getvalue(), "meta": meta}
    if isinstance(payload, dict):
        out.update(payload)
    print(json.dumps(out, ensure_ascii=False, default=str))
except Exception as exc:
    print(json.dumps({
        "ok": False,
        "error": str(exc),
        "traceback": traceback.format_exc(limit=8),
        "stdout": buf.getvalue(),
    }, ensure_ascii=False, default=str))
"""


def run_sandboxed(code: str, base_dir: Path) -> dict:
    """Executa código do usuário em subprocesso isolado, sem acesso à rede."""
    tmp: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".py",
            dir=base_dir / "examples",
            prefix="_sandbox_",
            delete=False,
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write(code)
            tmp = Path(f.name)

        runner = (
            _SANDBOX_RUNNER
            .replace("__BASE_DIR__", repr(str(base_dir)))
            .replace("__TMP_FILE__", repr(str(tmp)))
        )

        proc = subprocess.run(
            [sys.executable, "-c", runner],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(base_dir),
        )
        raw = proc.stdout.strip()
        if not raw:
            err = proc.stderr.strip() or "Processo encerrado sem saída"
            return {"ok": False, "error": err, "traceback": proc.stderr, "stdout": ""}
        return json.loads(raw)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Tempo limite excedido (30 segundos)", "stdout": ""}
    except json.JSONDecodeError as exc:
        return {"ok": False, "error": f"Saída inválida do sandbox: {exc}", "stdout": ""}
    finally:
        if tmp and tmp.exists():
            tmp.unlink(missing_ok=True)


def load_entry(example_id: str):
    entry = next((e for e in EXAMPLES if e["id"] == example_id), None)
    if entry is None:
        raise KeyError(example_id)
    module = importlib.import_module(entry["module"])
    module = importlib.reload(module)
    return entry, module


def json_bytes(payload: dict | list) -> bytes:
    return json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    server_version = "EsteganoLab/1.0"

    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {fmt % args}")

    def send_json(self, payload, status=200):
        body = json_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path: Path):
        if not path.exists() or not path.is_file():
            self.send_error(404)
            return
        data = path.read_bytes()
        mime, _ = mimetypes.guess_type(path.name)
        self.send_response(200)
        self.send_header(
            "Content-Type",
            (mime or "application/octet-stream")
            + ("; charset=utf-8" if (mime or "").startswith("text/") or path.suffix in {".js", ".css"} else ""),
        )
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path == "/":
            return self.send_file(STATIC_DIR / "index.html")
        if path == "/health":
            return self.send_json({"ok": True, "examples": len(EXAMPLES)})
        if path == "/api/examples":
            items = []
            for entry in EXAMPLES:
                _, module = load_entry(entry["id"])
                items.append(module.META)
            return self.send_json(items)
        if path.startswith("/api/examples/") and path.endswith("/code"):
            example_id = path[len("/api/examples/"):-len("/code")].strip("/")
            try:
                entry, _ = load_entry(example_id)
            except KeyError:
                return self.send_json({"error": "Exemplo não encontrado"}, 404)
            file_path = BASE_DIR / (entry["module"].replace(".", "/") + ".py")
            return self.send_json({"id": example_id, "code": file_path.read_text(encoding="utf-8")})

        # Arquivos estáticos. Bloqueia travessia de diretório.
        relative = path.lstrip("/")
        candidate = (STATIC_DIR / relative).resolve()
        try:
            candidate.relative_to(STATIC_DIR.resolve())
        except ValueError:
            return self.send_error(403)
        return self.send_file(candidate)

    def do_POST(self):
        path = unquote(urlparse(self.path).path)
        if path.startswith("/api/examples/") and path.endswith("/run"):
            example_id = path[len("/api/examples/"):-len("/run")].strip("/")
            try:
                entry, module = load_entry(example_id)
            except KeyError:
                return self.send_json({"error": "Exemplo não encontrado"}, 404)

            # Lê o código enviado pelo frontend (original ou editado pelo usuário)
            user_code = ""
            length = int(self.headers.get("Content-Length", 0) or 0)
            if length > 0:
                try:
                    body = json.loads(self.rfile.read(length))
                    user_code = body.get("code", "")
                except Exception:
                    pass

            # Fallback: usa o arquivo original se nenhum código foi enviado
            if not user_code:
                file_path = BASE_DIR / (entry["module"].replace(".", "/") + ".py")
                user_code = file_path.read_text(encoding="utf-8")

            data = run_sandboxed(user_code, BASE_DIR)
            # Sempre usa o META do módulo original para evitar adulteração
            data["meta"] = getattr(module, "META", {"id": example_id})
            status = 200 if data.get("ok") else 500
            return self.send_json(data, status)

        self.send_error(404)


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print("=" * 60)
    print("EsteganoLab iniciado")
    print(f"Abra no navegador: http://{HOST}:{PORT}")
    print("Pressione Ctrl+C para encerrar.")
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrando...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
