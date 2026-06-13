from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models.base.usuario import Usuario
from app.models.aluno.aluno import Aluno

cadastro_aluno_bp = Blueprint("cadastro_aluno", __name__)

@cadastro_aluno_bp.route("/cadastro/aluno", methods=["GET"])
def tela_cadastro_aluno():
    return render_template("cadastro/cadastro_aluno.html")

@cadastro_aluno_bp.route("/cadastro/aluno", methods=["POST"])
def cadastrar_aluno():
    nome            = request.form.get("nome", "").strip()
    matricula       = request.form.get("matricula", "").strip()
    email           = request.form.get("email", "").strip()
    curso           = request.form.get("curso", "").strip()
    turma_monitoria = request.form.get("turma_monitoria", "").strip()
    cpf             = request.form.get("cpf", "").strip()
    senha           = request.form.get("senha", "")
    confirma        = request.form.get("confirmaSenha", "")

    erros = []

    # 🔍 1. Validações básicas de preenchimento
    if not nome or not matricula or not email or not curso or not cpf or not senha or not confirma:
        erros.append("Preencha todos os campos obrigatórios.")

    # 🔍 2. Validação do Formato do CPF (Apenas números)
    if "." in cpf or "-" in cpf:
        erros.append("O CPF deve ser digitado apenas com números (sem pontos ou traços).")
    elif not cpf.isdigit():
        erros.append("O CPF contém caracteres inválidos. Digite apenas números.")
    elif len(cpf) != 11:
        erros.append("O CPF deve conter exatamente 11 números.")

    # 🔍 3. Validação da Senha
    if senha != confirma:
        erros.append("As senhas digitadas não coincidem.")

    # 🔍 4. Validações de Duplicidade no Banco de Dados
    if Aluno.query.filter_by(matricula=matricula).first():
        erros.append(f"A matrícula {matricula} já está vinculada a outro aluno.")

    if Aluno.query.filter_by(cpf=cpf).first():
        erros.append("Este CPF já possui cadastro no sistema.")

    if Usuario.query.filter_by(email=email).first():
        erros.append("O e-mail informado já está em uso por outro usuário.")

    # Se a lista tiver qualquer erro das verificações acima, devolve a página mostrando os motivos
    if erros:
        return render_template("cadastro/cadastro_aluno.html", erros=erros)

    # 🚀 5. Persistência no banco (Só chega aqui se os dados estiverem 100% corretos)
    try:
        novo_usuario = Usuario(
            email=email,
            senha=generate_password_hash(senha),
            tipo_usuario="Aluno"
        )
        db.session.add(novo_usuario)
        db.session.flush()  # Gera novo_usuario.id_usuarios

        novo_aluno = Aluno(
            nome_completo   = nome,
            matricula       = matricula,
            curso           = curso,
            turma_monitoria = turma_monitoria,
            cpf             = cpf,
            id_usuario      = novo_usuario.id_usuarios
        )
        db.session.add(novo_aluno)
        db.session.commit()

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("login_redirecionar.tela_login"))

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Erro ao cadastrar aluno")
        # Se cair neste erro, é um problema de conexão com o banco ou falha no servidor
        erros.append("Erro interno no servidor ao tentar salvar. Tente novamente mais tarde.")
        return render_template("cadastro/cadastro_aluno.html", erros=erros)