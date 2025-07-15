/**
 * SGHL - Script do Painel do Aluno
 * Contém a lógica para carregamento de horários e impressão de comprovantes/autorizações.
 */

document.addEventListener("DOMContentLoaded", () => {
  /*******************************************************
   *  SEÇÃO 1: GERENCIAMENTO DE AGENDAMENTO DE HORÁRIOS  *
   *******************************************************/

  const grade = document.getElementById("grade-horarios");

  if (grade) {
    // Função para carregar horários dinamicamente
    window.carregarHorarios = function () {
      const salaId = document.getElementById("sala_id").value;
      const data = document.getElementById("data").value;
      grade.innerHTML =
        "<p class='text-muted ml-3'>🔄 Carregando horários...</p>";

      if (!salaId || !data) {
        grade.innerHTML =
          "<p class='text-danger ml-3'><strong>Erro:</strong> Selecione um laboratório e uma data para continuar.</p>";
        return;
      }

      fetch(`/dashboard/aluno/horarios?sala_id=${salaId}&data=${data}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Falha na rede ou na resposta do servidor.");
          }
          return response.json();
        })
        .then((horarios) => {
          grade.innerHTML = "";
          if (!horarios.length) {
            grade.innerHTML =
              "<p class='text-muted ml-3'>Nenhum horário disponível para esta data. Por favor, tente outra.</p>";
            return;
          }
          // Garante que o container de horários tenha a classe 'row' do Bootstrap
          grade.classList.add("row");

          horarios.forEach((h) => {
            grade.innerHTML += `
              <div class="col-md-4 mb-3">
                <label class="horario-slot painel-horario-slot d-block text-center py-3 px-2 rounded shadow-sm">
                  <input 
                    type="radio" 
                    name="horario_id" 
                    value="${h.id}" 
                    class="d-none" 
                    data-status="${h.status}" 
                    ${h.status !== "Disponível" ? "disabled" : ""}>
                  ${h.texto}
                </label>
              </div>`;
          });
          atualizarTodosSlots();
        })
        .catch((error) => {
          grade.innerHTML = `<p class='text-danger ml-3'><strong>Erro ao carregar:</strong> Não foi possível buscar os horários. Tente novamente.</p>`;
          console.error("Fetch error:", error);
        });
    };

    function aplicarStatusSlot(slot) {
      const input = slot.querySelector('input[type="radio"]');
      if (!input) return;

      slot.classList.remove(
        "selecionado",
        "horario-disponivel",
        "horario-processo",
        "horario-agendado",
        "horario-indisponivel"
      );
      let status = input.dataset.status;

      if (input.checked && status === "Disponível") {
        slot.classList.add("selecionado", "horario-disponivel");
      } else if (status === "Disponível") {
        slot.classList.add("horario-disponivel");
      } else if (status === "Em processo") {
        slot.classList.add("horario-processo");
      } else if (status === "Agendado") {
        slot.classList.add("horario-agendado");
      } else {
        slot.classList.add("horario-indisponivel");
      }
    }

    function atualizarTodosSlots() {
      document.querySelectorAll(".horario-slot").forEach(aplicarStatusSlot);
    }

    grade.addEventListener("click", (event) => {
      const slot = event.target.closest(".horario-slot");
      if (!slot) return;
      const input = slot.querySelector('input[type="radio"]');
      if (!input || input.disabled) return;

      document
        .querySelectorAll('.horario-slot input[type="radio"]')
        .forEach((i) => (i.checked = false));
      input.checked = true;

      atualizarTodosSlots();
    });

    const observer = new MutationObserver(atualizarTodosSlots);
    observer.observe(grade, { childList: true, subtree: true });

    atualizarTodosSlots();
  }

  /**********************************************************
   *  SEÇÃO 2: IMPRESSÃO DO TERMO DE AUTORIZAÇÃO FORMAL     *
   **********************************************************/

  document.body.addEventListener("click", function (event) {
    const botaoImprimir = event.target.closest(".btn-imprimir");
    if (botaoImprimir) {
      const dados = {
        alunoNome: botaoImprimir.dataset.alunoNome,
        alunoMatricula: botaoImprimir.dataset.alunoMatricula,
        salaInfo: botaoImprimir.dataset.salaInfo,
        data: botaoImprimir.dataset.data,
        horario: botaoImprimir.dataset.horario,
        professor: botaoImprimir.dataset.professor,
        justificativa: botaoImprimir.dataset.justificativa,
        solicitacaoId: botaoImprimir.dataset.solicitacaoId,
        dataEmissao: new Date().toLocaleDateString("pt-BR", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
        }),
      };

      const logoElement = document.querySelector(".logo-ufc");
      const logoUrl = logoElement ? logoElement.src : "";

      gerarEImprimirTermo(dados, logoUrl);
    }
  });

  function gerarEImprimirTermo(dados, logoUrl) {
    const conteudoHtml = `
      <!DOCTYPE html>
      <html lang="pt-br">
      <head>
        <meta charset="UTF-8">
        <title>Termo de Autorização - ${dados.alunoNome}</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css" />
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Playfair+Display:wght@700&display=swap');
          
          body { font-family: 'Inter', 'Segoe UI', Arial, sans-serif; color: #333; margin: 0; padding: 0; background: #fff; }
          .comprovante-wrapper { width: 210mm; min-height: 297mm; margin: 0 auto; padding: 40px; box-sizing: border-box; }
          
          .comprovante-header { display: flex; align-items: center; text-align: center; flex-direction: column; padding-bottom: 20px; margin-bottom: 30px; border-bottom: 2px solid #003f6f; }
          .logo-ufc { max-height: 65px; margin-bottom: 15px; }
          .titulo-header h1 { font-family: 'Playfair Display', serif; color: #003f6f; font-size: 2rem; margin: 0; }
          .titulo-header span { font-size: 1.1rem; color: #666; }
  
          .secao { margin-bottom: 30px; }
          .secao h2 { font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.5px; color: #003f6f; border-bottom: 1.5px solid #e0e0e0; padding-bottom: 8px; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
          .secao p { font-size: 1.05rem; line-height: 1.6; margin: 8px 0; }
          .secao strong { color: #000; font-weight: 600; }
  
          .termo-declaracao { margin-top: 40px; margin-bottom: 40px; background-color: #f8f9fa; border-left: 5px solid #f2a900; padding: 20px 25px; }
          .termo-declaracao p { font-size: 1.1rem; line-height: 1.7; text-align: justify; }
          
          .assinatura-bloco { margin-top: 80px; text-align: center; }
          .assinatura-bloco hr { width: 350px; margin: 0 auto 5px auto; border: 0; border-top: 1px solid #555; }
          .assinatura-bloco p { font-size: 1rem; margin: 0; }
          
          .comprovante-footer { text-align: center; font-size: 0.85rem; color: #888; border-top: 1px solid #ccc; padding-top: 20px; margin-top: 40px; }
          @media print { body { -webkit-print-color-adjust: exact; print-color-adjust: exact; } .comprovante-wrapper { box-shadow: none; border: none; } }
        </style>
      </head>
      <body>
        <div class="comprovante-wrapper">
          <div class="comprovante-header">
            <img src="${logoUrl}" alt="Logo UFC" class="logo-ufc" />
            <div class="titulo-header">
              <h1>Termo de Autorização</h1>
              <span>Uso de Laboratório Didático – UFC Campus Sobral</span>
            </div>
          </div>
  
          <div class="secao">
            <h2><i class="bi bi-file-earmark-text-fill"></i> Detalhes da Solicitação</h2>
            <p><strong>Solicitante (Aluno):</strong> ${
              dados.alunoNome
            } (Matrícula: ${dados.alunoMatricula})</p>
            <p><strong>Laboratório Agendado:</strong> ${dados.salaInfo}</p>
            <p><strong>Data de Utilização:</strong> ${dados.data}</p>
            <p><strong>Horário Reservado:</strong> ${dados.horario}</p>
          </div>
  
          <div class="termo-declaracao">
            <p>
              Eu, professor(a) <strong>${dados.professor}</strong>,
              vinculado(a) à Universidade Federal do Ceará - Campus Sobral, declaro para os devidos fins que o(a) aluno(a) supracitado(a)
              está formalmente autorizado(a) a utilizar as instalações e equipamentos do laboratório
              identificado, na data e horário especificados, para a finalidade de
              "<strong>${dados.justificativa}</strong>".
            </p>
          </div>
  
          <div class="assinatura-bloco">
            <p>Sobral, ${new Date().toLocaleDateString("pt-BR", {
              day: "2-digit",
              month: "long",
              year: "numeric",
            })}.</p>
            <br><br>
            <hr />
            <p><strong>${dados.professor}</strong></p>
            <p>Professor(a) Responsável</p>
          </div>
          
          <div class="comprovante-footer">
            <p>ID da Solicitação: ${dados.solicitacaoId} | Emitido em ${
      dados.dataEmissao
    } pelo SGHL</p>
            <p>Este é um documento oficial gerado pelo sistema. A validade está condicionada à assinatura do professor responsável.</p>
          </div>
        </div>
      </body>
      </html>
    `;

    const iframe = document.createElement("iframe");
    iframe.style.position = "fixed";
    iframe.style.top = "-9999px";
    iframe.style.left = "-9999px";
    document.body.appendChild(iframe);

    iframe.contentWindow.document.open();
    iframe.contentWindow.document.write(conteudoHtml);
    iframe.contentWindow.document.close();

    iframe.onload = function () {
      iframe.contentWindow.focus();
      iframe.contentWindow.print();
      setTimeout(() => {
        document.body.removeChild(iframe);
      }, 500);
    };
  }
});
