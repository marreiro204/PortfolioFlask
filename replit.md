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
- **Project Model**: Stores portfolio projects with title, description, technology stack, URLs (GitHub/demo), images, and featured status
- **Skill Model**: Manages technical skills with categories and proficiency levels (1-5 scale)
- **Contact Model**: Handles contact form submissions with read status tracking
- **Database Migration**: Automatic table creation on application startup

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
- **SQLite**: Default database for development (portfolio.db)
- **PostgreSQL**: Production database support via DATABASE_URL environment variable
- **Connection Management**: Built-in connection pooling and health checks

## Hosting and Deployment
- **Replit Integration**: Optimized for Replit hosting environment
- **HTTPS Support**: ProxyFix configuration for secure connections
- **Environment Configuration**: Flexible database and session configuration via environment variables