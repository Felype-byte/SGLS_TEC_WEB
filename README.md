# 🏫 Sistema de Gerenciamento de Laboratórios (SGL) – UFC Sobral

## ✨ Visão Geral do Projeto

O **Sistema de Gerenciamento de Laboratórios (SGL)** é uma aplicação web desenvolvida para modernizar e otimizar a gestão de espaços no Bloco das Engenharias do Campus Mucambinho da UFC Sobral. Seu objetivo principal é:

- Eliminar conflitos de agendamento
- Proporcionar visibilidade em tempo real da disponibilidade das salas
- Centralizar o histórico de uso e reduzir retrabalho administrativo

A plataforma é totalmente acessível via navegador e oferece uma interface intuitiva para agendar, liberar e monitorar o uso das salas com eficiência e transparência.

---

## 🚀 Funcionalidades Principais

1. **Cadastro e Gestão de Salas**

   - Definição de nome, capacidade e recursos (projetores, ar‑condicionado, etc.)

2. **Consulta de Disponibilidade em Tempo Real**

   - Visualização em calendário e listas interativas

3. **Gerenciamento de Agendamentos**

   - Solicitação, aprovação, rejeição e cancelamento de reservas

4. **Sistema de Notificações Inteligente**

   - E‑mails e alertas internos sobre status de reservas e possíveis conflitos

5. **Relatórios e Análises (Dashboard Analítico)**

   - Gráficos e métricas de uso para otimizar a alocação de recursos

6. **Autenticação de Usuários Segura**
   - Perfis: Administrador, Professor/Docente, Técnico Administrativo
   - Controle de permissão baseado em JWT

---

## 🛠️ Tecnologias Utilizadas

| Camada         | Tecnologia / Ferramenta            |
| -------------- | ---------------------------------- |
| Front‑end      | HTML5, CSS3, JavaScript, Bootstrap |
| Back‑end       | Python (Flask ou Django)           |
| Banco de Dados | MySQL (remoto ou local)            |
| Autenticação   | JWT (JSON Web Tokens)              |

---

## ⚙️ Como Configurar e Executar

### 1. Pré‑requisitos

- **Python 3.x** (instale via [python.org](https://www.python.org/))
- **MySQL** em execução (local ou remoto)

---

### 2. Clonar o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <nome_da_pasta_do_projeto>
```

---

### 3. Criar e Ativar um Ambiente Virtual

```bash
# Criar (caso ainda não exista)
python -m venv venv

# Ativar
# Windows:
.\venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

---

### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

---

### 5. Configurar Conexão com Banco de Dados

Edite o arquivo de configuração (por exemplo, `config.py` ou `.env`) e informe:

```env
DB_HOST=<seu_host_mysql>
DB_USER=<seu_usuario>
DB_PASS=<sua_senha>
DB_NAME=<nome_do_banco>
JWT_SECRET=<chave_secreta_para_JWT>
```

---

### 6. Executar a Aplicação

```bash
python main.py
```

O servidor iniciará em um endereço exibido no terminal (ex: `http://127.0.0.1:5000/`).  
Copie-o e cole no navegador para acessar o SGL.

---

## 🤝 Contribuições

Contribuições são sempre bem‑vindas!

1. Faça um _fork_ deste repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`)
3. Dê _commit_ às suas alterações (`git commit -m "Descrição da feature"`)
4. Faça _push_ para a branch (`git push origin feature/nome-da-feature`)
5. Abra um _Pull Request_

Para relatar bugs ou sugerir melhorias, abra uma _issue_ neste repositório.

---

© 2025 UFC Sobral – Bloco das Engenharias
