# Manufacturing Marketplace Backend

A comprehensive B2B marketplace platform for manufacturers to trade surplus and dead stock inventory.

## 🚀 Features

- **User Management**: Registration, authentication with JWT tokens
- **Product Listings**: Full CRUD operations with image upload
- **Advanced Search**: Filter by category, material, location, price range
- **Messaging System**: Buyer-seller communication with offer negotiation
- **Admin Panel**: User verification, product moderation, analytics
- **Image Processing**: Automatic thumbnail generation
- **Security**: Password hashing, JWT tokens, input validation

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Virtual environment tool (venv, virtualenv, or conda)

## 🔧 Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd manufacturing_marketplace_backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

Create PostgreSQL database:
```sql
CREATE DATABASE marketplace_db;
CREATE USER marketplace_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE marketplace_db TO marketplace_user;
```

### 5. Environment Configuration

Create `.env` file from template:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
DATABASE_URL=postgresql://marketplace_user:your_password@localhost:5432/marketplace_db
SECRET_KEY=your-super-secret-key-minimum-32-characters
```

### 6. Initialize Database
```bash
python init_db.py
```

### 7. Create Sample Data (Optional)
```bash
python create_sample_data.py
```

## 🏃 Running the Application

### Development Mode
```bash
python run_server.py
```
Or:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## 🧪 Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## 📁 Project Structure

```
manufacturing_marketplace_backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py           # Authentication endpoints
│   │       ├── users.py          # User management
│   │       ├── products.py       # Product CRUD
│   │       ├── categories.py     # Categories & materials
│   │       ├── conversations.py  # Messaging system
│   │       └── admin.py          # Admin panel
│   ├── core/
│   │   ├── dependencies.py       # Dependency injection
│   │   ├── exceptions.py         # Custom exceptions
│   │   ├── logging.py           # Logging configuration
│   │   └── security.py          # Security utilities
│   ├── models/                  # SQLAlchemy models
│   ├── schemas/                 # Pydantic schemas
│   ├── services/                # Business logic
│   ├── utils/                   # Utility functions
│   ├── config.py               # Configuration
│   ├── database.py             # Database setup
│   └── main.py                 # FastAPI application
├── tests/                      # Test files
├── uploads/                    # File storage
├── logs/                       # Application logs
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔐 Security

- Passwords hashed with bcrypt
- JWT tokens for authentication
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy ORM
- File upload validation
- CORS configuration
- Rate limiting (recommended for production)

## 🚀 Deployment

### Using Docker (Recommended)

See `docker-compose.yml` for container setup.

```bash
docker-compose up -d
```

### Manual Deployment

1. Set up PostgreSQL database
2. Configure environment variables
3. Run database migrations
4. Start application with production WSGI server
5. Set up reverse proxy (nginx)
6. Configure SSL certificates
7. Set up monitoring and logging

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `GET /api/v1/users/{user_id}` - Get user profile

### Products
- `POST /api/v1/products/` - Create product
- `GET /api/v1/products/` - List/search products
- `GET /api/v1/products/{id}` - Get product details
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product
- `POST /api/v1/products/{id}/images` - Upload images

### Categories
- `GET /api/v1/categories/` - List categories
- `GET /api/v1/categories/materials` - List materials

### Conversations
- `POST /api/v1/conversations/` - Start conversation
- `GET /api/v1/conversations/` - List conversations
- `GET /api/v1/conversations/{id}` - Get conversation
- `POST /api/v1/conversations/{id}/messages` - Send message

### Admin
- `GET /api/v1/admin/dashboard` - Dashboard statistics
- `GET /api/v1/admin/users` - List all users
- `PUT /api/v1/admin/users/{id}/verify` - Verify user
- `PUT /api/v1/admin/users/{id}/deactivate` - Deactivate user