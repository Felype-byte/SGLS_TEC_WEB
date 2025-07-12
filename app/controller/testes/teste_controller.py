from flask import Blueprint, render_template
from app.models.professor import Professor

teste_bp = Blueprint("teste", __name__)

@teste_bp.route("/debug/professores")
def teste_professores():
    professores = Professor.query.order_by(Professor.nome_completo).all()
    return render_template("testes/teste_selecao_professores.html", professores=professores)
