from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash
from app.models.base.usuario import Usuario
from app.models.tecnico import Tecnico
from app.extensions import db  # Corrigido: deve vir do extensions

cadastro_tecnico_bp = Blueprint("cadastro_tecnico", __name__)

@cadastro_tecnico_bp.route("/cadastro/tecnico", methods=["GET"])
def tela_cadastro_tecnico():
    return render_template("cadastro/cadastro_tecnico.html")

@cadastro_tecnico_bp.route("/cadastro/tecnico", methods=["POST"])
def cadastrar_tecnico():
    nome     = request.form.get("nome", "").strip()
    siape    = request.form.get("siape", "").strip()
    email    = request.form.get("email", "").strip()
    senha    = request.form.get("senha", "")
    confirma = request.form.get("confirmaSenha", "")

    erros = []

    # 🔍 Validações básicas
    if not nome or not siape or not email or not senha or not confirma:
        erros.append("Preencha todos os campos obrigatórios.")

    if senha != confirma:
        erros.append("As senhas não coincidem.")

    if Tecnico.query.filter_by(siape=siape).first():
        erros.append("Já existe um técnico com esse número SIAPE.")

    if Usuario.query.filter_by(email=email).first():
        erros.append("Já existe um usuário com esse e-mail.")

    if erros:
        return render_template("cadastro/cadastro_tecnico.html", erros=erros)

    # 🚀 Persistência no banco
    try:
        novo_usuario = Usuario(
            email=email,
            senha=generate_password_hash(senha),
            tipo_usuario="Tecnico"
        )
        db.session.add(novo_usuario)
        db.session.flush()  # Garante id_usuarios disponível

        novo_tecnico = Tecnico(
            nome_completo=nome,
            siape=siape,
            id_usuario=novo_usuario.id_usuarios
        )
        db.session.add(novo_tecnico)
        db.session.commit()

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("login_redirecionar.tela_login"))

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Erro ao cadastrar técnico")
        erros.append("Erro interno no sistema. Nenhum dado foi salvo.")
        return render_template("cadastro/cadastro_tecnico.html", erros=erros)
