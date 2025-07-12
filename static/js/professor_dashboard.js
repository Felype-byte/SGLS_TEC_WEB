function carregarHorarios() {
  const salaId = document.getElementById('sala_id').value;
  const dataSelecionada = document.getElementById('data').value;
  const container = document.getElementById('grade-horarios');

  if (!salaId || !dataSelecionada) {
    alert('Selecione uma sala e uma data primeiro.');
    return;
  }

  fetch(`/dashboard/professor/horarios?sala_id=${salaId}&data=${dataSelecionada}`)
    .then(response => response.json())
    .then(horarios => {
      container.innerHTML = '';

      if (horarios.length === 0) {
        container.innerHTML = '<p class="text-muted ml-3">Nenhum horário disponível nesta data.</p>';
        return;
      }

      horarios.forEach(h => {
        const col = document.createElement('div');
        col.className = 'col-md-3 mb-3';

        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = `btn btn-block horario-btn ${
          h.status === 'Disponível'     ? 'btn-outline-secondary' :
          h.status === 'Em processo'    ? 'btn-warning' :
          h.status === 'Agendado'       ? 'btn-success' :
                                          'btn-secondary'
        }`;
        btn.textContent = h.texto;
        btn.dataset.id = h.id;

        if (h.status !== 'Disponível') {
          btn.disabled = true;
          btn.title = h.status === 'Em processo'
            ? '⏳ Horário em análise. Aguarde confirmação.'
            : h.status === 'Agendado'
              ? '✅ Horário já agendado. Indisponível.'
              : 'Horário reservado ou não disponível.';

          btn.textContent += h.status === 'Em processo' ? ' ⏳'
                             : h.status === 'Agendado'  ? ' ✅'
                             : '';
        } else {
          btn.onclick = () => selecionarHorario(h.id, btn);
        }

        col.appendChild(btn);
        container.appendChild(col);
      });
    })
    .catch(err => {
      container.innerHTML = '<p class="text-danger">Erro ao carregar horários. Tente novamente.</p>';
      console.error(err);
    });
}

function selecionarHorario(idHorario, botaoClicado) {
  // Remover seleção anterior
  document.querySelectorAll('.horario-btn').forEach(btn => {
    if (!btn.disabled) {
      btn.classList.remove('btn-info');
      btn.classList.add('btn-outline-secondary');
    }
  });

  // Selecionar novo
  botaoClicado.classList.remove('btn-outline-secondary');
  botaoClicado.classList.add('btn-info');

  // Adicionar campo oculto ao formulário
  let inputHidden = document.getElementById('input-horario-id');
  if (!inputHidden) {
    inputHidden = document.createElement('input');
    inputHidden.type = 'hidden';
    inputHidden.name = 'horario_id';
    inputHidden.id = 'input-horario-id';
    document.querySelector('form').appendChild(inputHidden);
  }
  inputHidden.value = idHorario;
}
