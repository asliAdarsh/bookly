# Bookly - Book Management API

A modern, fast, and secure REST API for managing books, users, and reviews built with FastAPI and Python. This application provides comprehensive book management capabilities with user authentication, role-based access control, and review functionality.

## 📑 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Environment Configuration](#-environment-configuration)
- [Database Setup](#-database-setup)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Database Schema](#-database-schema)
- [Authentication & Authorization](#-authentication--authorization)
- [Database Migrations](#-database-migrations)
- [API Response Examples](#-api-response-examples)
- [Troubleshooting](#-troubleshooting)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Development Guidelines](#-development-guidelines)
- [Docker Deployment](#-docker-deployment-optional)
- [Deployment to Production](#-deployment-to-production)
- [Installation Verification](#-installation-verification)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)
- [Useful Links](#-useful-links)

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

## 🔄 Database Migrations

This project uses Alembic for database schema management. Here are common migration operations:

### Creating Migrations
```bash
# Generate a new migration after model changes
alembic revision --autogenerate -m "Add new feature"

# Create an empty migration file
alembic revision -m "Custom migration name"
```

### Applying Migrations
```bash
# Apply all pending migrations
alembic upgrade head

# Apply migrations up to a specific revision
alembic upgrade <revision_id>

# Apply one migration at a time
alembic upgrade +1
```

### Migration History
```bash
# Show current migration status
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic heads
```

### Rollback Migrations
```bash
# Rollback one migration
alembic downgrade -1

# Rollback to a specific revision
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

## 📊 API Response Examples

### Successful Responses

#### User Registration Success
```json
{
  "uid": "123e4567-e89b-12d3-a456-426614174000",
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_verified": false,
  "created_at": "2023-01-01T10:00:00",
  "updated_at": "2023-01-01T10:00:00",
  "books": []
}
```

#### Book Creation Success
```json
{
  "uid": "456e7890-e89b-12d3-a456-426614174001",
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald", 
  "publisher": "Scribner",
  "published_date": "1925-04-10",
  "page_count": 180,
  "language": "English",
  "user_uid": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2023-01-01T10:05:00",
  "updated_at": "2023-01-01T10:05:00"
}
```

### Error Responses

#### Authentication Error
```json
{
  "detail": "Please provide a valid token"
}
```

#### Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### Not Found Error
```json
{
  "detail": "Book not found"
}
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: `ModuleNotFoundError` when running the application

**Solution**:
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
pip install sqlmodel alembic asyncpg psycopg2-binary passlib[bcrypt] PyJWT redis pydantic-settings

# Verify installation
python -c "import src; print('✅ All imports successful')"
```

#### 2. Database Connection Issues
**Problem**: `sqlalchemy.exc.OperationalError` or connection refused

**Solutions**:
- Verify PostgreSQL is running: `pg_ctl status`
- Check database credentials in `.env` file
- Ensure database exists: `createdb bookly_db`
- Test connection: `psql -h localhost -U bookly_user -d bookly_db`

#### 3. Redis Connection Issues  
**Problem**: Redis connection errors

**Solutions**:
- Start Redis server: `redis-server` or `brew services start redis`
- Check Redis is running: `redis-cli ping` (should return "PONG")
- Verify Redis configuration in `.env` file

#### 4. JWT Secret Key Issues
**Problem**: JWT decoding errors

**Solution**:
```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Add the generated key to your .env file as JWT_SECRET
```

#### 5. Migration Issues
**Problem**: Alembic migration errors

**Solutions**:
```bash
# Reset migration history (development only)
alembic downgrade base
alembic upgrade head

# Check current migration status
alembic current

# Manually set migration version (if needed)
alembic stamp head
```

### Performance Tips

1. **Database Connection Pooling**: The application uses SQLModel's built-in connection pooling
2. **Redis for Caching**: Token blacklisting is handled via Redis for fast lookups
3. **Async Operations**: All database operations are asynchronous for better performance
4. **Index Optimization**: Consider adding database indexes for frequently queried fields

## 🧪 Testing

### Manual API Testing

Use the interactive API documentation at `http://localhost:8000/docs` for easy testing, or use curl commands as shown in the examples above.

### Testing with Postman

1. Import the API endpoints into Postman
2. Set up environment variables for:
   - `base_url`: `http://localhost:8000`
   - `access_token`: (obtained from login)
3. Use Bearer token authentication for protected endpoints

### Unit Testing Setup

While this project doesn't include unit tests yet, here's how you could set them up:

```bash
# Install testing dependencies  
pip install pytest pytest-asyncio httpx

# Create test files
mkdir tests
touch tests/__init__.py
touch tests/test_auth.py
touch tests/test_books.py
```

Example test structure:
```python
# tests/test_auth.py
import pytest
from httpx import AsyncClient
from src import app

@pytest.mark.asyncio
async def test_user_registration():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/user/signup", json={
            "first_name": "Test",
            "last_name": "User", 
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        })
    assert response.status_code == 201
```

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

## 🐳 Docker Deployment (Optional)

### Dockerfile

Create a `Dockerfile` for containerizing the application:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY migrations/ ./migrations/
COPY alembic.ini .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

Create a `docker-compose.yml` for local development:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://bookly_user:password123@db:5432/bookly_db
      - JWT_SECRET=your-super-secure-secret-key
      - JWT_ALGORITHM=HS256
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - db
      - redis
    volumes:
      - ./src:/app/src
    command: ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=bookly_db
      - POSTGRES_USER=bookly_user
      - POSTGRES_PASSWORD=password123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Running with Docker

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Reset database
docker-compose down -v && docker-compose up --build
```

## 🌐 Deployment to Production

### Environment Variables for Production

```env
# Production database (use managed database service)
DATABASE_URL=postgresql+asyncpg://user:password@your-db-host:5432/bookly_prod

# Strong JWT secret (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_SECRET=your-very-secure-production-secret-key

# Production Redis (use managed Redis service)
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password

# Optional: Enable CORS for frontend
CORS_ORIGINS=["https://yourdomain.com"]
```

### Production Deployment Checklist

- [ ] Use managed database services (AWS RDS, Google Cloud SQL, etc.)
- [ ] Use managed Redis services (AWS ElastiCache, Redis Cloud, etc.)
- [ ] Set strong, random JWT_SECRET
- [ ] Enable HTTPS/SSL
- [ ] Set up proper CORS origins
- [ ] Configure logging and monitoring
- [ ] Set up automated backups
- [ ] Use environment-specific configuration files
- [ ] Implement health checks
- [ ] Set up CI/CD pipelines

### Recommended Production Stack

- **Hosting**: AWS ECS, Google Cloud Run, or DigitalOcean App Platform
- **Database**: AWS RDS PostgreSQL, Google Cloud SQL, or managed PostgreSQL
- **Cache**: AWS ElastiCache Redis, Redis Cloud, or managed Redis
- **Load Balancer**: AWS ALB, Google Cloud Load Balancer, or Nginx
- **Monitoring**: AWS CloudWatch, Google Cloud Monitoring, or DataDog

## ✅ Installation Verification

After completing the installation steps, run this verification script to ensure everything is set up correctly:

```python
# verification_script.py
import sys

def verify_installation():
    print("🔍 Verifying Bookly installation...")
    
    # Test imports
    try:
        import src
        print("✅ FastAPI application imports successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test configuration
    try:
        from src.config import Config
        print("✅ Configuration loads successfully")
        
        # Check required environment variables
        required_vars = ['DATABASE_URL', 'JWT_SECRET', 'JWT_ALGORITHM', 'REDIS_HOST', 'REDIS_PORT']
        missing_vars = []
        
        for var in required_vars:
            if not hasattr(Config, var) or not getattr(Config, var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
            print("📝 Make sure to configure your .env file")
        else:
            print("✅ All required environment variables are configured")
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    print("\n📋 Installation Summary:")
    print("   ✅ All Python dependencies installed")
    print("   ✅ Application imports successfully")  
    print("   ✅ Configuration system working")
    print("\n🚀 Next steps:")
    print("   1. Set up PostgreSQL database")
    print("   2. Start Redis server")
    print("   3. Configure environment variables in .env")
    print("   4. Run database migrations: alembic upgrade head")
    print("   5. Start the application: uvicorn src:app --reload")
    print("\n📚 For detailed instructions, see the README.md file")
    
    return True

if __name__ == "__main__":
    success = verify_installation()
    sys.exit(0 if success else 1)
```

Run the verification:
```bash
# Quick verification
python -c "
import src
from src.config import Config
print('✅ All imports successful!')
print('✅ FastAPI app created successfully!')
print('✅ Configuration loaded successfully!')
print('📋 Environment variables required:')
print('   - DATABASE_URL (PostgreSQL connection)')
print('   - JWT_SECRET (JWT signing key)')  
print('   - JWT_ALGORITHM (HS256)')
print('   - REDIS_HOST (Redis server host)')
print('   - REDIS_PORT (Redis server port)')
print('📚 Project is ready for development!')
"
```

If you see all checkmarks (✅), your installation is complete and ready for development!

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