function carregarHorarios() {
  const salaId = document.getElementById('sala_id').value;
  const dataSelecionada = document.getElementById('data').value;
  const container = document.getElementById('grade-horarios');

  container.innerHTML = '<p class="text-muted ml-3">🔄 Carregando horários...</p>';

  if (!salaId || !dataSelecionada) {
    container.innerHTML = '<p class="text-danger ml-3">Selecione uma sala e uma data válida.</p>';
    return;
  }

  fetch(`/dashboard/professor/horarios?sala_id=${salaId}&data=${dataSelecionada}`)
    .then(response => response.json())
    .then(horarios => {
      container.innerHTML = '';

      if (!horarios.length) {
        container.innerHTML = '<p class="text-muted ml-3">Nenhum horário disponível nesta data.</p>';
        return;
      }

      horarios.forEach((h, idx) => {
        // Quebra de linha a cada 3
        if (idx % 3 === 0) container.innerHTML += `<div class="w-100"></div>`;

        // Card de horário como label
        container.innerHTML += `
          <div class="col-md-4 mb-3">
            <label class="horario-slot painel-horario-slot d-block text-center py-3 px-2 rounded shadow-sm"
                   data-status="${h.status}"
                   title="${getHorarioTitle(h.status)}">
              <input 
                type="radio" 
                name="horario_id" 
                value="${h.id}" 
                class="d-none"
                ${h.status !== 'Disponível' ? 'disabled' : ''}
              >
              ${h.texto}
            </label>
          </div>
        `;
      });

      aplicarEstilosHorarios();
    })
    .catch(err => {
      container.innerHTML = '<p class="text-danger">Erro ao carregar horários. Tente novamente.</p>';
      console.error(err);
    });
}

function getHorarioTitle(status) {
  if (status === 'Disponível') return '⬜ Horário disponível para solicitação';
  if (status === 'Em processo') return '🟨 Horário em análise';
  if (status === 'Agendado') return '🟩 Horário já agendado';
  return '🔘 Horário reservado ou indisponível';
}

// Aplica as classes de cor/status nos cards, igual ao aluno
function aplicarEstilosHorarios() {
  const slots = document.querySelectorAll('.horario-slot');
  slots.forEach(slot => {
    const input = slot.querySelector('input[type="radio"]');
    const status = slot.dataset.status;

    slot.classList.remove(
      'selecionado', 'horario-disponivel', 'horario-processo',
      'horario-agendado', 'horario-indisponivel'
    );

    if (input.checked && status === 'Disponível') {
      slot.classList.add('selecionado', 'horario-disponivel');
    } else if (status === 'Disponível') {
      slot.classList.add('horario-disponivel');
    } else if (status === 'Em processo') {
      slot.classList.add('horario-processo');
    } else if (status === 'Agendado') {
      slot.classList.add('horario-agendado');
    } else {
      slot.classList.add('horario-indisponivel');
    }
  });
}

// Seleção visual do horário
document.addEventListener('click', event => {
  const slot = event.target.closest('.horario-slot');
  if (!slot) return;

  const input = slot.querySelector('input[type="radio"]');
  if (!input || input.disabled || slot.dataset.status !== 'Disponível') return;

  // Remove seleção de todos
  document.querySelectorAll('.horario-slot').forEach(s => {
    s.classList.remove('selecionado');
    const inp = s.querySelector('input[type="radio"]');
    if (inp) inp.checked = false;
  });

  // Seleciona o clicado
  slot.classList.add('selecionado');
  input.checked = true;

  aplicarEstilosHorarios();
});

// Reaplica estilos após renderização dinâmica
const grade = document.getElementById('grade-horarios');
if (grade) {
  const observer = new MutationObserver(aplicarEstilosHorarios);
  observer.observe(grade, { childList: true, subtree: true });
}
