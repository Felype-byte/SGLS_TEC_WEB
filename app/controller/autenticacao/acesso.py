from functools import wraps
from flask import session, redirect, url_for

def acesso_restrito(tipo_esperado):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tipo = session.get("tipo_usuario")
            if tipo != tipo_esperado:
                return redirect(url_for("login_redirecionar.tela_login"))
            return func(*args, **kwargs)
        return wrapper
    return decorator
