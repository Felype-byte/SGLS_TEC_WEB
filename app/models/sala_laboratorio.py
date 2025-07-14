from app.extensions import db

class SalaLaboratorio(db.Model):
    __tablename__ = 'salaslaboratorio'

    id_sala       = db.Column(db.Integer, primary_key=True)
    nome_sala     = db.Column(db.String(100), nullable=False)
    numero_sala   = db.Column(db.String(100), nullable=False)
    bloco         = db.Column(db.String(50), nullable=True)

    # Relacionamento com Horário
    horarios = db.relationship(
        'Horario',
        back_populates='sala',
        cascade='all, delete-orphan',
        lazy=True
    )

    # 🔗 Novo relacionamento com Solicitação
    solicitacoes = db.relationship(
        'Solicitacao',
        back_populates='sala',
        cascade='all, delete-orphan',
        lazy=True
    )

    def __repr__(self):
        return f'<SalaLaboratorio {self.nome_sala} – Sala {self.numero_sala} – Bloco {self.bloco}>'
