from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user
from app.models.aluno import Aluno
from app.models.base.usuario import Usuario

login_aluno_bp = Blueprint("login_aluno", __name__)

@login_aluno_bp.route("/login/aluno", methods=["POST"])
def autenticar_aluno():
    matricula = request.form.get("matricula")
    senha = request.form.get("senha")

    aluno = Aluno.query.filter_by(matricula=matricula).first()
    usuario = aluno.usuario if aluno else None

    if not usuario or not check_password_hash(usuario.senha, senha):
        return render_template("login.html", erro_aluno="Credenciais inválidas")

    login_user(usuario)  # 🔐 Isso ativa o current_user global
    return redirect(url_for("login_redirecionar.redirecionar_pos_login"))
