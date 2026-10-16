const state = {
  examples: [],
  current: null,
  completed: new Set(JSON.parse(localStorage.getItem('esteganoLabCompleted') || '[]')),
  filter: '',
  editing: false,
  originalCode: '',
};

const els = {
  nav:          document.getElementById('example-nav'),
  search:       document.getElementById('search'),
  title:        document.getElementById('example-title'),
  summary:      document.getElementById('example-summary'),
  chapter:      document.getElementById('chapter-label'),
  refs:         document.getElementById('reference-badges'),
  codeEditor:   document.getElementById('code-editor'),
  codePanelTitle: document.getElementById('code-panel-title'),
  run:          document.getElementById('run-btn'),
  edit:         document.getElementById('edit-btn'),
  reset:        document.getElementById('reset-btn'),
  copy:         document.getElementById('copy-btn'),
  result:       document.getElementById('result-view'),
  status:       document.getElementById('run-status'),
  progressText: document.getElementById('progress-text'),
  progressFill: document.getElementById('progress-fill'),
  explainBox:   document.getElementById('explanation-box'),
  explainChapter: document.getElementById('explain-chapter'),
  explainTitle:   document.getElementById('explain-title'),
  explainSummary: document.getElementById('explain-summary'),
  explainAlgorithm: document.getElementById('explain-algorithm'),
};

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

function updateProgress() {
  const total = state.examples.length || 1;
  const done = [...state.completed].filter(id => state.examples.some(e => e.id === id)).length;
  els.progressText.textContent = `${done} / ${state.examples.length} executados`;
  els.progressFill.style.width = `${(done / total) * 100}%`;
}

function groupExamples() {
  const q = state.filter.trim().toLowerCase();
  const visible = state.examples.filter(
    e => !q || `${e.id} ${e.title} ${e.chapter} ${e.summary}`.toLowerCase().includes(q)
  );
  const groups = new Map();
  visible.forEach(e => {
    if (!groups.has(e.chapter)) groups.set(e.chapter, []);
    groups.get(e.chapter).push(e);
  });
  return groups;
}

function renderNav() {
  els.nav.innerHTML = '';
  const groups = groupExamples();
  for (const [chapter, examples] of groups.entries()) {
    const wrap = document.createElement('div');
    wrap.className = 'chapter-group';
    const heading = document.createElement('div');
    heading.className = 'chapter-title';
    heading.textContent = chapter;
    wrap.appendChild(heading);
    examples.forEach(example => {
      const btn = document.createElement('button');
      btn.className = 'example-item';
      if (state.current?.id === example.id) btn.classList.add('active');
      if (state.completed.has(example.id)) btn.classList.add('done');
      btn.innerHTML = `<span class="example-id">${escapeHtml(example.id)}</span><span class="example-name">${escapeHtml(example.title)}</span>`;
      btn.addEventListener('click', () => selectExample(example));
      wrap.appendChild(btn);
    });
    els.nav.appendChild(wrap);
  }
  if (!groups.size) {
    els.nav.innerHTML = '<div class="chapter-title">Nenhum exemplo encontrado</div>';
  }
}

function exitEditMode() {
  state.editing = false;
  els.codeEditor.readOnly = true;
  els.codeEditor.classList.remove('editing');
  els.edit.textContent = 'Editar';
  els.reset.hidden = true;
  els.codePanelTitle.textContent = 'Código';
}

async function selectExample(example) {
  state.current = example;
  exitEditMode();
  els.title.textContent = `${example.id} — ${example.title}`;
  els.summary.textContent = example.summary;
  els.chapter.textContent = example.chapter;
  els.refs.innerHTML = (example.references || []).map(r => `<span class="ref-badge">[${r}]</span>`).join('');

  // Popula o box de explicação para leigos
  els.explainChapter.textContent = example.chapter;
  els.explainTitle.textContent = `${example.id} — ${example.title}`;
  els.explainSummary.textContent = example.summary;
  els.explainAlgorithm.textContent = example.algorithm || '';
  els.explainBox.removeAttribute('hidden');

  els.run.disabled = true;
  els.edit.disabled = true;
  els.status.className = 'run-status idle';
  els.status.textContent = 'Aguardando';
  els.result.className = 'result-view empty-state';
  els.result.innerHTML = '<div class="empty-icon">▶</div><h4>Pronto para executar</h4><p>Leia o código, faça sua previsão e pressione Executar.</p>';
  renderNav();

  try {
    const res = await fetch(`/api/examples/${encodeURIComponent(example.id)}/code`);
    const data = await res.json();
    state.originalCode = data.code;
    els.codeEditor.value = data.code;
    els.run.disabled = false;
    els.edit.disabled = false;
  } catch (err) {
    els.codeEditor.value = `# Erro ao carregar código: ${err}`;
  }
}

function renderValue(step) {
  if (!('value' in step)) return '';
  if (step.kind === 'image') {
    // Só aceita data URLs de imagem para evitar XSS
    const src = String(step.value);
    if (!src.startsWith('data:image/')) return '';
    const img = document.createElement('img');
    img.className = 'step-image';
    img.alt = 'Saída do exemplo';
    img.src = src;
    return img.outerHTML;
  }
  if (step.kind === 'table' && Array.isArray(step.value)) {
    return `<table class="step-table"><tbody>${
      step.value.map(row => `<tr>${row.map(cell => `<td>${escapeHtml(cell)}</td>`).join('')}</tr>`).join('')
    }</tbody></table>`;
  }
  const text = typeof step.value === 'string' ? step.value : JSON.stringify(step.value, null, 2);
  return `<pre class="step-value">${escapeHtml(text)}</pre>`;
}

function stepCard(step, index) {
  const el = document.createElement('div');
  el.className = 'step-card';
  el.innerHTML = `
    <div class="step-head">
      <div class="step-number">${index + 1}</div>
      <div class="step-title">${escapeHtml(step.title)}</div>
    </div>
    <div class="step-explanation">${escapeHtml(step.explanation || '')}</div>
    ${renderValue(step)}
  `;
  return el;
}

async function runCurrent() {
  if (!state.current) return;
  els.run.disabled = true;
  els.status.className = 'run-status running';
  els.status.textContent = 'Executando…';
  els.result.className = 'result-view';
  els.result.innerHTML = '';
  try {
    // Sempre envia o código atual (original ou editado) para execução no sandbox
    const res = await fetch(`/api/examples/${encodeURIComponent(state.current.id)}/run`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({code: els.codeEditor.value}),
    });
    const data = await res.json();
    if (!res.ok || !data.ok) throw data;

    for (let i = 0; i < (data.steps || []).length; i++) {
      els.result.appendChild(stepCard(data.steps[i], i));
      await new Promise(resolve => setTimeout(resolve, 180));
      els.result.scrollTop = els.result.scrollHeight;
    }
    if (data.final) {
      const final = document.createElement('div');
      final.className = 'final-box';
      final.innerHTML = `<strong>Resultado final</strong><br>${escapeHtml(data.final)}`;
      els.result.appendChild(final);
    }
    if (data.note) {
      const note = document.createElement('div');
      note.className = 'note-box';
      note.innerHTML = `<strong>Observação</strong><br>${escapeHtml(data.note)}`;
      els.result.appendChild(note);
    }
    if (data.stdout) {
      const stdout = document.createElement('pre');
      stdout.className = 'stdout-box';
      stdout.textContent = data.stdout;
      els.result.appendChild(stdout);
    }
    els.status.className = 'run-status ok';
    els.status.textContent = 'Concluído';
    state.completed.add(state.current.id);
    localStorage.setItem('esteganoLabCompleted', JSON.stringify([...state.completed]));
    updateProgress();
    renderNav();
  } catch (err) {
    els.status.className = 'run-status error';
    els.status.textContent = 'Erro';
    els.result.innerHTML = `<div class="error-box">${escapeHtml(err.traceback || err.error || String(err))}</div>`;
  } finally {
    els.run.disabled = false;
  }
}

// Botão Executar
els.run.addEventListener('click', runCurrent);

// Botão Copiar
els.copy.addEventListener('click', async () => {
  const code = els.codeEditor.value;
  if (!code) return;
  await navigator.clipboard.writeText(code);
  const old = els.copy.textContent;
  els.copy.textContent = 'Copiado';
  setTimeout(() => els.copy.textContent = old, 900);
});

// Botão Editar / Visualizar
els.edit.addEventListener('click', () => {
  state.editing = !state.editing;
  els.codeEditor.readOnly = !state.editing;
  els.codeEditor.classList.toggle('editing', state.editing);
  els.edit.textContent = state.editing ? 'Visualizar' : 'Editar';
  els.reset.hidden = !state.editing;
  els.codePanelTitle.textContent = state.editing ? 'Código (editando)' : 'Código';
  if (state.editing) els.codeEditor.focus();
});

// Botão Restaurar
els.reset.addEventListener('click', () => {
  els.codeEditor.value = state.originalCode;
  exitEditMode();
});

// Tab insere 4 espaços em vez de pular o foco
els.codeEditor.addEventListener('keydown', e => {
  if (e.key === 'Tab' && !els.codeEditor.readOnly) {
    e.preventDefault();
    const s = els.codeEditor.selectionStart;
    const end = els.codeEditor.selectionEnd;
    els.codeEditor.value =
      els.codeEditor.value.substring(0, s) + '    ' + els.codeEditor.value.substring(end);
    els.codeEditor.selectionStart = els.codeEditor.selectionEnd = s + 4;
  }
});

// Busca na lista lateral
els.search.addEventListener('input', e => {
  state.filter = e.target.value;
  renderNav();
});

async function boot() {
  const res = await fetch('/api/examples');
  state.examples = await res.json();
  renderNav();
  updateProgress();
  if (state.examples.length) selectExample(state.examples[0]);
}

boot().catch(err => {
  els.result.innerHTML = `<div class="error-box">Falha ao iniciar: ${escapeHtml(String(err))}</div>`;
});
