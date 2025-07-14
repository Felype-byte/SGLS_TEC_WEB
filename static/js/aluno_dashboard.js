document.addEventListener('DOMContentLoaded', () => {
  const grade = document.getElementById('grade-horarios');

  // Função para carregar horários dinamicamente
  window.carregarHorarios = function() {
    const salaId = document.getElementById("sala_id").value;
    const data = document.getElementById("data").value;
    grade.innerHTML = "<p class='text-muted ml-3'>🔄 Carregando horários...</p>";

    if (!salaId || !data) {
      grade.innerHTML = "<p class='text-danger ml-3'>Selecione uma sala e uma data válida.</p>";
      return;
    }

    fetch(`/dashboard/aluno/horarios?sala_id=${salaId}&data=${data}`)
      .then(response => response.json())
      .then(horarios => {
        grade.innerHTML = "";
        if (!horarios.length) {
          grade.innerHTML = "<p class='text-muted ml-3'>Nenhum horário disponível para esta data.</p>";
          return;
        }
        horarios.forEach((h, idx) => {
          if (idx % 3 === 0) grade.innerHTML += `<div class='w-100'></div>`;
          grade.innerHTML += `
            <div class="col-md-4 mb-3">
              <label class="horario-slot painel-horario-slot d-block text-center py-3 px-2 rounded shadow-sm">
                <input 
                  type="radio" 
                  name="horario_id" 
                  value="${h.id}" 
                  class="d-none" 
                  data-status="${h.status}" 
                  ${h.status !== 'Disponível' ? 'disabled' : ''}>
                ${h.texto}
              </label>
            </div>`;
        });
        // Garante aplicação de estilos nos slots carregados
        atualizarTodosSlots();
      });
  };

  function aplicarStatusSlot(slot) {
    const input = slot.querySelector('input[type="radio"]');
    if (!input) return;

    // Remove estilos anteriores
    slot.classList.remove(
      'selecionado', 'horario-disponivel', 'horario-processo', 'horario-agendado', 'horario-indisponivel'
    );

    let status = input.dataset.status;

    if (input.checked && status === "Disponível") {
      slot.classList.add('selecionado', 'horario-disponivel');
    } else if (status === "Disponível") {
      slot.classList.add('horario-disponivel');
    } else if (status === "Em processo") {
      slot.classList.add('horario-processo');
    } else if (status === "Agendado") {
      slot.classList.add('horario-agendado');
    } else {
      slot.classList.add('horario-indisponivel');
    }
  }

  function atualizarTodosSlots() {
    document.querySelectorAll('.horario-slot').forEach(aplicarStatusSlot);
  }

  // Seleção visual ao clicar
  grade.addEventListener('click', event => {
    const slot = event.target.closest('.horario-slot');
    if (!slot) return;
    const input = slot.querySelector('input[type="radio"]');
    if (!input || input.disabled || input.dataset.status !== 'Disponível') return;

    // Desmarca todos
    document.querySelectorAll('.horario-slot').forEach(s => {
      s.classList.remove('selecionado');
      const inp = s.querySelector('input[type="radio"]');
      if (inp) inp.checked = false;
    });

    // Marca clicado
    slot.classList.add('selecionado');
    input.checked = true;
    aplicarStatusSlot(slot);
  });

  // Observa DOM dinâmico (ajax etc)
  const observer = new MutationObserver(atualizarTodosSlots);
  observer.observe(grade, { childList: true, subtree: true });

  // Inicial
  atualizarTodosSlots();
});
