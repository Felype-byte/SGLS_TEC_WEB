from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user
from app.models.professor import Professor
from app.models.base.usuario import Usuario

login_professor_bp = Blueprint("login_professor", __name__)

@login_professor_bp.route("/login/professor", methods=["POST"])
def autenticar_professor():
    siape = request.form.get("siape")
    senha = request.form.get("senha")

    professor = Professor.query.filter_by(siape=siape).first()
    usuario = professor.usuario if professor else None

    if not usuario or not check_password_hash(usuario.senha, senha):
        return render_template("login.html", erro_professor="Credenciais inválidas")

    login_user(usuario)  # 🔐 Isso ativa o current_user globalmente
    return redirect(url_for("login_redirecionar.redirecionar_pos_login"))
