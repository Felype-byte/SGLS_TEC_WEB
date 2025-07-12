from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash
from app.models.base.usuario import Usuario
from app.models.professor import Professor
from app.extensions import db  # corrigido: vem de extensions, não de solicitacao

cadastro_professor_bp = Blueprint("cadastro_professor", __name__)

@cadastro_professor_bp.route("/cadastro/professor", methods=["GET"])
def tela_cadastro_professor():
    return render_template("cadastro/cadastro_professor.html")

@cadastro_professor_bp.route("/cadastro/professor", methods=["POST"])
def cadastrar_professor():
    nome         = request.form.get("nome", "").strip()
    departamento = request.form.get("departamento", "").strip()
    curso        = request.form.get("curso", "").strip()
    siape        = request.form.get("siape", "").strip()
    email        = request.form.get("email", "").strip()
    senha        = request.form.get("senha", "")
    confirma     = request.form.get("confirmaSenha", "")

    erros = []

    if not nome or not departamento or not curso or not siape or not email or not senha or not confirma:
        erros.append("Preencha todos os campos obrigatórios.")

    if senha != confirma:
        erros.append("As senhas não coincidem.")

    if Professor.query.filter_by(siape=siape).first():
        erros.append("Já existe um professor com esse número SIAPE.")

    if Usuario.query.filter_by(email=email).first():
        erros.append("Já existe um usuário com esse e-mail.")

    if erros:
        return render_template("cadastro/cadastro_professor.html", erros=erros)

    try:
        novo_usuario = Usuario(
            email=email,
            senha=generate_password_hash(senha),
            tipo_usuario="Professor"
        )
        db.session.add(novo_usuario)
        db.session.flush()  # garante que novo_usuario.id_usuarios está disponível

        novo_professor = Professor(
            nome_completo=nome,
            departamento=departamento,
            curso=curso,
            siape=siape,
            id_usuario=novo_usuario.id_usuarios
        )
        db.session.add(novo_professor)
        db.session.commit()

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("login_redirecionar.tela_login"))

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Erro ao cadastrar professor")
        erros.append("Erro interno no sistema. Nenhum dado foi salvo.")
        return render_template("cadastro/cadastro_professor.html", erros=erros)
