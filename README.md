🏫 Sistema de Gerenciamento de Laboratórios (SGL) UFC Sobral 🏫✨ Visão Geral do ProjetoO Sistema de Gerenciamento de Laboratórios (SGL) é uma aplicação web robusta, desenvolvida para modernizar e otimizar a gestão e o uso dos espaços no Bloco das Engenharias do Campus Mucambinho da UFC Sobral. Nosso objetivo é eliminar conflitos de agendamento, proporcionar visibilidade em tempo real sobre a disponibilidade das salas e centralizar o histórico de uso, reduzindo o retrabalho administrativo. O SGL é uma plataforma intuitiva e integrada, acessível via navegador web, projetada para facilitar o agendamento, a liberação e o monitoramento do uso das salas de aula de forma eficiente e transparente.🚀 Funcionalidades ChaveCadastro e Gestão de Salas: Gerencie detalhes completos das salas, incluindo nome, capacidade e recursos disponíveis (projetores, ar-condicionado, etc.).Consulta de Disponibilidade em Tempo Real: Visualize a ocupação das salas através de interfaces intuitivas como calendários e listas.Gerenciamento de Agendamentos: Controle todo o ciclo de reservas, desde a solicitação até a aprovação, rejeição ou cancelamento.Sistema de Notificações Inteligente: Receba e-mails e alertas internos sobre o status das reservas, incluindo confirmações, modificações, cancelamentos e conflitos.Relatórios e Análises (Dashboard Analítico): Acesse dados valiosos sobre o uso das salas para embasar decisões e otimizar a alocação de recursos.Autenticação de Usuários Segura: Garanta que apenas usuários autorizados (Administrador, Professor/Docente, Técnico Administrativo) possam interagir com o sistema, com diferentes níveis de permissão.🛠️ Tecnologias UtilizadasFront-end: HTML5, CSS3, JavaScript com Bootstrap (para interfaces responsivas e padronizadas).Back-end: Python (com um framework web, como Flask ou Django, se aplicável, ou scripts Python puros para a lógica do servidor).Banco de Dados: MySQL (online e já configurado, para armazenamento relacional e seguro de usuários, salas e reservas).Autenticação: JWT (JSON Web Tokens) (para controle de sessão e permissões de acesso seguro).⚙️ Como Configurar e Executar o ProjetoSiga os passos abaixo para configurar e colocar o SGL em funcionamento no seu ambiente local.Pré-requisitosCertifique-se de ter o seguinte software instalado em sua máquina:Python 3.x: Você pode baixá-lo em python.org.1. Clonar o RepositórioComece clonando o código do projeto para a sua máquina local:git clone <URL_DO_SEU_REPOSITORIO>
cd <nome_da_pasta_do_projeto>

2. Instalar as Dependências do ProjetoRecomendamos o uso de um ambiente virtual para isolar as dependências do seu projeto.# Criar o ambiente virtual (se ainda não tiver)
   python -m venv venv

# Ativar o ambiente virtual

# No Windows:

.\venv\Scripts\activate

# No macOS/Linux:

source venv/bin/activate

# Instalar as dependências listadas no requirements.txt

pip install -r requirements.txt

3. Executar o ProjetoCom o ambiente virtual ativado e as dependências instaladas, você pode iniciar o servidor da sua aplicação:python main.py

4. Acessar a Interface WebApós executar python main.py, o script irá iniciar o servidor e geralmente exibirá um endereço (URL) no seu terminal, indicando onde a interface web está sendo executada (ex: http://127.0.0.1:5000/ ou http://localhost:8080/).Copie este endereço e cole-o no seu navegador de preferência para acessar a plataforma do Sistema de Gerenciamento de Laboratórios UFC Sobral e começar a gerenciar suas salas!🤝 Contribuições: Sinta-se à vontade para contribuir com melhorias ou relatar problemas!
