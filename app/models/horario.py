from app.extensions import db
from datetime import time

class Horario(db.Model):
    __tablename__ = 'horarios'

    id_horarios  = db.Column(db.Integer, primary_key=True)
    status       = db.Column(db.String(20), default='Disponível', nullable=False)
    data         = db.Column(db.Date, nullable=False)
    hora_inicio  = db.Column(db.Time, nullable=False)
    hora_fim     = db.Column(db.Time, nullable=False)
    nome_bloco   = db.Column(db.String(100), nullable=True)

    id_sala = db.Column(
        db.Integer,
        db.ForeignKey('salaslaboratorio.id_sala'),
        nullable=False
    )

    # 🔗 Relacionamento com SalaLaboratorio
    sala = db.relationship(
        'SalaLaboratorio',
        back_populates='horarios',
        uselist=False
    )

    # 🔗 Relacionamento com Solicitacao
    solicitacoes = db.relationship(
        'Solicitacao',
        back_populates='horario',
        cascade='all, delete-orphan',
        lazy=True
    )

    @property
    def texto(self):
        return f"{self.hora_inicio.strftime('%H:%M')} – {self.hora_fim.strftime('%H:%M')}"

    def __repr__(self):
        return (
            f"<Horario {self.id_horarios} – {self.texto} ({self.data}) – "
            f"{self.status}{f' – {self.nome_bloco}' if self.nome_bloco else ''}>"
        )

    def esta_disponivel(self):
        return self.status.lower() == 'disponível'

    def descricao_completa(self):
        bloco = f" – {self.nome_bloco}" if self.nome_bloco else ""
        return f"{self.texto} – {self.data.strftime('%d/%m/%Y')} – Sala {self.sala.nome_sala}{bloco}"
