# app/__init__.py

from flask import Flask
from flask_login import LoginManager
from app.extensions import db

# importa todos os blueprints com seus nomes exatos
from auth.login_redirecionar       import login_redirecionar_bp
from auth.login.login_aluno        import login_aluno_bp
from auth.login.login_professor    import login_professor_bp
from auth.login.login_tecnico      import login_tecnico_bp
from auth.cadastro.cadastro_aluno      import cadastro_aluno_bp
from auth.cadastro.cadastro_professor  import cadastro_professor_bp
from auth.cadastro.cadastro_tecnico    import cadastro_tecnico_bp
from app.controller.agendamento.agendamento_aluno import agendamento_aluno_bp
from app.controller.agendamento.agendamento_professor import agendamento_professor_bp
# configura Flask-Login
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="seu-segredo-aqui",
        SQLALCHEMY_DATABASE_URI="sqlite:///dev.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login_redirecionar.tela_login"

    # registra blueprints (todos no prefixo /auth, se quiser)
    app.register_blueprint(login_redirecionar_bp)
    app.register_blueprint(cadastro_aluno_bp)
    app.register_blueprint(cadastro_professor_bp)
    app.register_blueprint(cadastro_tecnico_bp)
    app.register_blueprint(login_aluno_bp)
    app.register_blueprint(login_professor_bp)
    app.register_blueprint(login_tecnico_bp)
    app.register_blueprint(agendamento_aluno_bp)
    app.register_blueprint(agendamento_professor_bp)
    # cria as tabelas após as classes estarem carregadas
    with app.app_context():
        from app.models.base.usuario        import Usuario
        from app.models.aluno.aluno         import Aluno
        from app.models.professor.professor import Professor
        from app.models.tecnico.tecnico     import Tecnico
        from app.models.sala_laboratorio    import SalaLaboratorio
        from app.models.horario             import Horario
        from app.models.solicitacao         import Solicitacao

        db.create_all()
        
    return app
