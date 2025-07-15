from app.models.solicitacao import Solicitacao, db

#  Listar todas as solicitações pendentes para o professor
def listar_pendentes_professor():
    return Solicitacao.query.filter_by(status='pendente professor').all()

#  Aprovar uma solicitação
def aprovar_solicitacao(id_solicitacao, parecer):
    solicitacao = Solicitacao.query.get(id_solicitacao)
    if solicitacao:
        solicitacao.status = 'aprovado professor'
        solicitacao.parecer_professor = parecer
        db.session.commit()
        return True
    return False

#  Rejeitar uma solicitação
def rejeitar_solicitacao(id_solicitacao, parecer):
    solicitacao = Solicitacao.query.get(id_solicitacao)
    if solicitacao:
        solicitacao.status = 'rejeitado professor'
        solicitacao.parecer_professor = parecer
        db.session.commit()
        return True
    return False
