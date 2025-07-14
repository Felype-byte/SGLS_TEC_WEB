// tecnico_dashboard.js

document.addEventListener('DOMContentLoaded', () => {
  const tbody = document.querySelector('#tabela-horarios-intervalo tbody');
  const btnAdd = document.getElementById('btn-add-horario-intervalo');
  const form = document.getElementById('form-inserir-intervalo');
  const spinner = document.getElementById('spinner-loading');

  // Adiciona nova linha de horário
  btnAdd.addEventListener('click', () => {
    const nova = tbody.querySelector('.linha-horario').cloneNode(true);
    nova.querySelectorAll('input').forEach(i => i.value = '');
    nova.style.opacity = 0;
    tbody.appendChild(nova);
    setTimeout(() => nova.style.opacity = 1, 50);
  });

  // Remove linha de horário
  tbody.addEventListener('click', e => {
    if (e.target.classList.contains('btn-remove')) {
      const rows = tbody.querySelectorAll('tr');
      if (rows.length > 1) e.target.closest('tr').remove();
    }
  });

  // Validação e spinner ao enviar formulário
  form.addEventListener('submit', e => {
    const linhas = tbody.querySelectorAll('tr');
    for (const linha of linhas) {
      const inicio = linha.querySelector('input[name="hora_inicio"]').value;
      const fim = linha.querySelector('input[name="hora_fim"]').value;
      if (inicio >= fim) {
        alert("O horário de fim deve ser maior que o horário de início.");
        e.preventDefault();
        return;
      }
    }
    spinner.style.display = 'block';
  });

  // Persistência da última sala selecionada
  document.querySelectorAll('select[name="sala_id"]').forEach(select => {
    select.addEventListener('change', e => {
      localStorage.setItem('ultimaSalaSelecionada', e.target.value);
    });

    const saved = localStorage.getItem('ultimaSalaSelecionada');
    if (saved) select.value = saved;
  });

  // Suaviza o foco em flash message (se houver)
  const flash = document.querySelector('.alert');
  if (flash) {
    flash.scrollIntoView({ behavior: 'smooth' });
  }
});
