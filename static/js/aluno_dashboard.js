document.addEventListener('DOMContentLoaded', () => {
  const grade = document.getElementById('grade-horarios');

  // Aplica estilos aos horários após carregamento
  function aplicarEstiloHorarios() {
    document.querySelectorAll('.horario-slot').forEach(slot => {
      const input = slot.querySelector('input[type="radio"]');
      if (!input) return;

      // Reset
      slot.style.border = '1px solid #ccc';
      slot.style.borderRadius = '8px';
      slot.style.backgroundColor = '';
      slot.title = '';
      slot.classList.remove('selecionado');

      // Aplica visual conforme valor do input (status como texto)
      const status = input.dataset.status;

      if (status === 'Disponível') {
        slot.style.backgroundColor = '#f8f9fa'; // cinza claro
        slot.title = '⬜ Horário disponível para solicitação';
      } else if (status === 'Em processo') {
        slot.style.backgroundColor = '#fdb131'; // amarelo
        slot.title = '🟨 Horário em processo de análise';
      } else if (status === 'Agendado') {
        slot.style.backgroundColor = '#28a74c'; // verde
        slot.title = '🟩 Horário já agendado';
      } else {
        slot.style.backgroundColor = '#6c757d'; // cinza escuro
        slot.title = '🔘 Horário reservado ou indisponível';
      }

      // Interatividade
      if (!input.disabled && status === 'Disponível') {
        slot.classList.add('cursor-pointer');
      }
    });
  }

  // Clique para selecionar
  grade.addEventListener('click', event => {
    const slot = event.target.closest('.horario-slot');
    if (!slot) return;

    const input = slot.querySelector('input[type="radio"]');
    if (!input || input.disabled || input.dataset.status !== 'Disponível') return;

    // Reset estilo anterior
    document.querySelectorAll('.horario-slot').forEach(el => {
      el.classList.remove('selecionado');
      el.style.border = '1px solid #ccc';
      aplicarEstiloHorarios();
    });

    // Aplicar destaque
    slot.classList.add('selecionado');
    slot.style.backgroundColor = '#bee5eb';
    slot.style.border = '2px solid #0d6efd';
  });

  // Atualiza quando há mudanças no DOM (carregamento via AJAX ou template)
  const observer = new MutationObserver(() => aplicarEstiloHorarios());
  observer.observe(grade, { childList: true, subtree: true });
});
