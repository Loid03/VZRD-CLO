# VZRD Premium Streetwear - E-commerce Platform

## Overview

VZRD is a premium streetwear e-commerce platform specializing in oversized t-shirts. The application is built as a Flask web application with a focus on modern design, user experience, and streetwear culture aesthetics. The platform features a purple and black color scheme that reflects the urban streetwear aesthetic.

## System Architecture

The application follows a traditional web application architecture with the following components:

- **Frontend**: Server-side rendered HTML templates with Bootstrap 5 and custom CSS
- **Backend**: Flask web framework with Python 3.11
- **Database**: SQLAlchemy ORM with PostgreSQL (configurable to SQLite for development)
- **Payment Processing**: MercadoPago integration for Brazilian market
- **Deployment**: Gunicorn WSGI server with autoscale deployment target

## Key Components

### Backend Components

1. **Flask Application (`app.py`)**
   - Main application with complete e-commerce routes
   - Database initialization with VzrdClothing models
   - Full API endpoints for cart, orders, and admin management

2. **VzrdClothing Package**
   - `models_db.py`: Complete database models including Product, Customer, Order, OrderItem, Contact, Newsletter
   - `__init__.py`: Package initialization with Flask app factory

3. **Entry Point (`main.py`)**
   - Application runner with proper database initialization
   - Imports VzrdClothing models and creates all tables

### Frontend Components

1. **Template System**
   - Base template with responsive navigation and footer
   - Product catalog and detail pages
   - Checkout and payment result pages
   - Contact form and admin panels
   - Admin interface for content management

2. **Static Assets**
   - Custom CSS with streetwear-inspired design system
   - JavaScript for cart functionality and user interactions
   - SVG logo with graffiti-style branding

### Database Schema

- **Products Table**: Complete inventory with pricing, descriptions, stock, sizes, and categories
- **Customers Table**: Customer information for orders and communication
- **Orders Table**: Order management with status tracking and relationships
- **Order Items Table**: Individual items within orders with quantities and sizes
- **Contacts Table**: Customer service and inquiry management
- **Newsletter Table**: Email marketing subscriber management with activation status

## Data Flow

1. **Product Browsing**: Users browse products through filtered and searchable catalog
2. **Cart Management**: Client-side cart storage with localStorage persistence
3. **Checkout Process**: Multi-step checkout with customer information collection
4. **Payment Processing**: MercadoPago integration for Brazilian payment methods (PIX, credit card, boleto)
5. **Order Management**: Admin interface for order tracking and fulfillment

## External Dependencies

### Core Framework Dependencies
- **Flask 3.1.1**: Web framework and request handling
- **SQLAlchemy 2.0.41**: Database ORM and migrations
- **Gunicorn 23.0.0**: Production WSGI server

### Payment Integration
- **MercadoPago 2.3.0**: Payment processing for Brazilian market
- **Requests 2.32.3**: HTTP client for API communications

### Database and Utilities
- **psycopg2-binary 2.9.10**: PostgreSQL database adapter
- **email-validator 2.2.0**: Email validation for forms
- **Werkzeug 3.1.3**: WSGI utilities and security features

### Frontend Libraries (CDN-based)
- **Bootstrap 5.3.0**: Responsive UI framework
- **Font Awesome 6.4.0**: Icon library
- **Google Fonts**: Typography (Inter, Oswald, Bebas Neue)

## Deployment Strategy

The application is configured for deployment on Replit with the following specifications:

1. **Runtime Environment**: Python 3.11 with PostgreSQL 16
2. **Production Server**: Gunicorn with autoscale deployment target
3. **Process Management**: Parallel workflow execution with port binding on 5000
4. **Database Configuration**: Environment-based connection strings with fallback to SQLite
5. **Security**: ProxyFix middleware for proper header handling behind reverse proxies

The deployment supports both development (SQLite) and production (PostgreSQL) database configurations through environment variables.

## Changelog

```
Changelog:
- June 21, 2025: VZRD Otaku Graffiti 2.0 Complete Transformation
  - Complete visual overhaul with anime + graffiti Japanese aesthetic
  - Updated fonts: Permanent Marker (headers), Zen Tokyo Zoo (Japanese), Poppins (body)
  - Enhanced color palette: #111 background, #9D4EDD purple neon, #3A86FF blue neon
  - Added graffiti-style logo with neon glow and glitch effects
  - Implemented CSS glitch animations and sweep button effects
  - Japanese emoji navigation: 🈶 Produtos, 🏮 Drops, 🎌 Sobre, 📮 Contato
  - Created comprehensive product detail pages with reviews system
  - Built Drops page with countdown timer and limited edition previews
  - Integrated Twilio SMS notifications for orders and admin alerts
  - Added Animate.css for smooth entrance animations
  - Environment configuration with .env support
  - Complete README documentation with setup instructions
  - Admin login: admin@vzrd.com / vzrd123, User: user@vzrd.com / 123456

- June 20, 2025: Complete Authentication & Admin System Implementation
  - Implemented full user authentication with Flask-Login (login/register/profile)
  - Added favorites system for logged-in users with heart toggle
  - Created comprehensive product detail pages with size/quantity selection
  - Built advanced search and filtering system (name, category, price range)
  - Developed admin dashboard with statistics and order management
  - Added admin product management with add/edit capabilities
  - Integrated SMS notifications via Twilio for orders and admin alerts
  - Created user profile management and account system
  - Added sample data with 6 Japanese streetwear products and test users

- June 20, 2025: Japanese Streetwear + Graffiti Visual Evolution
  - Updated typography: Permanent Marker for headers, Zen Tokyo Zoo for Japanese elements
  - New graffiti-style logo with neon glow and glitch effects
  - Enhanced color palette: #111 background, #9D4EDD purple neon, #3A86FF blue neon
  - Added urban texture background with grain and gradient overlays
  - Implemented Japanese icons in navigation (🈶, 🏮, 🎌, 📮)
  - Created new collection banner with anime streetwear aesthetic
  - Enhanced buttons with neon glow effects and sweep animations
  - Integrated Animate.css for smooth entrance animations
  - Updated product cards with enhanced neon hover effects

- June 20, 2025: Feature Enhancement Phase
  - Added scroll animations and back-to-top button with purple glow
  - Created "Sobre a VZRD" page with typing effects and brand story
  - Redesigned footer with neon social links and Japanese accents
  - Implemented coupon system (VZRD10, WELCOME15, STREETWEAR20)
  - Added SMS notification system via Twilio integration
  - Enhanced checkout with finalize order functionality

- June 20, 2025: Complete VZRD e-commerce restructure
  - Created VzrdClothing package with proper models_db.py
  - Added full shopping cart functionality and order management
  - Implemented admin dashboard with statistics
  - Added customer management and newsletter system
  - Updated main.py with proper initialization
  - All dependencies installed: flask, flask-sqlalchemy, flask-cors, python-dotenv, twilio
- June 16, 2025: Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```