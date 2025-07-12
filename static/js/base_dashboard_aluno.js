function aplicarEstiloStatusModal() {
  const agendamentos = document.querySelectorAll('.agendamento-item');

  agendamentos.forEach(item => {
    const badge = item.querySelector('.solicitacao-status');
    const btnContainer = item.querySelector('.btn-container');
    const cancelUrl = item.dataset.cancelUrl;
    const status = badge?.dataset.status;

    if (!badge || !status) return;

    // Reset
    badge.className = 'badge solicitacao-status';
    badge.textContent = '';

    // Badge texto + cor
    switch (status) {
      case 'Pendente Professor':
        badge.classList.add('badge-warning');
        badge.textContent = '🟡 Aguardando aprovação do Professor';
        break;
      case 'Pendente Tecnico':
        badge.classList.add('badge-warning');
        badge.textContent = '🟡 Aguardando análise do Técnico';
        break;
      case 'Agendado':
        badge.classList.add('badge-success');
        badge.textContent = '✅ Confirmado';
        break;
      case 'Negado Professor':
        badge.classList.add('badge-danger');
        badge.textContent = '❌ Recusado pelo Professor';
        break;
      case 'Negado Tecnico':
        badge.classList.add('badge-danger');
        badge.textContent = '❌ Recusado pelo Técnico';
        break;
      case 'Cancelado pelo aluno':
        badge.classList.add('badge-secondary');
        badge.textContent = '⚪ Cancelado pelo Aluno';
        break;
      default:
        badge.classList.add('badge-secondary');
        badge.textContent = '🔘 Outros';
    }

    // Botão Cancelar
    if (btnContainer) {
      btnContainer.innerHTML = ''; // limpar conteúdo anterior

      const podeCancelar = ['Pendente Professor', 'Pendente Tecnico', 'Agendado'].includes(status);

      if (podeCancelar && cancelUrl) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = cancelUrl;
        form.className = 'mb-0';
        form.onsubmit = () => confirm('Tem certeza que deseja cancelar este agendamento?');

        const button = document.createElement('button');
        button.type = 'submit';
        button.className = 'btn btn-outline-danger btn-sm d-flex align-items-center px-3 rounded';
        button.innerHTML = '<i class="bi bi-x-circle-fill mr-2"></i> Cancelar';

        form.appendChild(button);
        btnContainer.appendChild(form);
      }
    }
  });
}

// Reaplicar estilo quando o modal abrir
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('modalAgendamentoStatus');
  if (modal) {
    modal.addEventListener('shown.bs.modal', aplicarEstiloStatusModal);
  }

  // Fallback: aplicar ao carregar página caso o modal já esteja renderizado
  aplicarEstiloStatusModal();
});
