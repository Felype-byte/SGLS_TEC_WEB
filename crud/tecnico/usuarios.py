# crud/tecnico/usuarios.py

from app.models.base.usuario import Usuario, db

# 🚀 Criar novo usuário
def criar_usuario(matricula_siape, senha, tipo):
    novo_usuario = Usuario(
        matricula_siape=matricula_siape,
        senha=senha,
        tipo_usuario=tipo
    )
    db.session.add(novo_usuario)
    db.session.commit()
    return novo_usuario

# 🔍 Buscar usuário por credenciais (para login)
def buscar_usuario(matricula_siape, senha):
    return Usuario.query.filter_by(
        matricula_siape=matricula_siape,
        senha=senha
    ).first()

# 📋 Listar todos os usuários
def listar_usuarios():
    return Usuario.query.all()

# 🗑️ Deletar usuário por ID
def deletar_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return True
    return False
