# ScholarFlow Backend API

A comprehensive school management system API built with Django and Django REST Framework. ScholarFlow provides robust authentication, user management, and school administration features for educational institutions.

## Table of Contents

- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Authentication & Authorization](#authentication--authorization)
- [Database Models](#database-models)
- [Core Modules](#core-modules)
- [Email System](#email-system)
- [Testing](#testing)

---

## Project Overview

**ScholarFlow** is a modern, RESTful API backend designed to manage all aspects of a school or educational institution. It provides:

- User registration and authentication with email verification
- Role-based access control (Student, Teacher, Parent, Administrator)
- User profile management with picture upload
- Password reset functionality
- JWT token-based authentication with refresh token rotation
- School/Establishment management
- WebSocket support via Django Channels
- Comprehensive API documentation with Swagger/ReDoc

The backend is built following best practices including:
- Separation of concerns (service layer architecture)
- Custom exception handling
- Centralized response formatting
- Token blacklisting and revocation
- Rate limiting on authentication endpoints
- Email verification with time-limited tokens

---

## Technology Stack

### Core Framework
- **Django 5.2.7** - Web framework
- **Django REST Framework 3.16.1** - API framework
- **Python 3.x** - Programming language

### Authentication & Security
- **djangorestframework_simplejwt 5.5.1** - JWT token management
- **PyJWT 2.10.1** - JWT encoding/decoding
- **django-cors-headers 4.9.0** - CORS support

### Database
- **PostgreSQL** (configured, MySQL support commented out)
- **mysqlclient 2.2.7** - MySQL adapter (optional)

### Real-time Communication
- **Channels 4.3.1** - WebSocket support
- **channels_redis 4.3.0** - Redis channel layer
- **redis 7.0.1** - Caching and session storage

### File Storage
- **boto3 1.40.71** - AWS S3 integration
- **botocore 1.40.71** - AWS core services
- **s3transfer 0.14.0** - S3 file transfers
- **Pillow 12.0.0** - Image processing

### Utilities & Tools
- **django-environ 0.12.0** - Environment variable management
- **python-dotenv 1.2.1** - .env file support
- **drf-yasg 1.21.11** - API documentation (Swagger/ReDoc)
- **pytz 2025.2** - Timezone handling
- **python-dateutil 2.9.0.post0** - Date utilities

---

## Project Structure

```
ScholarFlow/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not in repo)
├── README.md                 # This file
│
├── sch_pj/                   # Main Django project config
│   ├── settings.py           # Project settings & configuration
│   ├── urls.py               # URL routing configuration
│   ├── asgi.py               # ASGI config for WebSockets
│   ├── wsgi.py               # WSGI config for production
│   └── __init__.py
│
├── accounts/                 # User accounts & authentication app
│   ├── models.py             # User model with custom manager
│   ├── serializers.py        # Serializers for user data
│   ├── views.py              # API views
│   ├── urls.py               # App-specific URL routing
│   ├── admin.py              # Django admin configuration
│   ├── apps.py               # App configuration
│   ├── tests.py              # Unit tests
│   │
│   ├── auth/                 # Authentication submodule
│   │   ├── services.py       # Authentication business logic
│   │   ├── views.py          # Auth endpoints
│   │   └── __init__.py
│   │
│   ├── profile/              # User profile management
│   │   ├── services.py       # Profile business logic
│   │   ├── views.py          # Profile endpoints
│   │   ├── test_services.py  # Profile service tests
│   │   └── __init__.py
│   │
│   ├── verification/         # Email & password verification
│   │   ├── services.py       # Verification logic
│   │   ├── views.py          # Verification endpoints
│   │   ├── emails.py         # Email sending utilities
│   │   ├── tokens.py         # Token verification logic
│   │   ├── password_reset_service.py  # Password reset logic
│   │   └── __init__.py
│   │
│   ├── core/                 # Core utilities
│   │   ├── base_view.py      # Base API view class
│   │   ├── jwt_utils.py      # JWT token management
│   │   ├── response.py       # Response formatting
│   │   ├── exceptions.py     # Custom exceptions
│   │   └── __init__.py
│   │
│   ├── migrations/           # Database migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_user_is_verified.py
│   │   ├── 0003_alter_user_unique_together_user_full_name_and_more.py
│   │   └── __init__.py
│   │
│   └── __pycache__/
│
├── school/                   # School/Establishment app
│   ├── models.py             # Establishment model
│   ├── serializers.py        # Establishment serializers
│   ├── views.py              # Establishment API views
│   ├── urls.py               # App-specific routing
│   ├── admin.py              # Django admin config
│   ├── apps.py               # App configuration
│   ├── tests.py              # Unit tests
│   │
│   ├── migrations/           # Database migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   │
│   └── __pycache__/
│
├── profile_pics/             # User profile pictures storage
│
├── templates/                # Email templates
│   └── emails/
│       ├── base_email.html   # Base email template
│       ├── verify_email.html # Email verification template
│       └── password_reset.html  # Password reset template
│
└── __pycache__/

```

---

## Features

### 1. **Authentication System**
- User registration with email validation
- Email verification with time-limited tokens (3 days)
- Secure password hashing using Django's built-in system
- Password complexity validation
- Login with email-based authentication
- JWT token generation with access and refresh tokens
- Token refresh without full re-authentication
- Token rotation for enhanced security
- Token blacklisting on logout

### 2. **User Management**
- Multiple user roles (Student, Teacher, Parent, Administrator)
- Comprehensive user profile with:
  - Basic info (first name, last name, full name)
  - Email and phone number
  - Address
  - Profile picture with AWS S3 integration
  - Unique matricule (student ID)
  - Created and updated timestamps
- Profile update functionality
- Profile picture upload and management

### 3. **Password Management**
- Secure password reset via email
- Time-limited password reset tokens
- New password validation
- Password history tracking

### 4. **Email System**
- SMTP-based email sending (Gmail configured)
- HTML email templates with fallback to plain text
- Email verification workflow
- Password reset emails
- Configurable email templates
- Asynchronous email sending (background tasks)
- Error logging for email failures

### 5. **School Management**
- School/Establishment model with basic info:
  - Unique school ID
  - School name
  - Address
  - Creation date
  - Status
- Establishment CRUD operations (admin only)

### 6. **API Documentation**
- Swagger UI at `/docs/` endpoint
- ReDoc documentation at `/redoc/` endpoint
- Automatic schema generation from code
- Request/response examples

### 7. **Security Features**
- CORS support with configurable origins
- CSRF protection
- Rate limiting on authentication endpoints
- Email verification requirement before account activation
- Account locking on suspicious activity (framework in place)
- Secure HTTP headers
- Session management with Redis

### 8. **Real-time Communication**
- WebSocket support via Django Channels
- Redis-based channel layers for multi-process deployment
- ASGI application server support

---

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (or MySQL)
- Redis (for caching and WebSockets)
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/your-org/scholarflow.git
cd ScholarFlow/tests/back
```

### Step 2: Create Virtual Environment
```bash
# On Windows (cmd)
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=scholarflow_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Redis
REDIS_URL=redis://localhost:6379/0

# AWS S3 (optional)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1
```

### Step 5: Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

---

## Configuration

### Django Settings (`sch_pj/settings.py`)

#### Installed Apps
```python
INSTALLED_APPS = [
    # Django built-in
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'channels',
    # Local apps
    'accounts',
    'school',
]
```

#### JWT Configuration
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
}
```

#### Database Support
- **Primary**: PostgreSQL (recommended for production)
- **Alternative**: MySQL (configuration available, commented out)

#### Cache Configuration
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```
Redis cache is available for production deployments.

#### Email Settings
Configured for Gmail SMTP with support for HTML templates.

#### WebSocket Configuration (Channels)
```python
ASGI_APPLICATION = 'sch_pj.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [env('REDIS_URL')],
        },
    },
}
```

---

## Running the Application

### Development Server
```bash
# Start Django development server
python manage.py runserver

# Server will be available at http://localhost:8000
```

### Production with Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn sch_pj.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### With WebSocket Support (Daphne)
```bash
# Install Daphne
pip install daphne

# Run with Daphne for ASGI
daphne -b 0.0.0.0 -p 8000 sch_pj.asgi:application
```

---

## API Documentation

### Swagger UI
- **URL**: `http://localhost:8000/docs/`
- Interactive API documentation with "Try it out" functionality

### ReDoc
- **URL**: `http://localhost:8000/redoc/`
- Clean, reader-friendly API documentation

### Base URL
```
http://localhost:8000/api/
```

---

## Authentication & Authorization

### Authentication Flow

#### 1. Registration
**Endpoint**: `POST /api/auth/register/`

Request:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "phone_number": "+1234567890",
  "full_name": "John Doe"
}
```

Response:
```json
{
  "success": true,
  "message": "Registration successful. Please verify your email.",
  "data": {
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
  }
}
```

#### 2. Email Verification
**Endpoint**: `POST /api/auth/email-verify/`

Request:
```json
{
  "uid": "base64-encoded-user-id",
  "token": "verification-token-from-email"
}
```

#### 3. Login
**Endpoint**: `POST /api/auth/login/`

Request:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

Response:
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 4. Token Refresh
**Endpoint**: `POST /api/auth/token/refresh`

Request:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 5. Logout
**Endpoint**: `POST /api/auth/logout/`

Blacklists the current refresh token.

### JWT Token Structure

**Access Token** (15 minutes expiry):
- `user_id`: User's unique identifier
- `username`: User's username
- `email`: User's email
- `is_staff`: Admin status
- `is_verified`: Email verification status
- `jti`: Unique token identifier (for blacklisting)

**Refresh Token** (14 days expiry):
- All access token claims plus longer expiry
- Used to obtain new access tokens

### Authorization

#### Protected Endpoints
All endpoints except registration and login require authentication.

**Header**:
```
Authorization: Bearer <access_token>
```

#### Role-Based Access
- **Student**: Can view own profile and school info
- **Teacher**: Can manage classes and assignments
- **Parent**: Can view child's information
- **Administrator**: Full access to all resources

---

## Database Models

### User Model
Located in `accounts/models.py`

```python
class User(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ("etudiant", "Étudiant"),
        ("enseignant", "Enseignant"),
        ("parent", "Parent"),
        ("administrateur", "Administrateur"),
    ]
    
    id = BigAutoField(primary_key=True)
    matricule = CharField(unique=True, max_length=50)
    username = CharField(max_length=150, unique=True)
    email = EmailField(unique=True, max_length=191)
    first_name = CharField(max_length=100)
    full_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    profile_picture = ImageField(upload_to='profile_pics/')
    phone_number = CharField(max_length=20)
    adresse = CharField(max_length=255)
    role = CharField(max_length=20, choices=ROLES)
    
    is_verified = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=False)
    
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**Key Features**:
- Custom manager for user creation
- Support for 4 user roles
- Email-based authentication (no username login)
- Profile picture storage
- Timestamps for audit trail

### Establishment Model
Located in `school/models.py`

```python
class Etablissement(models.Model):
    id = CharField(primary_key=True, max_length=50)
    name = CharField(max_length=255)
    adresse = CharField(max_length=255)
    created_at = DateField()
    statut = CharField(max_length=7)
```

**Key Features**:
- String-based ID for school code
- Address and creation tracking
- Status management

---

## Core Modules

### 1. Authentication Service (`accounts/auth/services.py`)

**Class**: `AuthenticationService`

Methods:
- `register()` - User registration with email verification
- `login()` - Authenticate user and generate tokens
- `validate_password()` - Password complexity validation

**Features**:
- Email conflict detection
- Asynchronous email sending
- Request logging and tracking
- Comprehensive error messages

### 2. Email Verification Service (`accounts/verification/services.py`)

**Class**: `EmailVerificationService`

Methods:
- `verify_email()` - Verify email with token
- `send_verification_email()` - Send verification email
- `send_verification_email_background()` - Async email sending

**Features**:
- Time-limited tokens (3 days)
- Email rate limiting
- Cache-based verification status
- Transaction safety with database atomicity

### 3. Profile Service (`accounts/profile/services.py`)

**Class**: `ProfileService`

Methods:
- `get_profile()` - Retrieve user profile
- `update_profile()` - Update profile data
- `_process_profile_picture_file()` - Handle image uploads

**Features**:
- Profile picture validation
- Password change handling
- Partial updates support
- File size and format validation

### 4. JWT Token Manager (`accounts/core/jwt_utils.py`)

**Class**: `TokenManager`

Methods:
- `generate_token()` - Create access and refresh token pair
- `refresh_token()` - Generate new token from refresh token
- `blacklist_token()` - Revoke token
- `is_token_blacklisted()` - Check token status

**Features**:
- Token rotation support
- Cache-based blacklisting
- Comprehensive error handling
- Token metadata storage

### 5. Token Verification (`accounts/verification/tokens.py`)

**Class**: `TokenVerifier`

Methods:
- `verify_token()` - Validate email verification tokens

**Features**:
- Base64 UID decoding
- Django token generator integration
- Detailed error messages

### 6. Email Service (`accounts/verification/emails.py`)

**Class**: `EmailService`

Methods:
- `send_verification_email()` - Send HTML email with verification link
- Email template rendering
- SMTP error handling

**Features**:
- HTML and plain text versions
- Template-based email composition
- Comprehensive logging
- Error recovery

---

## Email System

### Email Configuration

**Provider**: Gmail SMTP

```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'app-specific-password'
```

**Note**: Use Gmail App Passwords, not regular password

### Email Templates

#### 1. Base Template (`templates/emails/base_email.html`)
Common styling and layout for all emails.

#### 2. Email Verification (`templates/emails/verify_email.html`)
Verification link and instructions with:
- User greeting
- Verification button (clickable link)
- Direct link as backup
- Expiry information

#### 3. Password Reset (`templates/emails/password_reset.html`)
Password reset with:
- Reset link
- Instructions
- Security information

### Sending Emails

#### Synchronous (Blocking)
```python
EmailService.send_verification_email(user)
```

#### Asynchronous (Non-blocking)
```python
EmailVerificationService.send_verification_email_background(user_id)
```

---

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login user | No |
| POST | `/api/auth/logout/` | Logout user | Yes |
| POST | `/api/auth/token/refresh` | Refresh access token | No (needs refresh) |
| POST | `/api/auth/token/validate/` | Validate current token | Yes |

### Email Verification Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/api/auth/email-verify/` | Verify email with token | No |
| POST | `/api/auth/send-verification/` | Send verification email | No |
| GET | `/api/auth/verification-status/` | Check verification status | Yes |

### Password Reset Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/api/auth/password-reset/` | Request password reset | No |
| POST | `/api/auth/password-reset-confirm/` | Confirm password reset | No |

### Profile Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| GET | `/api/profile/` | Get user profile | Yes |
| PUT | `/api/profile/` | Update profile | Yes |
| PATCH | `/api/profile/` | Partial profile update | Yes |

---

## Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test school

# Run with verbose output
python manage.py test --verbosity=2

# Run specific test class
python manage.py test accounts.profile.test_services.ProfileServiceTest

# Generate coverage report
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test Files

- `accounts/tests.py` - Account app tests
- `accounts/profile/test_services.py` - Profile service unit tests
- `school/tests.py` - School app tests

### Key Test Areas

1. **User Registration**
   - Valid registration
   - Duplicate email handling
   - Password validation
   - Email verification

2. **Authentication**
   - Successful login
   - Invalid credentials
   - Inactive accounts
   - Token generation

3. **Profile Management**
   - Profile retrieval
   - Profile updates
   - Picture uploads
   - Password changes

4. **Email System**
   - Email sending
   - Template rendering
   - Error handling

---

## Security Considerations

### Current Implementation

1. **Password Security**
   - PBKDF2 hashing with SHA256
   - Minimum 8 characters required
   - Common password validation
   - Numeric and similarity checking

2. **Token Security**
   - JWT with HS256 algorithm
   - Short-lived access tokens (15 min)
   - Long-lived refresh tokens (14 days)
   - Token rotation on refresh
   - Blacklist support for logout

3. **Request Security**
   - CORS protection (configurable origins)
   - CSRF protection on forms
   - Rate limiting on auth endpoints
   - Email verification requirement

4. **Data Protection**
   - HTTPS enforced in production
   - Secure cookie flags (httponly, secure, samesite)
   - SQL injection prevention via ORM
   - XSS protection via templates

### Recommended for Production

1. Set `DEBUG = False`
2. Use strong `SECRET_KEY`
3. Enable `HTTPS` and `SECURE_SSL_REDIRECT`
4. Set `SECURE_HSTS_SECONDS` to enforce HSTS
5. Configure `ALLOWED_HOSTS` properly
6. Use environment variables for all secrets
7. Enable email verification requirement
8. Consider implementing 2FA
9. Monitor and log all authentication attempts
10. Regular security updates for dependencies

---

## Troubleshooting

### Common Issues

#### 1. Email Verification Not Sending
**Solution**:
- Verify Gmail app password is correct
- Check `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in settings
- Enable "Less secure app access" or use App Password
- Check logs for SMTP errors

#### 2. Database Connection Error
**Solution**:
- Verify PostgreSQL is running
- Check `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`
- Ensure database exists: `CREATE DATABASE scholarflow_db;`

#### 3. Redis Connection Error
**Solution**:
- Ensure Redis is running: `redis-server`
- Check `REDIS_URL` configuration
- Verify Redis port (default 6379)

#### 4. CORS Errors
**Solution**:
- Add frontend URL to `CORS_ALLOWED_ORIGINS` in settings
- Check `CORS_ALLOW_CREDENTIALS` setting
- Verify frontend makes requests with proper headers

#### 5. Static Files Not Loading
**Solution**:
```bash
python manage.py collectstatic --noinput
```

---

## Deployment

### Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure proper database (PostgreSQL recommended)
- [ ] Set up Redis cache
- [ ] Configure email provider credentials
- [ ] Set strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS
- [ ] Set up logging
- [ ] Configure AWS S3 for media storage
- [ ] Run database migrations
- [ ] Create superuser
- [ ] Collect static files
- [ ] Set up monitoring and alerts

### Deployment Commands

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server (production)
gunicorn sch_pj.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

---

## Contributing

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small

### Making Changes
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and add tests
3. Run tests: `python manage.py test`
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature/your-feature`
6. Create Pull Request

---

## License

[Add your license information here]

---

## Support

For issues, questions, or contributions, please contact the development team or submit an issue on GitHub.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Dec 2025 | Initial release with auth, profiles, and email |

---

## Acknowledgments

- Django and Django REST Framework communities
- Django Channels for WebSocket support
- JWT authentication implementation
- ScholarFlow team for requirements and design

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc7519)
- [OWASP API Security](https://owasp.org/www-project-api-security/)

---

**Last Updated**: December 4, 2025
**Project Name**: ScholarFlow - School Management System
**Backend Version**: 1.0.0
