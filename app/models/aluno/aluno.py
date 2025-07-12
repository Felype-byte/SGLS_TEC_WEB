from app.extensions import db

class Aluno(db.Model):
    __tablename__ = 'alunos'

    id_aluno        = db.Column(db.Integer, primary_key=True)
    matricula       = db.Column(db.String(20), unique=True, nullable=False)
    nome_completo   = db.Column(db.String(100), nullable=False)
    curso           = db.Column(db.String(100), nullable=False)
    turma_monitoria = db.Column(db.String(45), nullable=True)
    cpf             = db.Column(db.String(11), unique=True, nullable=False)

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id_usuarios'),
        nullable=False
    )
    usuario = db.relationship(
        'Usuario',
        back_populates='aluno',
        uselist=False
    )

    def __repr__(self):
        return f"<Aluno {self.nome_completo} – {self.matricula}>"

# ------------------------------------------------------------
# Relacionamento com Solicitacoes
# ------------------------------------------------------------
from app.models.solicitacao import Solicitacao

Aluno.solicitacoes = db.relationship(
    'Solicitacao',
    back_populates='aluno',
    cascade='all, delete-orphan'
)
