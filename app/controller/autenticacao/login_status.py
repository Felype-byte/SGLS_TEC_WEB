from functools import wraps
from flask import session, redirect, url_for

def usuario_logado():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "id_usuario" not in session:
                return redirect(url_for("login_redirecionar.tela_login"))
            return func(*args, **kwargs)
        return wrapper
    return decorator
