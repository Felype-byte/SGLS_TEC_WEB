from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.solicitacao import Solicitacao
from app.models.horario import Horario
from app.models.sala_laboratorio import SalaLaboratorio
from datetime import datetime, timedelta
from sqlalchemy import distinct

agendamento_tecnico_bp = Blueprint('tecnico', __name__)

# 📋 Painel principal
@agendamento_tecnico_bp.route('/dashboard/tecnico')
@login_required
def agendamento_tecnico():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    solicitacoes_pendentes = (
        Solicitacao.query
        .filter_by(status='Pendente Tecnico')
        .order_by(Solicitacao.data_solicitacao.desc())
        .all()
    )

    solicitacoes_todas = (
        Solicitacao.query
        .filter(Solicitacao.status.in_([
            'Pendente Tecnico', 'Agendado', 'Negado Tecnico'
        ]))
        .order_by(Solicitacao.data_solicitacao.desc())
        .all()
    )

    salas = SalaLaboratorio.query.order_by(SalaLaboratorio.nome_sala.asc()).all()
    horarios = Horario.query.order_by(Horario.data.desc(), Horario.hora_inicio.asc()).limit(50).all()

    return render_template(
        'dashboard/tecnico_dashboard.html',
        solicitacoes_pendentes=solicitacoes_pendentes,
        solicitacoes_todas=solicitacoes_todas,
        salas=salas,
        horarios=horarios
    )

# ✅ Aprovar solicitação
@agendamento_tecnico_bp.route('/dashboard/tecnico/aprovar/<int:id>', methods=['POST'])
@login_required
def aprovar_tecnico(id):
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    solicitacao = Solicitacao.query.get_or_404(id)

    if solicitacao.status == 'Pendente Tecnico':
        solicitacao.status = 'Agendado'
        db.session.commit()
        flash('Solicitação aprovada com sucesso! ✅', 'success')
    else:
        flash('Solicitação não está pendente de aprovação técnica.', 'warning')

    return redirect(url_for('tecnico.agendamento_tecnico'))

# ❌ Recusar solicitação
@agendamento_tecnico_bp.route('/dashboard/tecnico/recusar/<int:id>', methods=['POST'])
@login_required
def recusar_tecnico(id):
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    solicitacao = Solicitacao.query.get_or_404(id)

    if solicitacao.status == 'Pendente Tecnico':
        solicitacao.status = 'Negado Tecnico'
        horario = Horario.query.get(solicitacao.id_horarios)
        if horario:
            horario.status = 'Disponível'
        db.session.commit()
        flash('Solicitação recusada pelo técnico. ❌', 'info')
    else:
        flash('Solicitação não está pendente.', 'warning')

    return redirect(url_for('tecnico.agendamento_tecnico'))

# 🏛️ Criar nova sala
@agendamento_tecnico_bp.route('/dashboard/tecnico/sala/nova', methods=['POST'])
@login_required
def criar_sala():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    nome = request.form.get('nome_sala')
    numero = request.form.get('numero_sala')
    bloco = request.form.get('bloco')

    if not all([nome, numero, bloco]):
        flash('Preencha todos os campos da sala.', 'danger')
    else:
        nova = SalaLaboratorio(nome_sala=nome, numero_sala=numero, bloco=bloco)
        db.session.add(nova)
        db.session.commit()
        flash('Sala criada com sucesso. ✅', 'success')

    return redirect(url_for('tecnico.agendamento_tecnico'))

# ✏️ Editar sala
@agendamento_tecnico_bp.route('/dashboard/tecnico/sala/editar/<int:id>', methods=['POST'])
@login_required
def editar_sala(id):
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    sala = SalaLaboratorio.query.get_or_404(id)
    sala.nome_sala = request.form.get('nome_sala')
    sala.numero_sala = request.form.get('numero_sala')
    sala.bloco = request.form.get('bloco')

    db.session.commit()
    flash('Sala atualizada. ✏️', 'info')
    return redirect(url_for('tecnico.agendamento_tecnico'))

# 🗑️ Excluir sala
@agendamento_tecnico_bp.route('/dashboard/tecnico/sala/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_sala(id):
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    sala = SalaLaboratorio.query.get_or_404(id)
    db.session.delete(sala)
    db.session.commit()
    flash('Sala excluída permanentemente. 🗑️', 'warning')
    return redirect(url_for('tecnico.agendamento_tecnico'))

# ⏱️ Inserir blocos fixos de horários por intervalo
@agendamento_tecnico_bp.route('/dashboard/tecnico/horarios/inserir_bloco', methods=['POST'])
@login_required
def inserir_blocos_de_horarios():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    sala_id      = request.form.get('sala_id')
    data_inicio  = request.form.get('data_inicio')
    data_fim     = request.form.get('data_fim')

    if not sala_id or not data_inicio or not data_fim:
        flash('Informe sala e intervalo de datas.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    try:
        d_ini = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        d_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
    except:
        flash('Formato de data inválido.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    blocos = [
        ('08:00:00', '10:00:00'),
        ('10:00:00', '12:00:00'),
        ('13:30:00', '15:30:00'),
        ('15:30:00', '17:30:00'),
        ('18:30:00', '20:30:00'),
        ('20:30:00', '22:00:00'),
    ]

    dia = d_ini
    while dia <= d_fim:
        if dia.weekday() < 5:
            for inicio, fim in blocos:
                novo = Horario(
                    id_sala=sala_id,
                    data=dia,
                    hora_inicio=datetime.strptime(inicio, '%H:%M:%S').time(),
                    hora_fim=datetime.strptime(fim, '%H:%M:%S').time(),
                    status='Disponível'
                )
                db.session.add(novo)
        dia += timedelta(days=1)

    db.session.commit()
    flash('Blocos de horários inseridos para o intervalo selecionado! ✅', 'success')
    return redirect(url_for('tecnico.agendamento_tecnico'))

@agendamento_tecnico_bp.route('/dashboard/tecnico/horarios/inserir_blocos_personalizados', methods=['POST'])
@login_required
def inserir_blocos_personalizados():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    sala_id       = request.form.get('sala_id')
    data_inicio   = request.form.get('data_inicio')
    data_fim      = request.form.get('data_fim')
    hora_inicio   = request.form.get('hora_inicio')
    hora_fim      = request.form.get('hora_fim')

    if not sala_id or not data_inicio or not data_fim or not hora_inicio or not hora_fim:
        flash('Preencha todos os campos para adicionar horário personalizado.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    try:
        d_ini  = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        d_fim  = datetime.strptime(data_fim, '%Y-%m-%d').date()
        h_ini  = datetime.strptime(hora_inicio, '%H:%M').time()
        h_fim  = datetime.strptime(hora_fim, '%H:%M').time()
        if h_ini >= h_fim:
            raise ValueError('Hora de início deve ser menor que a hora de fim.')
    except Exception as e:
        flash(f'Erro ao processar datas ou horários: {e}', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    total_criados = 0
    dia = d_ini
    while dia <= d_fim:
        if dia.weekday() < 5:  # Apenas dias úteis
            novo = Horario(
                id_sala=sala_id,
                data=dia,
                hora_inicio=h_ini,
                hora_fim=h_fim,
                status='Disponível'
            )
            db.session.add(novo)
            total_criados += 1
        dia += timedelta(days=1)

    db.session.commit()

    flash(f'{total_criados} horário(s) personalizado(s) inserido(s).', 'success')

    # Se o intervalo foi um único dia, redireciona para a visualização da data
    if data_inicio == data_fim:
        return redirect(url_for(
            'tecnico.visualizar_horarios_por_data',
            sala_id=sala_id,
            data=data_inicio
        ))

    # Caso contrário, vai pro painel
    return redirect(url_for('tecnico.agendamento_tecnico'))

# remoer um horario especifico 
# 🗑️ Excluir um horário específico (data + início + fim + sala)
@agendamento_tecnico_bp.route('/dashboard/tecnico/horarios/excluir', methods=['POST'])
@login_required
def excluir_horario_personalizado():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    sala_id     = request.form.get('sala_id')
    data        = request.form.get('data')
    hora_inicio = request.form.get('hora_inicio')
    hora_fim    = request.form.get('hora_fim')

    if not sala_id or not data or not hora_inicio or not hora_fim:
        flash('Dados incompletos para excluir o horário.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    try:
        dia   = datetime.strptime(data, '%Y-%m-%d').date()
        h_ini = datetime.strptime(hora_inicio, '%H:%M').time()
        h_fim = datetime.strptime(hora_fim,    '%H:%M').time()
    except ValueError as e:
        flash(f'Erro ao interpretar data ou horário: {e}', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    # Buscar o horário específico e excluir
    horario = (
        Horario.query.filter_by(
            id_sala=sala_id,
            data=dia,
            hora_inicio=h_ini,
            hora_fim=h_fim
        ).first()
    )

    if horario:
        db.session.delete(horario)
        db.session.commit()
        flash('Horário removido com sucesso! 🗑️', 'success')
    else:
        flash('Horário não encontrado para exclusão.', 'warning')

    # Redirecionar de volta para a mesma data e sala
    return redirect(url_for(
        'tecnico.visualizar_horarios_por_data',
        sala_id=sala_id,
        data=data
    ))


# 🗑️ Remover todos horários de um intervalo
@agendamento_tecnico_bp.route('/dashboard/tecnico/horarios/deletar_bloco', methods=['POST'])
@login_required
def deletar_blocos_horarios():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    sala_id      = request.form.get('sala_id')
    data_inicio  = request.form.get('data_inicio')
    data_fim     = request.form.get('data_fim')

    if not sala_id or not data_inicio or not data_fim:
        flash('Informe sala e intervalo de datas.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    try:
        d_ini = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        d_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
    except:
        flash('Formato de data inválido.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    excluidos = 0
    dia = d_ini
    while dia <= d_fim:
        if dia.weekday() < 5:
            excluidos += Horario.query.filter_by(id_sala=sala_id, data=dia).delete()
        dia += timedelta(days=1)

    db.session.commit()
    flash(f'{excluidos} horários removidos no intervalo. 🗑️', 'warning')
    return redirect(url_for('tecnico.agendamento_tecnico'))

@agendamento_tecnico_bp.route('/dashboard/tecnico/horarios/visualizar', methods=['GET', 'POST'])
@login_required
def visualizar_horarios_por_data():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    sala_id  = request.form.get('sala_id') or request.args.get('sala_id')
    data_dia = request.form.get('data')    or request.args.get('data')

    if not sala_id or not data_dia:
        flash('Selecione uma sala e uma data para visualizar os horários.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    try:
        d = datetime.strptime(data_dia, '%Y-%m-%d').date()
    except ValueError:
        flash('Formato de data inválido.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    horarios = Horario.query.filter_by(id_sala=sala_id, data=d).order_by(Horario.hora_inicio).all()
    sala = SalaLaboratorio.query.get(sala_id)

    # Mesmo que não haja horários, mantemos a visualização da página
    return render_template(
        'dashboard/horarios_por_data.html',
        horarios=horarios,
        sala=sala,
        data_escolhida=d
    )

# 📑 Inserir horários selecionados em intervalo (apenas dias úteis)
@agendamento_tecnico_bp.route(
    '/dashboard/tecnico/horarios/inserir_selecionados',
    methods=['POST']
)
@login_required
def inserir_horarios_selecionados():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    sala_id      = request.form.get('sala_id')
    data_inicio  = request.form.get('data_inicio')
    data_fim     = request.form.get('data_fim')
    nome_bloco   = request.form.get('nome_bloco') or None
    h_inicio_lst = request.form.getlist('hora_inicio')  # ex: ['08:00','10:00']
    h_fim_lst    = request.form.getlist('hora_fim')     # ex: ['10:00','12:00']

    # validação básica
    if not sala_id or not data_inicio or not data_fim \
       or not h_inicio_lst or not h_fim_lst \
       or len(h_inicio_lst) != len(h_fim_lst):
        flash('Preencha sala, intervalo de datas e todos os horários corretamente.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    try:
        d_ini = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        d_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        # converter strings em time
        slots = []
        for hi, hf in zip(h_inicio_lst, h_fim_lst):
            t_ini = datetime.strptime(hi, '%H:%M').time()
            t_fim = datetime.strptime(hf, '%H:%M').time()
            if t_ini >= t_fim:
                raise ValueError('Hora início deve ser menor que fim.')
            slots.append((t_ini, t_fim))
    except ValueError as e:
        flash(f'Erro no formato de data/hora: {e}', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    # inserir apenas em dias úteis
    dia = d_ini
    criado = 0
    while dia <= d_fim:
        if dia.weekday() < 5:  # 0=segunda ... 4=sexta
            for t_ini, t_fim in slots:
                novo = Horario(
                    id_sala=sala_id,
                    data=dia,
                    hora_inicio=t_ini,
                    hora_fim=t_fim,
                    status='Disponível',
                    nome_bloco=nome_bloco  # 👈 aqui entra o nome do bloco
                )
                db.session.add(novo)
                criado += 1
        dia += timedelta(days=1)

    db.session.commit()
    flash(f'{criado} horário(s) inserido(s) com o nome "{nome_bloco or "sem rótulo"}" de {data_inicio} a {data_fim} (dias úteis).', 'success')
    return redirect(url_for('tecnico.agendamento_tecnico'))


@agendamento_tecnico_bp.route(
    '/dashboard/tecnico/horario/editar/<int:id>',
    methods=['POST']
)
@login_required
def editar_horario(id):
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    horario = Horario.query.get_or_404(id)
    hi_str  = request.form.get('hora_inicio')
    hf_str  = request.form.get('hora_fim')

    try:
        hi = datetime.strptime(hi_str, '%H:%M').time()
        hf = datetime.strptime(hf_str, '%H:%M').time()
        if hi >= hf:
            flash('Hora início deve ser menor que a hora fim.', 'warning')
            return redirect(request.referrer)
    except:
        flash('Formato de hora inválido.', 'danger')
        return redirect(request.referrer)

    horario.hora_inicio = hi
    horario.hora_fim    = hf
    db.session.commit()

    flash('Horário atualizado com sucesso! ✏️', 'success')
    return redirect(request.referrer)

@agendamento_tecnico_bp.route(
    '/dashboard/tecnico/horarios/deletar_selecionados',
    methods=['POST']
)
@login_required
def deletar_horarios_selecionados():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    ids = request.form.getlist('selecionados')  # lista de id_horarios
    if not ids:
        flash('Selecione ao menos um horário para excluir.', 'warning')
        return redirect(request.referrer)

    count = 0
    for hid in ids:
        h = Horario.query.get(hid)
        if h:
            db.session.delete(h)
            count += 1

    db.session.commit()
    flash(f'{count} horário(s) excluído(s) com sucesso! 🗑️', 'success')
    return redirect(request.referrer)

@agendamento_tecnico_bp.route(
    '/dashboard/tecnico/horarios/excluir_intervalo',
    methods=['POST']
)
@login_required
def excluir_horarios_intervalo():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    sala_id     = request.form.get('sala_id')
    data_inicio = request.form.get('data_inicio')
    data_fim    = request.form.get('data_fim')

    if not sala_id or not data_inicio or not data_fim:
        flash('Selecione sala e intervalo corretamente.', 'danger')
        return redirect(request.referrer)

    try:
        d_ini = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        d_fim = datetime.strptime(data_fim,    '%Y-%m-%d').date()
        if d_ini > d_fim:
            raise ValueError("Data início maior que data fim")
    except ValueError as e:
        flash(f'Erro no intervalo de datas: {e}', 'danger')
        return redirect(request.referrer)

    qtd = (
        Horario.query
        .filter(
            Horario.id_sala == sala_id,
            Horario.data >= d_ini,
            Horario.data <= d_fim
        )
        .delete(synchronize_session=False)
    )
    db.session.commit()

    flash(f'{qtd} horário(s) excluído(s) de {data_inicio} a {data_fim}.', 'success')
    return redirect(request.referrer)

@agendamento_tecnico_bp.route('/dashboard/tecnico/horarios/gerenciar_por_sala', methods=['GET'])
@login_required
def gerenciar_horarios_por_sala():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    sala_id = request.args.get('sala_id')

    if not sala_id:
        flash('Selecione uma sala para gerenciar seus horários.', 'warning')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    sala = SalaLaboratorio.query.get(sala_id)
    if not sala:
        flash('Sala não encontrada.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    # Agrupa todos os horários da sala por data
    horarios = (
        Horario.query
        .filter_by(id_sala=sala_id)
        .order_by(Horario.data, Horario.hora_inicio)
        .all()
    )

    return render_template(
        'dashboard/gerenciar_por_sala.html',
        sala=sala,
        horarios=horarios
    )
@agendamento_tecnico_bp.route('/dashboard/tecnico/horarios/buscar_intervalo', methods=['POST'])
@login_required
def buscar_horarios_por_intervalo():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    sala_id     = request.form.get('sala_id')
    data_inicio = request.form.get('data_inicio')
    data_fim    = request.form.get('data_fim')

    if not sala_id or not data_inicio or not data_fim:
        flash('Preencha todos os campos para buscar os horários.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    try:
        d_ini = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        d_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
    except:
        flash('Formato de data inválido.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    sala = SalaLaboratorio.query.get(sala_id)
    horarios = (
        Horario.query
        .filter(
            Horario.id_sala == sala_id,
            Horario.data >= d_ini,
            Horario.data <= d_fim
        )
        .order_by(Horario.data, Horario.hora_inicio)
        .all()
    )

    return render_template(
        'dashboard/horarios_intervalo.html',
        sala=sala,
        horarios=horarios,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

@agendamento_tecnico_bp.route(
    '/dashboard/tecnico/horarios/ver_por_sala',
    methods=['POST']
)
@login_required
def ver_horarios_por_sala():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    sala_id = request.form.get('sala_id')
    if not sala_id:
        flash('Selecione uma sala para visualizar os horários.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    sala = SalaLaboratorio.query.get(sala_id)
    if not sala:
        flash('Sala não encontrada.', 'danger')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    # Pega todos os nomes de bloco existentes (não-NONE) desta sala
    nomes = [n[0] for n in
        db.session.query(distinct(Horario.nome_bloco))
        .filter(
            Horario.id_sala == sala_id,
            Horario.nome_bloco.isnot(None)
        )
        .all()
    ]

    if not nomes:
        flash('Nenhum bloco de horários encontrado para esta sala.', 'info')
        return redirect(url_for('tecnico.agendamento_tecnico'))

    blocos_info = []
    for nome in nomes:
        hs = (
            Horario.query
            .filter_by(id_sala=sala_id, nome_bloco=nome)
            .order_by(Horario.data, Horario.hora_inicio)
            .all()
        )
        datas = [h.data for h in hs]
        blocos_info.append({
            'nome_bloco': nome,
            'data_min': min(datas).strftime('%Y-%m-%d'),
            'data_max': max(datas).strftime('%Y-%m-%d'),
            'horarios': hs
        })

    return render_template(
        'dashboard/ver_horarios_por_sala.html',
        sala=sala,
        blocos_info=blocos_info
    )


@agendamento_tecnico_bp.route(
    '/dashboard/tecnico/horarios/excluir_por_bloco',
    methods=['POST']
)
@login_required
def excluir_horarios_por_bloco():
    if current_user.tipo_usuario != 'Tecnico':
        return "Acesso negado.", 403

    sala_id    = request.form.get('sala_id')
    nome_bloco = request.form.get('nome_bloco')
    if not sala_id or not nome_bloco:
        flash('Dados incompletos para exclusão.', 'danger')
        return redirect(request.referrer or url_for('tecnico.agendamento_tecnico'))

    qtd = (
        Horario.query
        .filter_by(id_sala=sala_id, nome_bloco=nome_bloco)
        .delete()
    )
    db.session.commit()
    flash(f'{qtd} horário(s) do bloco "{nome_bloco}" excluído(s).', 'success')
    return redirect(url_for('tecnico.agendamento_tecnico'))