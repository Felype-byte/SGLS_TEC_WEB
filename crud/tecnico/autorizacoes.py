from app.models.solicitacao import Solicitacao, db

def listar_aprovadas_professor():
    return Solicitacao.query.filter_by(status='aprovado professor').all()

def autorizar_solicitacao(id_solicitacao, parecer):
    solicitacao = Solicitacao.query.get(id_solicitacao)
    if solicitacao:
        solicitacao.status = 'autorizado tecnico'
        solicitacao.parecer_tecnico = parecer
        db.session.commit()
        return True
    return False

def negar_solicitacao(id_solicitacao, parecer):
    solicitacao = Solicitacao.query.get(id_solicitacao)
    if solicitacao:
        solicitacao.status = 'negado tecnico'
        solicitacao.parecer_tecnico = parecer
        db.session.commit()
        return True
    return False
