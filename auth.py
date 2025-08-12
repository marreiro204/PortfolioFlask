from functools import wraps
from flask import session, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import smtplib
from email.mime.text import MIMEText

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('login', next=request.url))
        
        from models import User
        from app import db
        user = db.session.get(User, session['user_id'])
        if not user or not user.is_admin:
            flash('Acesso negado. Apenas administradores podem acessar esta página.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def generate_password_reset_token():
    """Generate a secure password reset token"""
    return secrets.token_urlsafe(32)

def send_password_reset_email(email, token):
    """Simulate sending password reset email (print to console)"""
    reset_link = f"http://localhost:5000/reset-password/{token}"
    
    print("=" * 60)
    print("EMAIL DE RECUPERAÇÃO DE SENHA")
    print("=" * 60)
    print(f"Para: {email}")
    print(f"Assunto: Redefinir sua senha")
    print()
    print("Olá,")
    print()
    print("Você solicitou a redefinição de sua senha.")
    print("Clique no link abaixo para criar uma nova senha:")
    print()
    print(f"Link: {reset_link}")
    print()
    print("Este link expira em 1 hora.")
    print("Se você não solicitou esta redefinição, ignore este e-mail.")
    print()
    print("Atenciosamente,")
    print("Equipe do Portfólio")
    print("=" * 60)
    
    return True