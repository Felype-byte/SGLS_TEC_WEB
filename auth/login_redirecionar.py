from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user

login_redirecionar_bp = Blueprint("login_redirecionar", __name__)

@login_redirecionar_bp.route("/login", methods=["GET"])
def tela_login():
    return render_template("login.html")

@login_redirecionar_bp.route("/pos-login")
def redirecionar_pos_login():
    tipo = current_user.tipo_usuario  # 🔐 Usando o Flask-Login

    if tipo == "Aluno":
        return redirect(url_for("aluno.agendamento_aluno"))
    elif tipo == "Professor":
        return redirect(url_for("professor.agendamento_professor"))
    elif tipo == "Tecnico":
        return redirect(url_for("dashboard_tecnico"))

    return redirect(url_for("login_redirecionar.tela_login"))
