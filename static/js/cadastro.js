// 🔐 Alterna visibilidade da senha e confirmação
function configurarToggleSenha(idInput, idToggle, idIcone) {
  const input = document.getElementById(idInput);
  const toggle = document.getElementById(idToggle);
  const icone = document.getElementById(idIcone);

  if (input && toggle && icone) {
    toggle.addEventListener("click", () => {
      const mostrar = input.type === "password";
      input.type = mostrar ? "text" : "password";
      icone.classList.toggle("bi-eye", mostrar);
      icone.classList.toggle("bi-eye-slash", !mostrar);
    });
  }
}

// ⚠️ Validação individual de campos obrigatórios
function validarCampo(id) {
  const campo = document.getElementById(id);
  if (!campo) return true;

  const vazio = campo.value.trim() === "";
  campo.classList.toggle("is-invalid", vazio);
  return !vazio;
}

// ✅ Validação de CPF (11 dígitos)
function validarCPF(id) {
  const campo = document.getElementById(id);
  if (!campo) return true;

  const cpfLimpo = campo.value.replace(/\D/g, "");
  const valido = cpfLimpo.length === 11;
  campo.classList.toggle("is-invalid", !valido);
  if (!valido) alert("CPF inválido. Deve conter 11 números.");
  return valido;
}

// 🔁 Validação de senhas iguais
function validarSenhas(id1, id2) {
  const s1 = document.getElementById(id1);
  const s2 = document.getElementById(id2);
  if (!s1 || !s2) return true;

  const iguais = s1.value === s2.value;
  s2.classList.toggle("is-invalid", !iguais);
  if (!iguais) alert("As senhas não coincidem.");
  return iguais;
}

document.addEventListener("DOMContentLoaded", () => {
  // 👁 Botões de alternância de visibilidade
  configurarToggleSenha("senha", "toggleSenha", "iconeSenha");
  configurarToggleSenha("confirmaSenha", "toggleConfirmaSenha", "iconeConfirmaSenha");

  const form = document.querySelector("form");

  if (form) {
    form.addEventListener("submit", (e) => {
      let valid = true;

      const camposObrigatorios = [
        "nome",
        "email",
        "senha",
        "confirmaSenha",
        "matricula",
        "cpf",
        "curso",
        "siape",
        "setor"
      ];

      camposObrigatorios.forEach((id) => {
        if (!validarCampo(id)) valid = false;
      });

      if (!validarCPF("cpf")) valid = false;
      if (!validarSenhas("senha", "confirmaSenha")) valid = false;

      if (!valid) {
        e.preventDefault();
        console.log("❌ Cadastro bloqueado por falhas de validação.");
      } else {
        console.log("✅ Cadastro validado com sucesso.");
      }
    });
  }
});
