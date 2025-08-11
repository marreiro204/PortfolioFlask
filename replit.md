# Overview

This is a personal portfolio website built with Flask, designed to showcase projects, skills, and provide contact functionality. The application features a Portuguese interface and uses a dark theme optimized for the Replit environment. The site serves as a professional portfolio for a full-stack developer, with sections for projects, skills, and contact information.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 with Flask for server-side rendering
- **UI Framework**: Bootstrap 5 with Replit's dark theme customization
- **Icons**: Font Awesome for consistent iconography
- **JavaScript**: Vanilla JavaScript for smooth scrolling, navbar highlighting, form validation, and animations
- **Styling**: Custom CSS with CSS variables for theming, gradient backgrounds, and responsive design
- **Language**: Portuguese (pt-BR) localization throughout the interface

## Backend Architecture
- **Web Framework**: Flask with SQLAlchemy ORM for database operations
- **Database Models**: Three main entities - Project, Skill, and Contact with appropriate relationships
- **Session Management**: Flask sessions with configurable secret key
- **Error Handling**: Custom 404 error pages and comprehensive exception logging
- **Middleware**: ProxyFix for proper HTTPS URL generation in hosted environments

## Database Schema
- **User Model**: Stores user information with id, nome, email, senha_hash, foto_url, criado_em
- **Project Model**: Stores portfolio projects with id, titulo, descricao, imagem_url, status ('draft'/'published'), criado_em, atualizado_em, user_id (FK)
- **Achievement Model**: Manages user achievements with id, titulo, descricao, data, imagem_url, user_id (FK)
- **Comment Model**: Handles project comments with id, conteudo, criado_em, user_id (FK), project_id (FK)
- **Like Model**: Manages project likes with id, user_id (FK), project_id (FK) - unique constraint prevents duplicate likes
- **Notification Model**: Stores user notifications with id, tipo, mensagem, lida (boolean), criado_em, user_id (FK)
- **Database Migration**: Automatic table creation on application startup using SQLite

## Security and Configuration
- **Environment Variables**: Database URL and session secret configuration
- **Connection Pooling**: SQLAlchemy engine optimization with connection recycling and pre-ping
- **Proxy Support**: ProxyFix middleware for reverse proxy compatibility

# External Dependencies

## Frontend Libraries
- **Bootstrap 5**: UI framework with Replit dark theme variant
- **Font Awesome 6.4.0**: Icon library for consistent UI elements
- **Custom CSS**: Portfolio-specific styling and responsive design

## Backend Dependencies
- **Flask**: Core web framework
- **Flask-SQLAlchemy**: Database ORM integration
- **SQLAlchemy**: Database abstraction layer with DeclarativeBase
- **Werkzeug**: WSGI utilities including ProxyFix middleware

## Database Support
- **SQLite**: Primary database for development and production (portfolio.db)
- **Connection Management**: Built-in connection pooling and health checks
- **Relationships**: Full foreign key support with cascade delete operations

## Hosting and Deployment
- **Replit Integration**: Optimized for Replit hosting environment
- **HTTPS Support**: ProxyFix configuration for secure connections
- **Environment Configuration**: Flexible database and session configuration via environment variables