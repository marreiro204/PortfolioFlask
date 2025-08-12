import os
from datetime import datetime, timedelta
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import desc, func
from extensions import db
from models import User, Project, Achievement, Comment, Like, Notification
from forms import (RegistrationForm, LoginForm, PasswordResetRequestForm, 
                  PasswordResetForm, ProjectForm, AchievementForm, CommentForm)
from auth import login_required, admin_required, generate_password_reset_token, send_password_reset_email

# Create Blueprint
main_bp = Blueprint('main', __name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Upload configuration will be set in the app factory

def save_uploaded_file(file):
    """Save uploaded file and return the path"""
    if file and file.filename:
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return f'uploads/{filename}'
    return None

# Authentication Routes
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        senha_hash = generate_password_hash(form.senha.data)
        user = User(
            nome=form.nome.data,
            email=form.email.data,
            senha_hash=senha_hash
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('auth/register.html', form=form)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.senha_hash, form.senha.data):
            session['user_id'] = user.id
            session['user_name'] = user.nome
            session['is_admin'] = user.is_admin
            
            if form.lembrar.data:
                session.permanent = True
                current_app.permanent_session_lifetime = timedelta(days=30)
            
            next_page = request.args.get('next')
            flash(f'Bem-vindo, {user.nome}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Email ou senha incorretos.', 'danger')
    
    return render_template('auth/login.html', form=form)

@main_bp.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.index'))

@main_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_password_reset_token()
            user.reset_token = token
            user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
            
            send_password_reset_email(user.email, token)
            flash('Instruções para redefinir a senha foram enviadas para seu email.', 'info')
        else:
            flash('Email não encontrado.', 'warning')
        return redirect(url_for('main.login'))
    
    return render_template('auth/forgot_password.html', form=form)

@main_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    if not user or user.reset_token_expires < datetime.utcnow():
        flash('Token inválido ou expirado.', 'danger')
        return redirect(url_for('main.forgot_password'))
    
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.senha_hash = generate_password_hash(form.senha.data)
        user.reset_token = None
        user.reset_token_expires = None
        db.session.commit()
        
        flash('Senha redefinida com sucesso!', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('auth/reset_password.html', form=form)

# Public Routes
@main_bp.route('/')
def index():
    # Get recent and most liked projects
    recent_projects = Project.query.filter_by(status='published').order_by(desc(Project.criado_em)).limit(6).all()
    popular_projects = Project.query.filter_by(status='published').order_by(desc(Project.likes_count)).limit(6).all()
    
    return render_template('index.html', recent_projects=recent_projects, popular_projects=popular_projects)

@main_bp.route('/project/<int:id>')
def project_detail(id):
    project = Project.query.get_or_404(id)
    if project.status != 'published' and not (session.get('is_admin')):
        flash('Projeto não encontrado.', 'warning')
        return redirect(url_for('main.index'))
    
    comments = Comment.query.filter_by(project_id=id).order_by(desc(Comment.criado_em)).all()
    
    # Check if current user liked this project
    user_liked = False
    if 'user_id' in session:
        like = Like.query.filter_by(user_id=session['user_id'], project_id=id).first()
        user_liked = bool(like)
    
    form = CommentForm()
    return render_template('project_detail.html', project=project, comments=comments, 
                         user_liked=user_liked, form=form)

@main_bp.route('/project/<int:id>/like', methods=['POST'])
@login_required
def toggle_like(id):
    project = Project.query.get_or_404(id)
    user_id = session['user_id']
    
    existing_like = Like.query.filter_by(user_id=user_id, project_id=id).first()
    
    if existing_like:
        # Unlike
        db.session.delete(existing_like)
        project.likes_count = max(0, project.likes_count - 1)
        liked = False
    else:
        # Like
        like = Like(user_id=user_id, project_id=id)
        db.session.add(like)
        project.likes_count += 1
        liked = True
        
        # Create notification for admin
        if project.user.is_admin:
            notification = Notification(
                tipo='like',
                mensagem=f'{session.get("user_name", "Usuário")} curtiu seu projeto "{project.titulo}"',
                user_id=project.user_id
            )
            db.session.add(notification)
    
    db.session.commit()
    
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({'liked': liked, 'likes_count': project.likes_count})
    
    return redirect(url_for('main.project_detail', id=id))

@main_bp.route('/project/<int:id>/comment', methods=['POST'])
@login_required
def add_comment(id):
    project = Project.query.get_or_404(id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(
            conteudo=form.conteudo.data,
            user_id=session['user_id'],
            project_id=id
        )
        db.session.add(comment)
        
        # Create notification for admin
        if project.user.is_admin:
            notification = Notification(
                tipo='comment',
                mensagem=f'{session.get("user_name", "Usuário")} comentou no projeto "{project.titulo}"',
                user_id=project.user_id
            )
            db.session.add(notification)
        
        db.session.commit()
        flash('Comentário adicionado com sucesso!', 'success')
    else:
        flash('Erro ao adicionar comentário.', 'danger')
    
    return redirect(url_for('main.project_detail', id=id))

@main_bp.route('/about')
def about():
    # Get admin user info and achievements
    admin = User.query.filter_by(is_admin=True).first()
    if admin:
        achievements = Achievement.query.filter_by(user_id=admin.id).order_by(desc(Achievement.data)).all()
    else:
        achievements = []
    
    return render_template('about.html', admin=admin, achievements=achievements)

# Admin Routes
@main_bp.route('/admin')
@admin_required
def admin_dashboard():
    projects_count = Project.query.count()
    comments_count = Comment.query.count()
    likes_count = Like.query.count()
    unread_notifications = Notification.query.filter_by(lida=False).count()
    
    return render_template('admin/dashboard.html', 
                         projects_count=projects_count,
                         comments_count=comments_count,
                         likes_count=likes_count,
                         unread_notifications=unread_notifications)

@main_bp.route('/admin/projects')
@admin_required
def admin_projects():
    projects = Project.query.order_by(desc(Project.criado_em)).all()
    return render_template('admin/projects.html', projects=projects)

@main_bp.route('/admin/projects/new', methods=['GET', 'POST'])
@admin_required
def admin_project_new():
    form = ProjectForm()
    if form.validate_on_submit():
        # Save uploaded image
        imagem_url = save_uploaded_file(form.imagem.data)
        
        project = Project(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            imagem_url=imagem_url,
            tags=form.tags.data,
            status=form.status.data,
            user_id=session['user_id']
        )
        db.session.add(project)
        db.session.commit()
        
        flash('Projeto criado com sucesso!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/project_form.html', form=form, title='Novo Projeto')

@main_bp.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_project_edit(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    
    if form.validate_on_submit():
        project.titulo = form.titulo.data
        project.descricao = form.descricao.data
        project.tags = form.tags.data
        project.status = form.status.data
        project.atualizado_em = datetime.utcnow()
        
        # Update image if new one uploaded
        if form.imagem.data:
            imagem_url = save_uploaded_file(form.imagem.data)
            if imagem_url:
                project.imagem_url = imagem_url
        
        db.session.commit()
        flash('Projeto atualizado com sucesso!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/project_form.html', form=form, project=project, title='Editar Projeto')

@main_bp.route('/admin/projects/delete/<int:id>', methods=['POST'])
@admin_required
def admin_project_delete(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Projeto excluído com sucesso!', 'success')
    return redirect(url_for('admin_projects'))

@main_bp.route('/admin/achievements')
@admin_required
def admin_achievements():
    achievements = Achievement.query.filter_by(user_id=session['user_id']).order_by(desc(Achievement.data)).all()
    return render_template('admin/achievements.html', achievements=achievements)

@main_bp.route('/admin/achievements/new', methods=['GET', 'POST'])
@admin_required
def admin_achievement_new():
    form = AchievementForm()
    if form.validate_on_submit():
        # Parse date string
        try:
            data = datetime.strptime(form.data_conquista.data, '%Y-%m-%d')
        except ValueError:
            flash('Formato de data inválido. Use AAAA-MM-DD.', 'danger')
            return render_template('admin/achievement_form.html', form=form, title='Nova Conquista')
        
        # Save uploaded image
        imagem_url = save_uploaded_file(form.imagem.data)
        
        achievement = Achievement(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            data=data,
            imagem_url=imagem_url,
            user_id=session['user_id']
        )
        db.session.add(achievement)
        db.session.commit()
        
        flash('Conquista criada com sucesso!', 'success')
        return redirect(url_for('admin_achievements'))
    
    return render_template('admin/achievement_form.html', form=form, title='Nova Conquista')

@main_bp.route('/admin/achievements/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_achievement_edit(id):
    achievement = Achievement.query.get_or_404(id)
    form = AchievementForm(obj=achievement)
    
    # Set date field
    if achievement.data:
        form.data_conquista.data = achievement.data.strftime('%Y-%m-%d')
    
    if form.validate_on_submit():
        try:
            data = datetime.strptime(form.data_conquista.data, '%Y-%m-%d')
        except ValueError:
            flash('Formato de data inválido. Use AAAA-MM-DD.', 'danger')
            return render_template('admin/achievement_form.html', form=form, achievement=achievement, title='Editar Conquista')
        
        achievement.titulo = form.titulo.data
        achievement.descricao = form.descricao.data
        achievement.data = data
        
        # Update image if new one uploaded
        if form.imagem.data:
            imagem_url = save_uploaded_file(form.imagem.data)
            if imagem_url:
                achievement.imagem_url = imagem_url
        
        db.session.commit()
        flash('Conquista atualizada com sucesso!', 'success')
        return redirect(url_for('admin_achievements'))
    
    return render_template('admin/achievement_form.html', form=form, achievement=achievement, title='Editar Conquista')

@main_bp.route('/admin/achievements/delete/<int:id>', methods=['POST'])
@admin_required
def admin_achievement_delete(id):
    achievement = Achievement.query.get_or_404(id)
    db.session.delete(achievement)
    db.session.commit()
    flash('Conquista excluída com sucesso!', 'success')
    return redirect(url_for('admin_achievements'))

@main_bp.route('/admin/notifications')
@admin_required
def admin_notifications():
    notifications = Notification.query.filter_by(user_id=session['user_id']).order_by(desc(Notification.criado_em)).all()
    
    # Mark all as read
    for notification in notifications:
        if not notification.lida:
            notification.lida = True
    db.session.commit()
    
    return render_template('admin/notifications.html', notifications=notifications)