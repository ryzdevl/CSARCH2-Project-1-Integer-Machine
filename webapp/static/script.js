// ---------------------------------------------------------------------------
// Tab navigation
// ---------------------------------------------------------------------------

document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.panel-view').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.target).classList.add('active');
  });
});

// ---------------------------------------------------------------------------
// Binary/decimal input-mode toggles
// ---------------------------------------------------------------------------

function wireToggle(switchId, labelId) {
  const el = document.getElementById(switchId);
  const label = document.getElementById(labelId);
  el.addEventListener('click', () => {
    el.classList.toggle('on');
    const isOn = el.classList.contains('on');
    label.textContent = isOn
      ? 'Input mode: Binary (click to switch to decimal)'
      : 'Input mode: Decimal (click to switch to binary)';
  });
}
wireToggle('mul-toggle', 'mul-toggle-label');
wireToggle('div-toggle', 'div-toggle-label');

// ---------------------------------------------------------------------------
// Bit-size preset buttons (4 / 8 / 16 / 32 / 64) beside each bits field
// ---------------------------------------------------------------------------

function wireBitsPresets(groupEl) {
  const targetId = groupEl.dataset.target;
  const input = document.getElementById(targetId);
  const buttons = groupEl.querySelectorAll('.preset-btn');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      input.value = btn.dataset.val;
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });

  // Typing a custom value clears the preset highlight unless it matches one
  input.addEventListener('input', () => {
    buttons.forEach(b => b.classList.toggle('active', b.dataset.val === input.value));
  });
}

document.querySelectorAll('.bits-presets').forEach(wireBitsPresets);

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

function renderBitCells(containerId, bitString) {
  const container = document.getElementById(containerId);
  container.innerHTML = '';
  if (!bitString) return;
  for (const bit of bitString) {
    const cell = document.createElement('div');
    cell.className = 'bit-cell' + (bit === '1' ? ' lit' : '');
    cell.textContent = bit;
    container.appendChild(cell);
  }
}

function showError(elId, message) {
  const el = document.getElementById(elId);
  el.textContent = message;
  el.classList.add('show');
}

function hideError(elId) {
  const el = document.getElementById(elId);
  el.textContent = '';
  el.classList.remove('show');
}

async function postJSON(url, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || 'Something went wrong.');
  }
  return data;
}

// ---------------------------------------------------------------------------
// CONVERSION
// ---------------------------------------------------------------------------

document.getElementById('conv-run').addEventListener('click', async () => {
  hideError('conv-error');
  document.getElementById('conv-results').style.display = 'none';

  const decimal = document.getElementById('conv-decimal').value.trim();
  const bits = document.getElementById('conv-bits').value.trim();

  if (decimal === '' || bits === '') {
    showError('conv-error', 'Please enter both a decimal value and a bit size.');
    return;
  }

  try {
    const data = await postJSON('/api/convert', { decimal, bits });

    document.getElementById('conv-results').style.display = 'block';

    const unsignedCells = document.getElementById('conv-unsigned-cells');
    const unsignedSummary = document.getElementById('conv-unsigned-summary');
    if (data.unsigned_error) {
      unsignedCells.innerHTML = '';
      const span = document.createElement('span');
      span.className = 'error-msg show';
      span.style.marginTop = '0';
      span.textContent = data.unsigned_error;
      unsignedCells.appendChild(span);
      unsignedSummary.textContent = '';
    } else {
      renderBitCells('conv-unsigned-cells', data.unsigned_binary);
      unsignedSummary.textContent =
        `${data.decimal} = ${data.unsigned_binary} (${data.bits}-bit unsigned)`;
    }

    const signedCells = document.getElementById('conv-signed-cells');
    const signedSummary = document.getElementById('conv-signed-summary');
    if (data.signed_error) {
      signedCells.innerHTML = '';
      const span = document.createElement('span');
      span.className = 'error-msg show';
      span.style.marginTop = '0';
      span.textContent = data.signed_error;
      signedCells.appendChild(span);
      signedSummary.textContent = '';
    } else {
      renderBitCells('conv-signed-cells', data.signed_binary);
      signedSummary.textContent =
        `${data.decimal} = ${data.signed_binary} (${data.bits}-bit signed, two's complement)`;
    }
  } catch (err) {
    showError('conv-error', err.message);
  }
});

// ---------------------------------------------------------------------------
// Generic trace-stepper factory (shared by Multiply and Divide)
// ---------------------------------------------------------------------------

function makeStepper(config) {
  // config: { trace, registerKeys: [{key, cellsId}], tableBodyEl, stepLabelId, stepOpId, prevBtnId, nextBtnId }
  let index = 0;
  const stepLabel = document.getElementById(config.stepLabelId);
  const stepOp = document.getElementById(config.stepOpId);
  const prevBtn = document.getElementById(config.prevBtnId);
  const nextBtn = document.getElementById(config.nextBtnId);

  function render() {
    const row = config.trace[index];
    config.registerKeys.forEach(rk => {
      let val = row[rk.key];
      if (rk.key === 'E' || rk.key === 'Q-1') {
        val = String(val); // single bit, 0 or 1
      }
      renderBitCells(rk.cellsId, val);
    });
    stepLabel.textContent = `Step ${index + 1} / ${config.trace.length}`;
    stepOp.textContent = `${row.step !== undefined ? '#' + row.step + ' — ' : ''}${row.operation}`;
    prevBtn.disabled = index === 0;
    nextBtn.disabled = index === config.trace.length - 1;

    // highlight current row in the trace table
    const rows = config.tableBodyEl.querySelectorAll('tr');
    rows.forEach((r, i) => r.classList.toggle('current-step', i === index));
    if (rows[index]) {
      rows[index].scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  prevBtn.onclick = () => { if (index > 0) { index--; render(); } };
  nextBtn.onclick = () => { if (index < config.trace.length - 1) { index++; render(); } };

  render();
}

function populateTraceTable(tbody, trace, columns) {
  tbody.innerHTML = '';
  trace.forEach(row => {
    const tr = document.createElement('tr');
    columns.forEach(col => {
      const td = document.createElement('td');
      td.textContent = row[col];
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
}

// ---------------------------------------------------------------------------
// MULTIPLICATION (Sequential Circuit Binary Multiplier)
// ---------------------------------------------------------------------------

document.getElementById('mul-run').addEventListener('click', async () => {
  hideError('mul-error');
  document.getElementById('mul-results').style.display = 'none';

  const binaryMode = document.getElementById('mul-toggle').classList.contains('on');
  const multiplicand = document.getElementById('mul-a').value.trim();
  const multiplier = document.getElementById('mul-b').value.trim();
  const bits = document.getElementById('mul-bits').value.trim();

  if (multiplicand === '' || multiplier === '' || bits === '') {
    showError('mul-error', 'Please fill in both operands and the bit size.');
    return;
  }

  try {
    const data = await postJSON('/api/multiply', {
      multiplicand, multiplier, bits, binary_input: binaryMode
    });

    document.getElementById('mul-results').style.display = 'block';
    document.getElementById('mul-product-bin').textContent = data.product_binary;
    document.getElementById('mul-product-dec').textContent = data.product_decimal;
    document.getElementById('mul-sign').textContent = data.result_negative ? 'Negative (−)' : 'Positive (+)';

    const tbody = document.querySelector('#mul-trace-table tbody');
    populateTraceTable(tbody, data.trace, ['step', 'operation', 'A', 'Q', 'Q-1']);

    makeStepper({
      trace: data.trace,
      registerKeys: [
        { key: 'A', cellsId: 'mul-a-cells' },
        { key: 'Q', cellsId: 'mul-q-cells' },
        { key: 'Q-1', cellsId: 'mul-q1-cells' }
      ],
      tableBodyEl: tbody,
      stepLabelId: 'mul-step-label',
      stepOpId: 'mul-step-op',
      prevBtnId: 'mul-prev',
      nextBtnId: 'mul-next'
    });
  } catch (err) {
    showError('mul-error', err.message);
  }
});

// ---------------------------------------------------------------------------
// DIVISION (Non-Restoring Division)
// ---------------------------------------------------------------------------

document.getElementById('div-run').addEventListener('click', async () => {
  hideError('div-error');
  document.getElementById('div-results').style.display = 'none';

  const binaryMode = document.getElementById('div-toggle').classList.contains('on');
  const dividend = document.getElementById('div-a').value.trim();
  const divisor = document.getElementById('div-b').value.trim();
  const bits = document.getElementById('div-bits').value.trim();

  if (dividend === '' || divisor === '' || bits === '') {
    showError('div-error', 'Please fill in both operands and the bit size.');
    return;
  }

  try {
    const data = await postJSON('/api/divide', {
      dividend, divisor, bits, binary_input: binaryMode
    });

    document.getElementById('div-results').style.display = 'block';
    document.getElementById('div-quotient').textContent =
      `${data.quotient_binary} (${data.quotient_decimal})`;
    document.getElementById('div-remainder').textContent =
      `${data.remainder_binary} (${data.remainder_decimal})`;

    const tbody = document.querySelector('#div-trace-table tbody');
    populateTraceTable(tbody, data.trace, ['step', 'operation', 'A', 'Q']);

    makeStepper({
      trace: data.trace,
      registerKeys: [
        { key: 'A', cellsId: 'div-a-cells' },
        { key: 'Q', cellsId: 'div-q-cells' }
      ],
      tableBodyEl: tbody,
      stepLabelId: 'div-step-label',
      stepOpId: 'div-step-op',
      prevBtnId: 'div-prev',
      nextBtnId: 'div-next'
    });
  } catch (err) {
    showError('div-error', err.message);
  }
});
