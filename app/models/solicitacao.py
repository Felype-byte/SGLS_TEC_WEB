from app.extensions import db

class Solicitacao(db.Model):
    __tablename__ = 'solicitacoes'

    id_solicitacao = db.Column(db.Integer, primary_key=True)

    # Autor da solicitação
    id_usuario_criador = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuarios'), nullable=False)

    # Participantes
    id_aluno     = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=True)
    id_professor = db.Column(db.Integer, db.ForeignKey('professores.id_professor'), nullable=True)
    id_tecnico   = db.Column(db.Integer, db.ForeignKey('tecnicos.id_tecnico'), nullable=True)

    # Dados do agendamento
    id_sala     = db.Column(db.Integer, db.ForeignKey('salaslaboratorio.id_sala'), nullable=False)
    id_horarios = db.Column(db.Integer, db.ForeignKey('horarios.id_horarios'),    nullable=False)

    data_solicitacao = db.Column(db.DateTime, default=db.func.now())
    data_agendada    = db.Column(db.Date,     nullable=False)
    justificativa    = db.Column(db.Text)
    status           = db.Column(db.String(30), default='Pendente Professor')

    parecer_professor     = db.Column(db.Text)
    data_parecer_professor = db.Column(db.DateTime)

    parecer_tecnico      = db.Column(db.Text)
    data_parecer_tecnico = db.Column(db.DateTime)

    # Relacionamentos bidirecionais
    usuario_criador = db.relationship('Usuario', back_populates='solicitacoes_criadas')
    aluno           = db.relationship('Aluno', back_populates='solicitacoes')
    professor       = db.relationship('Professor', back_populates='solicitacoes')
    tecnico         = db.relationship('Tecnico', back_populates='solicitacoes')
    sala            = db.relationship('SalaLaboratorio', back_populates='solicitacoes')
    horario         = db.relationship('Horario', back_populates='solicitacoes')

    def __repr__(self):
        return f'<Solicitacao #{self.id_solicitacao} – Sala {self.id_sala} – Horário {self.id_horarios}>'
