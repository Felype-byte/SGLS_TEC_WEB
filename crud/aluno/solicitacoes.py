from app.models.solicitacao import Solicitacao
from app.models.horario import Horario
from app.models.sala_laboratorio import SalaLaboratorio
from app.extensions import db
from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import current_user
from datetime import datetime

# 🚀 Criar nova solicitação
def criar_solicitacao(id_aluno, id_sala, id_horarios, justificativa, data_agendada, status="Aguardando"):
    nova = Solicitacao(
        id_aluno=id_aluno,
        id_sala=id_sala,
        id_horarios=id_horarios,
        justificativa=justificativa,
        status=status,
        data_agendada=data_agendada,
        data_solicitacao=datetime.utcnow()
    )
    db.session.add(nova)
    db.session.commit()
    return nova

# 📋 Listar todas as solicitações feitas por um aluno
def listar_solicitacoes_por_aluno(id_aluno):
    return (Solicitacao.query
            .filter_by(id_aluno=id_aluno)
            .order_by(Solicitacao.data_solicitacao.desc())
            .all())

# 📘 Histórico completo de agendamentos
def historico_agendamentos_aluno(id_aluno):
    return (Solicitacao.query
            .filter_by(id_aluno=id_aluno)
            .join(Solicitacao.horario)
            .join(Solicitacao.sala)
            .order_by(Solicitacao.data_agendada.asc())
            .all())

# 🗑️ Cancelar solicitação
def cancelar_solicitacao(id_solicitacao, id_aluno):
    solicitacao = Solicitacao.query.get_or_404(id_solicitacao)
    if solicitacao.id_aluno != id_aluno:
        return None  # não autorizado
    if "Aguardando" in solicitacao.status:
        db.session.delete(solicitacao)
        db.session.commit()
        return True
    return False

# 🧭 Dados para exibição no painel do aluno
def montar_contexto_painel():
    salas = SalaLaboratorio.query.order_by(SalaLaboratorio.nome_sala).all()
    horarios_disponiveis = Horario.query.order_by(Horario.data.asc(), Horario.hora_inicio.asc()).all()
    solicitacoes = listar_solicitacoes_por_aluno(current_user.id)
    return salas, horarios_disponiveis, solicitacoes

# 🔍 Buscar horários para uma sala e data (JSON)
def buscar_horarios_json():
    data = request.args.get("data")
    sala_id = request.args.get("sala_id")

    if not data or not sala_id:
        return []

    horarios = (Horario.query
        .filter_by(id_sala=sala_id)
        .filter(Horario.data == data)
        .order_by(Horario.hora_inicio.asc())
        .all())

    return [
        {
            "id": h.id_horarios,
            "texto": h.texto,
            "status": h.status
        } for h in horarios
    ]

# 📆 Consulta direta via formulário
def consultar_horarios_por_form():
    horarios_disponiveis = []
    sala_id = None
    data_selecionada = None
    salas = SalaLaboratorio.query.order_by(SalaLaboratorio.nome_sala).all()

    if request.method == "POST":
        sala_id = request.form.get("sala_id")
        data_selecionada = request.form.get("data")

        if sala_id and data_selecionada:
            horarios_disponiveis = (Horario.query
                .filter_by(id_sala=sala_id)
                .filter(Horario.data == data_selecionada)
                .order_by(Horario.hora_inicio.asc())
                .all())
        else:
            flash("Por favor, selecione uma sala e uma data.", "warning")

    return salas, sala_id, data_selecionada, horarios_disponiveis

