from app.extensions import db

class Tecnico(db.Model):
    __tablename__ = 'tecnicos'

    id_tecnico     = db.Column(db.Integer, primary_key=True)
    nome_completo  = db.Column(db.String(100), nullable=False)
    siape          = db.Column(db.String(20), unique=True, nullable=False)

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id_usuarios'),
        nullable=False
    )

    usuario = db.relationship(
        'Usuario',
        back_populates='tecnico',
        uselist=False
    )

    def __repr__(self):
        return f"<Tecnico {self.nome_completo} – SIAPE {self.siape}>"

# ------------------------------------------------------------
# relacionamento com Solicitações (adicionado após importação)
# ------------------------------------------------------------
from app.models.solicitacao import Solicitacao

Tecnico.solicitacoes = db.relationship(
    'Solicitacao',
    back_populates='tecnico',
    cascade='all, delete-orphan'
)
