from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user
from app.models.tecnico import Tecnico
from app.models.base.usuario import Usuario

login_tecnico_bp = Blueprint("login_tecnico", __name__)

@login_tecnico_bp.route("/login/tecnico", methods=["POST"])
def autenticar_tecnico():
    siape = request.form.get("siape")
    senha = request.form.get("senha")

    tecnico = Tecnico.query.filter_by(siape=siape).first()
    usuario = tecnico.usuario if tecnico else None

    if not usuario or not check_password_hash(usuario.senha, senha):
        return render_template("login.html", erro_tecnico="Credenciais inválidas")

    login_user(usuario)  # 🔐 Isso ativa o current_user global
    return redirect(url_for("login_redirecionar.redirecionar_pos_login"))
