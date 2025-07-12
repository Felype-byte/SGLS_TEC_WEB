from app.extensions import db

class Professor(db.Model):
    __tablename__ = 'professores'

    id_professor   = db.Column(db.Integer, primary_key=True)
    nome_completo  = db.Column(db.String(100), nullable=False)
    departamento   = db.Column(db.String(100), nullable=False)
    curso          = db.Column(db.String(100), nullable=False)
    siape          = db.Column(db.String(20), unique=True, nullable=False)

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id_usuarios'),
        nullable=False
    )

    usuario = db.relationship(
        'Usuario',
        back_populates='professor',
        uselist=False
    )

    def __repr__(self):
        return f"<Professor {self.nome_completo} – {self.departamento}>"

# ------------------------------------------------------------
# Relacionamento com Solicitações
# ------------------------------------------------------------
from app.models.solicitacao import Solicitacao

Professor.solicitacoes = db.relationship(
    'Solicitacao',
    back_populates='professor',
    cascade='all, delete-orphan'
)
