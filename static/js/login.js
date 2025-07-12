// 🔄 Alternância entre abas de perfil (Aluno, Professor, Técnico)
function showTab(tabId, element) {
  document
    .querySelectorAll(".tab")
    .forEach((tab) => tab.classList.remove("active"));
  element.classList.add("active");

  document
    .querySelectorAll(".form-content")
    .forEach((form) => form.classList.remove("active"));
  document.getElementById(tabId).classList.add("active");
}

// 🚀 Inicializações após o carregamento da página
document.addEventListener("DOMContentLoaded", () => {
  // Nenhuma funcionalidade adicional no momento
  // showTab pode ser invocado diretamente nos elementos onclick do HTML
});
