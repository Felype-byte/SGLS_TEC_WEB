from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.solicitacao import Solicitacao
from app.models.horario import Horario
from app.models.sala_laboratorio import SalaLaboratorio
from app.models.professor.professor import Professor
from datetime import datetime

agendamento_aluno_bp = Blueprint('aluno', __name__)

@agendamento_aluno_bp.route('/dashboard/aluno', methods=['GET', 'POST'])
@login_required
def agendamento_aluno():
    if current_user.tipo_usuario != 'Aluno' or not current_user.aluno:
        return "Acesso negado.", 403

    salas = SalaLaboratorio.query.order_by(SalaLaboratorio.nome_sala.asc()).all()
    professores = Professor.query.order_by(Professor.nome_completo.asc()).all()

    solicitacoes = (
        Solicitacao.query
        .filter_by(id_aluno=current_user.aluno.id_aluno)
        .order_by(Solicitacao.data_solicitacao.desc())
        .all()
    )

    if request.method == 'POST':
        sala_id       = request.form.get('sala_id')
        data          = request.form.get('data')
        horario_id    = request.form.get('horario_id')
        justificativa = request.form.get('justificativa')
        professor_id  = request.form.get('professor_id')

        if not all([sala_id, data, horario_id, professor_id]):
            flash('Preencha todos os campos obrigatórios!', 'danger')
            return redirect(url_for('aluno.agendamento_aluno'))

        horario = Horario.query.filter_by(
            id_horarios=horario_id,
            id_sala=sala_id,
            data=data
        ).first()

        if not horario or horario.status != 'Disponível':
            flash('Horário selecionado não está disponível.', 'warning')
            return redirect(url_for('aluno.agendamento_aluno'))

        nova = Solicitacao(
            id_usuario_criador=current_user.id_usuarios,
            id_aluno=current_user.aluno.id_aluno,
            id_professor=professor_id,
            id_sala=sala_id,
            id_horarios=horario_id,
            data_agendada=data,
            justificativa=justificativa,
            status='Pendente Professor'
        )
        db.session.add(nova)

        horario.status = 'Ocupado'
        db.session.commit()

        flash('Agendamento solicitado com sucesso! ✅', 'success')
        return redirect(url_for('aluno.agendamento_aluno'))

    return render_template(
        'dashboard/aluno_dashboard.html',
        salas=salas,
        professores=professores,
        solicitacoes=solicitacoes
    )


@agendamento_aluno_bp.route('/dashboard/aluno/horarios')
@login_required
def horarios_disponiveis():
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


@agendamento_aluno_bp.route('/dashboard/aluno/cancelar/<int:solicitacao_id>', methods=['POST'])
@login_required
def cancelar_agendamento(solicitacao_id):
    if current_user.tipo_usuario != 'Aluno' or not current_user.aluno:
        return "Acesso negado.", 403

    solicitacao = Solicitacao.query.get_or_404(solicitacao_id)

    if solicitacao.id_aluno != current_user.aluno.id_aluno:
        flash('Você não pode cancelar esta solicitação.', 'danger')
        return redirect(url_for('aluno.agendamento_aluno'))

    solicitacao.status = 'Cancelado pelo aluno'

    horario = Horario.query.get(solicitacao.id_horarios)
    if horario:
        horario.status = 'Disponível'

    db.session.commit()
    flash('Seu agendamento foi cancelado.', 'info')
    return redirect(url_for('aluno.agendamento_aluno'))
