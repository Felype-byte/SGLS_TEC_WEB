// Função genérica para alternar visibilidade da senha
function configurarToggleSenha(idInput, idToggle, idIcone) {
  const input = document.getElementById(idInput);
  const toggle = document.getElementById(idToggle);
  const icone = document.getElementById(idIcone);

  if (input && toggle && icone) {
    toggle.addEventListener("click", () => {
      const isSenha = input.type === "password";
      input.type = isSenha ? "text" : "password";
      icone.classList.toggle("bi-eye");
      icone.classList.toggle("bi-eye-slash");
    });
  }
}
const modalDetalhes = document.getElementById("modalDetalhesAgendamento");

if (modalDetalhes) {
  modalDetalhes.addEventListener("show.bs.modal", function (event) {
    // O botão que acionou o modal
    const button = event.relatedTarget;

    // Extrai as informações dos atributos data-* do botão
    const status = button.getAttribute("data-status");
    const statusClass = button.getAttribute("data-status-class");
    const laboratorio = button.getAttribute("data-laboratorio");
    const dataHorario = button.getAttribute("data-data-horario");
    const solicitante = button.getAttribute("data-solicitante");
    const aprovadorProf = button.getAttribute("data-aprovador-prof");
    const aprovadorTec = button.getAttribute("data-aprovador-tec");
    const motivo = button.getAttribute("data-motivo");

    // Pega os elementos dentro do modal para preencher
    const modalStatus = modalDetalhes.querySelector("#detalhes-status");
    const modalLab = modalDetalhes.querySelector("#detalhes-laboratorio");
    const modalData = modalDetalhes.querySelector("#detalhes-data-horario");
    const modalSolicitante = modalDetalhes.querySelector(
      "#detalhes-solicitante"
    );
    const modalAprovProf = modalDetalhes.querySelector(
      "#detalhes-aprovador-prof"
    );
    const modalAprovTec = modalDetalhes.querySelector(
      "#detalhes-aprovador-tec"
    );

    const motivoContainer = modalDetalhes.querySelector(
      "#detalhes-motivo-container"
    );
    const motivoTexto = modalDetalhes.querySelector("#detalhes-motivo-texto");

    // Preenche os campos do modal com as informações
    modalStatus.textContent = status;
    modalStatus.className = "badge " + statusClass; // Reseta as classes e aplica a nova
    modalLab.textContent = laboratorio;
    modalData.textContent = dataHorario;

    // Preenche o histórico
    modalSolicitante.innerHTML = `<i class="bi bi-person-fill text-muted"></i> <strong>Solicitado por:</strong> ${solicitante}`;
    modalAprovProf.innerHTML = `<i class="bi bi-person-check-fill text-muted"></i> <strong>Etapa Professor:</strong> ${aprovadorProf}`;
    modalAprovTec.innerHTML = `<i class="bi bi-person-workspace text-muted"></i> <strong>Etapa Técnico:</strong> ${aprovadorTec}`;

    // Lógica para mostrar o motivo (se houver)
    if (motivo) {
      motivoTexto.textContent = motivo;
      motivoContainer.style.display = "block";
    } else {
      motivoContainer.style.display = "none";
    }
  });
}

// Inicializações (executa após o carregamento do DOM)
document.addEventListener("DOMContentLoaded", () => {
  configurarToggleSenha("senha", "toggleSenha", "iconeSenha");
  configurarToggleSenha(
    "confirmaSenha",
    "toggleConfirmaSenha",
    "iconeConfirmaSenha"
  );

  // Se no login, ids podem ser os mesmos
  configurarToggleSenha("senhaLogin", "toggleSenhaLogin", "iconeSenhaLogin");
});

document.addEventListener("DOMContentLoaded", () => {
  // Configura botões de mostrar senha
  configurarToggleSenha("senha", "toggleSenha", "iconeSenha");
  configurarToggleSenha(
    "confirmaSenha",
    "toggleConfirmaSenha",
    "iconeConfirmaSenha"
  );

  // Validação de formulário de cadastro
  const form = document.querySelector("form");

  if (form) {
    form.addEventListener("submit", function (e) {
      const senha = document.getElementById("senha");
      const confirma = document.getElementById("confirmaSenha");
      const cpf = document.getElementById("cpf");

      // Campos obrigatórios (validação básica)
      const camposObrigatorios = [
        "matricula",
        "nome",
        "email",
        "curso",
        "turma",
        "cpf",
        "senha",
        "confirmaSenha",
      ];
      let valid = true;

      camposObrigatorios.forEach((id) => {
        const campo = document.getElementById(id);
        if (!campo || campo.value.trim() === "") {
          campo.classList.add("is-invalid");
          valid = false;
        } else {
          campo.classList.remove("is-invalid");
        }
      });

      // Verifica se as senhas coincidem
      if (senha.value !== confirma.value) {
        confirma.classList.add("is-invalid");
        alert("As senhas não coincidem!");
        valid = false;
      }

      // Validação simples de CPF (apenas 11 dígitos)
      const cpfLimpo = cpf.value.replace(/\D/g, "");
      if (cpfLimpo.length !== 11) {
        cpf.classList.add("is-invalid");
        alert("CPF inválido. Deve conter 11 números.");
        valid = false;
      }

      if (!valid) e.preventDefault(); // Impede o envio se algo estiver errado
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  // Seleção múltipla de horários
  const botoesHorario = document.querySelectorAll(".horario-slot.disponivel");

  botoesHorario.forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.classList.toggle("selecionado");
    });
  });

  // (Opcional) validação ao clicar em "Solicitar Agendamento"
  const solicitarBtn = document.querySelector(".btn-success");
  if (solicitarBtn) {
    solicitarBtn.addEventListener("click", (e) => {
      const selecionados = document.querySelectorAll(
        ".horario-slot.selecionado"
      );
      const confirmacao = document.getElementById("responsabilidade");

      if (selecionados.length === 0) {
        e.preventDefault();
        alert("Selecione ao menos um horário para agendar.");
        return;
      }

      if (!confirmacao.checked) {
        e.preventDefault();
        alert("Você deve aceitar o termo de responsabilidade.");
        return;
      }

      // Aqui você poderia enviar os dados via fetch() ou formulário
      alert(
        `Horários selecionados: ${[...selecionados]
          .map((b) => b.textContent.trim())
          .join(", ")}`
      );
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const formModal = document.getElementById("formModalSolicitacao");

  if (formModal) {
    formModal.addEventListener("submit", function (e) {
      e.preventDefault();

      const nome = document.getElementById("nomeAluno").value.trim();
      const matricula = document.getElementById("matriculaAluno").value.trim();
      const curso = document.getElementById("cursoAluno").value.trim();

      const horariosSelecionados = [
        ...document.querySelectorAll(".horario-slot.selecionado"),
      ].map((btn) => btn.textContent.trim());

      if (horariosSelecionados.length === 0) {
        alert("Selecione ao menos um horário para agendar.");
        return;
      }

      if (!nome || !matricula || !curso) {
        alert("Preencha todos os dados do aluno.");
        return;
      }

      // Aqui você pode enviar os dados via AJAX ou gravar temporariamente
      alert(
        `Solicitação confirmada para ${nome} (${matricula}) em:\n${horariosSelecionados.join(
          ", "
        )}`
      );

      // Fecha o modal
      $("#modalSolicitacao").modal("hide");

      // Limpa os campos se quiser
      formModal.reset();
      document
        .querySelectorAll(".horario-slot.selecionado")
        .forEach((btn) => btn.classList.remove("selecionado"));
      document.getElementById("responsabilidade").checked = false;
    });
  }
});
