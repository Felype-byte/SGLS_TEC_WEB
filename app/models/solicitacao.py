from app.extensions import db

class Solicitacao(db.Model):
    __tablename__ = 'solicitacoes'

    id_solicitacao       = db.Column(db.Integer, primary_key=True)

    # autor da solicitação (aluno, professor ou técnico)
    id_usuario_criador   = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuarios'), nullable=False)

    # participantes envolvidos no fluxo
    id_aluno             = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'),         nullable=True)
    id_professor         = db.Column(db.Integer, db.ForeignKey('professores.id_professor'), nullable=True)
    id_tecnico           = db.Column(db.Integer, db.ForeignKey('tecnicos.id_tecnico'),     nullable=True)

    # dados do agendamento
    id_sala              = db.Column(db.Integer, db.ForeignKey('salaslaboratorio.id_sala'), nullable=False)
    id_horarios          = db.Column(db.Integer, db.ForeignKey('horarios.id_horarios'),    nullable=False)

    data_solicitacao     = db.Column(db.DateTime, default=db.func.now())
    data_agendada        = db.Column(db.Date,     nullable=False)
    justificativa        = db.Column(db.Text)
    status               = db.Column(db.String(30), default='Pendente Professor')

    parecer_professor    = db.Column(db.Text)
    data_parecer_professor = db.Column(db.DateTime)

    parecer_tecnico      = db.Column(db.Text)
    data_parecer_tecnico = db.Column(db.DateTime)

# ------------------------------------------------------------
# Relacionamentos bidirecionais
# ------------------------------------------------------------
from app.models.base.usuario         import Usuario
from app.models.aluno.aluno          import Aluno
from app.models.professor.professor  import Professor
from app.models.tecnico.tecnico      import Tecnico
from app.models.sala_laboratorio     import SalaLaboratorio
from app.models.horario              import Horario

Solicitacao.usuario_criador = db.relationship(
    Usuario,
    back_populates='solicitacoes_criadas'
)

Solicitacao.aluno = db.relationship(
    Aluno,
    back_populates='solicitacoes'
)

Solicitacao.professor = db.relationship(
    Professor,
    back_populates='solicitacoes'
)

Solicitacao.tecnico = db.relationship(
    Tecnico,
    back_populates='solicitacoes'
)

Solicitacao.sala = db.relationship(
    SalaLaboratorio,
    backref='solicitacoes'
)

Solicitacao.horario = db.relationship(
    Horario,
    backref='solicitacoes'
)
