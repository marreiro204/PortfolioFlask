# Overview

This is a complete personal portfolio website built with Flask, featuring comprehensive user authentication, admin panel for content management, and public pages for portfolio showcase. The application includes a full-featured authentication system with login, registration, and password recovery, an administrative dashboard for managing projects and achievements, and interactive public pages where users can view, like, and comment on projects. The interface is entirely in Portuguese with a responsive dark theme optimized for the Replit environment.

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
- **Authentication System**: Complete user authentication with session management, password hashing using Werkzeug, and role-based access control (admin/user)
- **File Upload System**: Secure file handling for project and achievement images with proper validation
- **Form Handling**: WTForms integration with CSRF protection for all user inputs
- **Session Management**: Flask sessions with permanent session support and configurable secret key
- **Error Handling**: Custom 404/500 error pages and comprehensive exception logging
- **Middleware**: ProxyFix for proper HTTPS URL generation in hosted environments
- **Modular Structure**: Separated extensions.py to resolve circular import dependencies

## Database Schema
- **User Model**: Complete user management with id, nome, email, senha_hash, foto_url, is_admin (boolean), criado_em, reset_token, reset_token_expires for password recovery
- **Project Model**: Enhanced project storage with id, titulo, descricao, imagem_url, tags (comma-separated), status ('draft'/'published'), likes_count, criado_em, atualizado_em, user_id (FK)
- **Achievement Model**: User achievements with id, titulo, descricao, data, imagem_url, user_id (FK)
- **Comment Model**: Project comments with id, conteudo, criado_em, user_id (FK), project_id (FK)
- **Like Model**: Project likes with id, user_id (FK), project_id (FK) - unique constraint prevents duplicate likes
- **Notification Model**: Admin notifications with id, tipo ('like'/'comment'), mensagem, lida (boolean), criado_em, user_id (FK)
- **Database Migration**: Automatic table creation on application startup using SQLite with full relationship mapping

## Security and Configuration
- **Environment Variables**: Database URL and session secret configuration
- **Connection Pooling**: SQLAlchemy engine optimization with connection recycling and pre-ping
- **Proxy Support**: ProxyFix middleware for reverse proxy compatibility

# External Dependencies

## Frontend Libraries
- **Bootstrap 5**: UI framework with Replit dark theme variant for consistent dark mode styling
- **Font Awesome 6.4.0**: Icon library for comprehensive UI iconography
- **Custom CSS**: Portfolio-specific styling and responsive design enhancements

## Backend Dependencies
- **Flask**: Core web framework for routing and request handling
- **Flask-SQLAlchemy**: Database ORM integration with relationship management
- **Flask-WTF**: Form handling with CSRF protection and file uploads
- **WTForms**: Form validation and rendering
- **SQLAlchemy**: Database abstraction layer with DeclarativeBase
- **Werkzeug**: WSGI utilities including ProxyFix middleware and password hashing
- **Email-validator**: Email format validation for user registration

## Database Support
- **SQLite**: Primary database for development and production (portfolio.db)
- **Connection Management**: Built-in connection pooling and health checks
- **Relationships**: Full foreign key support with cascade delete operations

## Hosting and Deployment
- **Replit Integration**: Optimized for Replit hosting environment with proper workflow configuration
- **HTTPS Support**: ProxyFix configuration for secure connections in production
- **Environment Configuration**: Flexible database and session configuration via environment variables
- **File Storage**: Local file system storage for uploaded images in static/uploads directory
- **Admin Access**: Default admin account (admin@portfolio.com / admin123) for content management

## Recent Changes (August 12, 2025)
- ✓ Resolved circular import issue by creating extensions.py for database initialization
- ✓ Implemented complete authentication system with registration, login, logout, and password recovery
- ✓ Created comprehensive admin panel with full CRUD operations for projects and achievements
- ✓ Developed interactive public pages with like/comment functionality for logged-in users
- ✓ Added notification system to alert admin of new user interactions
- ✓ Implemented secure file upload system for project and achievement images
- ✓ Created sample data with 3 projects and 2 achievements for demonstration
- ✓ Added proper error handling with custom 404/500 pages
- ✓ Enhanced navigation with dynamic user menu and admin access links