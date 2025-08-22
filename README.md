# Bookly - Book Management API

A modern, fast, and secure REST API for managing books, users, and reviews built with FastAPI and Python. This application provides comprehensive book management capabilities with user authentication, role-based access control, and review functionality.

## 🚀 Features

### Core Functionality
- **User Management**: User registration, authentication, and profile management
- **Book Management**: Complete CRUD operations for books
- **Review System**: Users can rate and review books (1-5 stars)
- **Role-Based Access Control**: Admin and user roles with different permissions

### Security & Authentication
- **JWT Token Authentication**: Secure access and refresh token system
- **Password Hashing**: Secure password storage using bcrypt
- **Token Blacklisting**: Secure logout with Redis-based token invalidation
- **Role-Based Authorization**: Different access levels for admin and regular users

### Technical Features
- **Async/Await Support**: High-performance asynchronous operations
- **Database Migrations**: Automated database schema management with Alembic
- **Data Validation**: Comprehensive input validation using Pydantic
- **API Documentation**: Auto-generated interactive API docs with Swagger UI

## 🛠 Technology Stack

- **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- **Database ORM**: [SQLModel](https://sqlmodel.tiangolo.com/) - SQL databases using Python type hints
- **Database**: PostgreSQL with async support
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Database migration tool
- **Authentication**: [PyJWT](https://pyjwt.readthedocs.io/) - JSON Web Token implementation
- **Password Hashing**: [Passlib](https://passlib.readthedocs.io/) with bcrypt
- **Caching/Session Storage**: [Redis](https://redis.io/) - For token blacklisting
- **Data Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation using Python type annotations
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- Python 3.8 or higher
- PostgreSQL database
- Redis server
- pip (Python package manager)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/asliAdarsh/bookly.git
cd bookly
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

The current `requirements.txt` is incomplete. Install the required dependencies:

```bash
pip install -r requirements.txt

# Install additional required dependencies (if not already in requirements.txt)
pip install sqlmodel alembic asyncpg psycopg2-binary passlib[bcrypt] PyJWT redis pydantic-settings
```

**Complete Dependencies List:**
```txt
# Web Framework
fastapi==0.115.13
uvicorn[standard]==0.34.3

# Database & ORM
sqlmodel
alembic
asyncpg
psycopg2-binary

# Authentication & Security
PyJWT
passlib[bcrypt]

# Caching & Session Management
redis
pydantic-settings

# Data Validation & Utilities
pydantic==2.11.7
python-dotenv==1.1.1
python-multipart==0.0.20
email-validator==2.2.0

# Additional FastAPI dependencies
fastapi-cli==0.0.7
# ... (other dependencies from existing requirements.txt)
```

### 4. Environment Configuration

Create a `.env` file in the project root directory:

```bash
cp .env.example .env  # If example exists, otherwise create new
```

Add the following environment variables to your `.env` file:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/bookly_db

# JWT Configuration
JWT_SECRET=your-super-secure-secret-key-here
JWT_ALGORITHM=HS256

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Optional: Redis Password (if your Redis server requires authentication)
# REDIS_PASSWORD=your-redis-password
```

**Important**: Replace the placeholder values with your actual configuration:
- `username:password` - Your PostgreSQL credentials
- `bookly_db` - Your database name
- `your-super-secure-secret-key-here` - A strong, random secret key for JWT signing

### 5. Database Setup

#### Create Database

```sql
-- Connect to PostgreSQL and create database
CREATE DATABASE bookly_db;
CREATE USER bookly_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE bookly_db TO bookly_user;
```

#### Run Migrations

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Run database migrations
alembic upgrade head
```

### 6. Start Redis Server

Make sure Redis is running on your system:

```bash
# On macOS with Homebrew
brew services start redis

# On Ubuntu/Debian
sudo systemctl start redis-server

# On Windows (if using WSL or native installation)
redis-server
```

## 🚀 Running the Application

### Quick Start (Test Import)

To verify the application loads correctly:

```bash
# Test if all dependencies are properly installed
cd bookly
python -c "import src; print('✅ Application ready to run!')"
```

### Development Mode

```bash
# Using uvicorn directly
uvicorn src:app --reload --host 0.0.0.0 --port 8000

# Or using FastAPI CLI
fastapi dev src/__init__.py
```

**Note**: The application requires a properly configured database and Redis to start successfully. Make sure you have completed the [Database Setup](#database-setup) and [Redis](#start-redis-server) configuration steps.

### Production Mode

```bash
uvicorn src:app --host 0.0.0.0 --port 8000 --workers 4
```

The application will be available at:
- **API**: http://localhost:8000
- **Interactive API Documentation**: http://localhost:8000/docs
- **Alternative API Documentation**: http://localhost:8000/redoc

## 📖 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication Endpoints

#### User Registration
```http
POST /api/v1/user/signup
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

#### User Login
```http
POST /api/v1/user/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepassword"
}
```

Response:
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "uid": "123e4567-e89b-12d3-a456-426614174000",
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

#### Get Current User
```http
GET /api/v1/user/me
Authorization: Bearer <access_token>
```

#### Refresh Token
```http
GET /api/v1/user/refresh-token
Authorization: Bearer <refresh_token>
```

#### Logout
```http
GET /api/v1/user/logout
Authorization: Bearer <access_token>
```

### Book Management Endpoints

#### Get All Books
```http
GET /api/v1/book/
Authorization: Bearer <access_token>
```

#### Get Book by ID
```http
GET /api/v1/book/{book_uid}
Authorization: Bearer <access_token>
```

#### Create New Book
```http
POST /api/v1/book/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "publisher": "Scribner",
  "published_date": "1925-04-10",
  "page_count": 180,
  "language": "English"
}
```

#### Update Book
```http
PATCH /api/v1/book/{book_uid}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "page_count": 200
}
```

#### Delete Book
```http
DELETE /api/v1/book/{book_uid}
Authorization: Bearer <access_token>
```

#### Get Books by User
```http
GET /api/v1/book/user/{user_uid}
Authorization: Bearer <access_token>
```

### Review Endpoints

#### Add Review to Book
```http
POST /api/v1/review/book/{book_uid}/review
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "rating": 5,
  "review_text": "Excellent book! Highly recommended."
}
```

## 🗄 Database Schema

### Users Table
```sql
CREATE TABLE users (
    uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR NOT NULL UNIQUE,
    email VARCHAR NOT NULL UNIQUE,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'user',
    is_verified BOOLEAN DEFAULT FALSE,
    password_hash VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Books Table
```sql
CREATE TABLE books (
    uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    publisher VARCHAR NOT NULL,
    published_date DATE NOT NULL,
    page_count INTEGER NOT NULL,
    language VARCHAR NOT NULL,
    user_uid UUID REFERENCES users(uid),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Reviews Table
```sql
CREATE TABLE reviews (
    uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT NOT NULL,
    user_uid UUID REFERENCES users(uid),
    book_uid UUID REFERENCES books(uid),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## 🔐 Authentication & Authorization

### JWT Token System
- **Access Token**: Short-lived token (1 hour) for API access
- **Refresh Token**: Long-lived token (2 days) for obtaining new access tokens
- **Token Blacklisting**: Logout functionality using Redis to blacklist tokens

### User Roles
- **admin**: Full access to all resources and operations
- **user**: Access to personal resources and general read operations

### Security Features
- Password hashing using bcrypt
- JWT token expiration and validation
- Role-based access control on all endpoints
- Secure token refresh mechanism

## 🧪 Testing

### Manual Testing with curl

#### Register a new user:
```bash
curl -X POST "http://localhost:8000/api/v1/user/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Test",
       "last_name": "User",
       "username": "testuser",
       "email": "test@example.com",
       "password": "testpass123"
     }'
```

#### Login:
```bash
curl -X POST "http://localhost:8000/api/v1/user/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "password": "testpass123"
     }'
```

#### Create a book (replace TOKEN with actual token):
```bash
curl -X POST "http://localhost:8000/api/v1/book/" \
     -H "Authorization: Bearer TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Test Book",
       "author": "Test Author",
       "publisher": "Test Publisher",
       "published_date": "2023-01-01",
       "page_count": 100,
       "language": "English"
     }'
```

## 🏗 Project Structure

```
bookly/
├── src/                          # Source code directory
│   ├── __init__.py              # FastAPI application setup
│   ├── config.py                # Configuration management
│   ├── auth/                    # Authentication module
│   │   ├── __init__.py
│   │   ├── routes.py            # Auth endpoints
│   │   ├── schemas.py           # Auth data models
│   │   ├── service.py           # Auth business logic
│   │   ├── dependencies.py      # Auth dependencies & middleware
│   │   └── utils.py             # Auth utility functions
│   ├── books/                   # Books module
│   │   ├── __init__.py
│   │   ├── routes.py            # Book endpoints
│   │   ├── schemas.py           # Book data models
│   │   └── service.py           # Book business logic
│   ├── review/                  # Reviews module
│   │   ├── __init__.py
│   │   ├── routes.py            # Review endpoints
│   │   ├── schemas.py           # Review data models
│   │   └── services.py          # Review business logic
│   └── db/                      # Database module
│       ├── __init__.py
│       ├── main.py              # Database connection & session
│       ├── models.py            # SQLModel database models
│       └── redis.py             # Redis connection & operations
├── migrations/                  # Alembic database migrations
│   ├── env.py                   # Alembic environment configuration
│   └── versions/                # Migration files
├── alembic.ini                  # Alembic configuration
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🚀 Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for all function parameters and return values
- Use descriptive variable and function names
- Add docstrings to all public functions and classes

### Database Migrations
Always create migrations for database schema changes:
```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade if needed
alembic downgrade -1
```

### Adding New Features
1. Create appropriate schemas in the respective `schemas.py` file
2. Add business logic to the service layer
3. Create API endpoints in the routes file
4. Update database models if needed
5. Create and run migrations
6. Test the new functionality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/asliAdarsh/bookly/issues) page
2. Create a new issue if your problem isn't already reported
3. Provide detailed information about your environment and the issue

## 🔗 Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)