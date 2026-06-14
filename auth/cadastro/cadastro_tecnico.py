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

    # 🔍 1. Validações básicas de preenchimento
    if not nome or not siape or not email or not senha or not confirma:
        erros.append("Preencha todos os campos obrigatórios.")

    # 🔍 2. Validação do Formato do SIAPE (Apenas números)
    if "." in siape or "-" in siape:
        erros.append("O SIAPE deve ser digitado apenas com números (sem pontos ou traços).")
    elif not siape.isdigit():
        erros.append("O SIAPE contém caracteres inválidos. Digite apenas números.")

    # 🔍 3. Validação da Senha
    if senha != confirma:
        erros.append("As senhas digitadas não coincidem.")

    # 🔍 4. Validações de Duplicidade no Banco de Dados
    if Tecnico.query.filter_by(siape=siape).first():
        erros.append(f"O SIAPE {siape} já está vinculado a outro técnico.")

    if Usuario.query.filter_by(email=email).first():
        erros.append("O e-mail informado já está em uso por outro usuário.")

    # Se a lista tiver qualquer erro, devolve a página mostrando os motivos exatos
    if erros:
        return render_template("cadastro/cadastro_tecnico.html", erros=erros)

    # 🚀 5. Persistência no banco
    try:
        novo_usuario = Usuario(
            email=email,
            senha=generate_password_hash(senha),
            tipo_usuario="Tecnico" # Mantido sem acento para padronização no banco
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
        # Se cair neste erro, é um problema real no servidor
        erros.append("Erro interno no servidor ao tentar salvar. Tente novamente mais tarde.")
        return render_template("cadastro/cadastro_tecnico.html", erros=erros)
