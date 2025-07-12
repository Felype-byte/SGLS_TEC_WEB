from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.solicitacao import Solicitacao
from app.models.horario import Horario
from app.models.sala_laboratorio import SalaLaboratorio
from datetime import datetime

agendamento_professor_bp = Blueprint('professor', __name__)


# 📌 Rota principal do painel do professor
@agendamento_professor_bp.route('/dashboard/professor', methods=['GET', 'POST'])
@login_required
def agendamento_professor():
    if current_user.tipo_usuario != 'Professor' or not current_user.professor:
        return "Acesso negado.", 403

    salas = SalaLaboratorio.query.order_by(SalaLaboratorio.nome_sala.asc()).all()

    # 👤 Solicitações feitas por este professor
    solicitacoes = (
        Solicitacao.query
        .filter_by(id_usuario_criador=current_user.id_usuarios)
        .order_by(Solicitacao.data_solicitacao.desc())
        .all()
    )

    # 📥 Solicitações de alunos pendentes de análise por este professor
    solicitacoes_pendentes = (
        Solicitacao.query
        .filter_by(id_professor=current_user.professor.id_professor, status='Pendente Professor')
        .order_by(Solicitacao.data_solicitacao.desc())
        .all()
    )

    # 📝 Submissão de nova solicitação pelo professor
    if request.method == 'POST':
        sala_id       = request.form.get('sala_id')
        data          = request.form.get('data')
        horario_id    = request.form.get('horario_id')
        justificativa = request.form.get('justificativa')

        if not all([sala_id, data, horario_id]):
            flash('Preencha todos os campos obrigatórios!', 'danger')
            return redirect(url_for('professor.agendamento_professor'))

        horario = Horario.query.filter_by(
            id_horarios=horario_id,
            id_sala=sala_id,
            data=data
        ).first()

        if not horario or horario.status != 'Disponível':
            flash('Horário selecionado não está disponível.', 'warning')
            return redirect(url_for('professor.agendamento_professor'))

        nova = Solicitacao(
            id_usuario_criador=current_user.id_usuarios,
            id_professor=current_user.professor.id_professor,
            id_sala=sala_id,
            id_horarios=horario_id,
            data_agendada=data,
            justificativa=justificativa,
            status='Pendente Tecnico'
        )
        db.session.add(nova)

        horario.status = 'Ocupado'
        db.session.commit()

        flash('Solicitação registrada com sucesso! ✅', 'success')
        return redirect(url_for('professor.agendamento_professor'))

    return render_template(
        'dashboard/professor_dashboard.html',
        salas=salas,
        solicitacoes=solicitacoes,
        solicitacoes_pendentes=solicitacoes_pendentes
    )


# 📅 Consulta de horários disponíveis
@agendamento_professor_bp.route('/dashboard/professor/horarios')
@login_required
def horarios_disponiveis_professor():
    sala_id = request.args.get('sala_id')
    data    = request.args.get('data')

    if not sala_id or not data:
        return jsonify([])

    horarios = (
        Horario.query
        .filter_by(id_sala=sala_id, data=data)
        .order_by(Horario.hora_inicio.asc())
        .all()
    )

    retorno = []
    for h in horarios:
        solicitacao = (
            Solicitacao.query
            .filter_by(id_horarios=h.id_horarios)
            .order_by(Solicitacao.id_solicitacao.desc())
            .first()
        )

        if h.status == 'Disponível':
            status_visual = 'Disponível'
        elif solicitacao and solicitacao.status in ['Pendente Professor', 'Pendente Tecnico']:
            status_visual = 'Em processo'
        elif solicitacao and solicitacao.status == 'Agendado':
            status_visual = 'Agendado'
        else:
            status_visual = 'Reservado'

        retorno.append({
            "id": h.id_horarios,
            "texto": f"{h.hora_inicio.strftime('%H:%M')} às {h.hora_fim.strftime('%H:%M')}",
            "status": status_visual
        })

    return jsonify(retorno)


# ✅ Aprovar solicitação de aluno (pelo professor)
@agendamento_professor_bp.route('/dashboard/professor/aprovar/<int:id>', methods=['POST'])
@login_required
def aprovar_solicitacao(id):
    if current_user.tipo_usuario != 'Professor' or not current_user.professor:
        return "Acesso negado.", 403

    solicitacao = Solicitacao.query.get_or_404(id)

    if solicitacao.id_professor != current_user.professor.id_professor:
        flash('Você não pode aprovar esta solicitação.', 'danger')
        return redirect(url_for('professor.agendamento_professor'))

    solicitacao.status = 'Pendente Tecnico'
    db.session.commit()

    flash('Solicitação aprovada. Agora será analisada pelo técnico. ✅', 'success')
    return redirect(url_for('professor.agendamento_professor'))


# ❌ Recusar solicitação de aluno
@agendamento_professor_bp.route('/dashboard/professor/recusar/<int:id>', methods=['POST'])
@login_required
def recusar_solicitacao(id):
    if current_user.tipo_usuario != 'Professor' or not current_user.professor:
        return "Acesso negado.", 403

    solicitacao = Solicitacao.query.get_or_404(id)

    if solicitacao.id_professor != current_user.professor.id_professor:
        flash('Você não pode recusar esta solicitação.', 'danger')
        return redirect(url_for('professor.agendamento_professor'))

    solicitacao.status = 'Negado Professor'

    horario = Horario.query.get(solicitacao.id_horarios)
    if horario:
        horario.status = 'Disponível'

    db.session.commit()
    flash('Solicitação recusada. Horário liberado. ❌', 'info')
    return redirect(url_for('professor.agendamento_professor'))


# ❎ Cancelar solicitação criada pelo próprio professor
@agendamento_professor_bp.route('/dashboard/professor/cancelar/<int:id>', methods=['POST'])
@login_required
def cancelar_solicitacao(id):
    if current_user.tipo_usuario != 'Professor' or not current_user.professor:
        return "Acesso negado.", 403

    solicitacao = Solicitacao.query.get_or_404(id)

    # Somente o criador pode cancelar (o próprio professor)
    if solicitacao.id_usuario_criador != current_user.id_usuarios:
        flash('Você não pode cancelar esta solicitação.', 'danger')
        return redirect(url_for('professor.agendamento_professor'))

    solicitacao.status = 'Cancelado pelo professor'

    horario = Horario.query.get(solicitacao.id_horarios)
    if horario:
        horario.status = 'Disponível'

    db.session.commit()
    flash('Solicitação cancelada com sucesso. ❌', 'info')
    return redirect(url_for('professor.agendamento_professor'))
