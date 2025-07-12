from flask_login import UserMixin
from app.extensions import db

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id_usuarios   = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(100), unique=True, nullable=False)
    senha         = db.Column(db.String(255), nullable=False)

    tipo_usuario = db.Column(
        db.Enum('Aluno', 'Professor', 'Tecnico', name='tipo_usuario_enum'),
        nullable=False
    )

    # Relacionamento com os perfis específicos
    aluno     = db.relationship('Aluno',     back_populates='usuario', uselist=False)
    professor = db.relationship('Professor', back_populates='usuario', uselist=False)
    tecnico   = db.relationship('Tecnico',   back_populates='usuario', uselist=False)

    # Relacionamento com solicitações criadas (ajustado para usar back_populates)
    solicitacoes_criadas = db.relationship(
        'Solicitacao',
        back_populates='usuario_criador',
        cascade='all, delete-orphan'
    )

    def get_id(self):
        return str(self.id_usuarios)

    def __repr__(self):
        return f"<Usuario {self.id_usuarios} – {self.tipo_usuario}>"
