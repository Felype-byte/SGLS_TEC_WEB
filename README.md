# 🏫 Sistema de Gerenciamento de Laboratórios (SGLS) – UFC Sobral (v1.1.0)

<p align="center">
  <img src="https://img.shields.io/badge/Vers%C3%A3o-1.1.0-2ea44f?style=for-the-badge" alt="Versão 1.1.0"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL"/>
  <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap"/>
  <img src="https://img.shields.io/badge/Frontend-HTML|CSS|JS-orange?style=for-the-badge" alt="Frontend"/>
</p>

## ✨ Visão Geral do Projeto

> O **Sistema de Gerenciamento de Laboratórios (SGLS)** é uma aplicação web robusta, desenvolvida para modernizar e otimizar a gestão de agendamentos no Bloco das Engenharias do Campus Mucambinho da UFC Sobral. O objetivo é eliminar conflitos, oferecer visibilidade em tempo real da disponibilidade das salas e centralizar o histórico de uso, criando uma plataforma intuitiva e eficiente para toda a comunidade acadêmica.

---

## 🎭 Perfis de Usuário e Suas Funções

O sistema dispõe de três níveis de acesso, cada um com permissões específicas:

| Perfil        | Ícone | Funções Principais |
| ------------- | :---: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Aluno** |  👨‍🎓   | - Solicitar agendamento de laboratório, indicando um professor responsável. <br>- Acompanhar status (`Pendente Professor`, `Pendente Técnico`, `Confirmado`, `Cancelado`). <br>- Cancelar solicitações pendentes. <br>- Imprimir comprovante após confirmação. |
| **Professor** |  👨‍🏫   | - Solicitações próprias de uso de laboratório (aulas, pesquisa). <br>- Aprovar ou recusar pedidos de alunos (painel dedicado + termo de responsabilidade). <br>- Visualizar contador de pendências.                                                                           |
| **Técnico** |  🛠️   | - CRUD de salas (nome, capacidade, recursos). <br>- Gerenciar disponibilidade: <ul><li>Inserção em massa (semestre/datas)</li><li>Horários avulsos</li></ul> <br>- Aprovação final de solicitações. <br>- Visão completa de horários.                                         |

---

## 🚀 Funcionalidades Chave

- **Cadastro e Gestão de Salas:** Nome, capacidade, recursos (projetores, ar‑condicionado, etc.).
- **Consulta de Disponibilidade em Tempo Real:** Visualização via calendário e listas.
- **Gerenciamento de Agendamentos:** Fluxo completo de solicitação, aprovação, recusa e cancelamento.
- **Notificações Inteligentes:** E‑mails e alertas internos em cada etapa do fluxo.
- **Dashboard Analítico:** Relatórios de uso e métricas para otimização.
- **Autenticação Segura:** Perfis com JWT e níveis de permissão definidos.

---

## 🌊 Fluxo de Agendamento (Aluno)

1. **Aluno solicita:** Preenche formulário e seleciona professor responsável → status `Pendente Professor`.
2. **Professor avalia:** Aprova ou recusa. <br>• Recusa → fim do processo. <br>• Aprova → status `Pendente Técnico`.
3. **Técnico finaliza:** Aprova ou recusa. <br>• Recusa → fim do processo. <br>• Aprova → status `Agendado` e bloqueio de horário no sistema.

---

## 🛠️ Tecnologias Utilizadas

| Camada         | Tecnologias                        |
| -------------- | ---------------------------------- |
| Front‑end      | HTML5, CSS3, JavaScript, Bootstrap |
| Back‑end       | Python (Flask), Jinja2             |
| Banco de Dados | MySQL                              |
| Autenticação   | JWT (JSON Web Tokens)              |

---

## ⚙️ Como Configurar e Executar

### Pré‑requisitos

- Python 3.x
- MySQL em execução
- Git

### Passos

1. **Clonar o repositório**
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <PASTA_DO_PROJETO>
   ```

2. **Criar ambiente virtual**
   ```bash
   python -m venv venv
   # Ativar:
   # Windows: .\venv\Scripts\activate
   # macOS/Linux: source venv/bin/activate
   ```

3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar conexão ao banco**
   Preencha seu `.env` ou `config.py` com:
   ```env
   DB_HOST=<host>
   DB_USER=<usuário>
   DB_PASS=<senha>
   DB_NAME=<banco>
   JWT_SECRET=<chave_secreta>
   ```

5. **Executar a aplicação**
   ```bash
   python main.py
   ```
   Acesse em `http://127.0.0.1:5000/`.

---

## 🤝 Como Contribuir

Ficamos felizes com o seu interesse em tornar o **SGLS** ainda melhor! Contribuições, relatos de bugs (*issues*) e envio de *pull requests* são fundamentais para a evolução do sistema.

Siga este passo a passo para contribuir com o código:

1. Faça um **Fork** deste repositório.
2. Crie uma nova *branch* para a sua alteração:
   ```bash
   git checkout -b feature/minha-melhoria
   ```
3. Faça o *commit* das suas alterações (dê preferência a mensagens claras e objetivas):
   ```bash
   git commit -m "feat: Adiciona nova funcionalidade na tela de agendamento"
   ```
4. Faça o *push* para a sua *branch*:
   ```bash
   git push origin feature/minha-melhoria
   ```
5. Abra um **Pull Request** neste repositório detalhando o que foi feito.

Sinta-se à vontade para explorar o código, sugerir melhorias e ajudar a nossa comunidade acadêmica!

---

<p align="center">
  <b>© 2025 UFC Sobral – Bloco das Engenharias</b><br>
  <i>Desenvolvido com dedicação para a gestão eficiente dos laboratórios.</i>
</p>