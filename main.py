from flask import Flask, redirect, url_for
from flask_login import LoginManager, login_required, logout_user
from app.extensions import db

# Models
from app.models.base.usuario import Usuario

# Blueprints
from auth.login_redirecionar import login_redirecionar_bp
from auth.login.login_aluno import login_aluno_bp
from auth.login.login_professor import login_professor_bp
from auth.login.login_tecnico import login_tecnico_bp
from auth.cadastro.cadastro_aluno import cadastro_aluno_bp
from auth.cadastro.cadastro_professor import cadastro_professor_bp
from auth.cadastro.cadastro_tecnico import cadastro_tecnico_bp
from app.controller.agendamento.agendamento_aluno import agendamento_aluno_bp
from app.controller.agendamento.agendamento_professor import agendamento_professor_bp
app = Flask(__name__)
app.secret_key = "sghl_super_secreto"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://sgls:ynFs42LpfsjGDEHP@132.226.249.149:3306/sgls"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login_redirecionar.tela_login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Registro de Blueprints
app.register_blueprint(login_redirecionar_bp)
app.register_blueprint(cadastro_aluno_bp)
app.register_blueprint(cadastro_professor_bp)
app.register_blueprint(cadastro_tecnico_bp)
app.register_blueprint(login_aluno_bp)
app.register_blueprint(login_professor_bp)
app.register_blueprint(login_tecnico_bp)
app.register_blueprint(agendamento_aluno_bp)
app.register_blueprint(agendamento_professor_bp)
# 🔁 Redirecionamento inicial
@app.route("/")
def home():
    return redirect(url_for("login_redirecionar.tela_login"))

# 🚪 Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login_redirecionar.tela_login"))

if __name__ == "__main__":
    app.run(debug=True)
