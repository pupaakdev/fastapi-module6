# FastAPI User Authentication Backend

A production-ready FastAPI backend with PostgreSQL database, JWT authentication, and user management capabilities.

## Features

- **User Registration** - Create new user accounts with unique usernames and emails
- **User Login** - Secure authentication with JWT tokens
- **Password Security** - Bcrypt hashing for secure password storage
- **Protected Routes** - Endpoints accessible only to authenticated users
- **User Management** - List all users and delete users by ID
- **Environment Configuration** - Database credentials managed via environment variables

## Tech Stack

- **Backend Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens)
- **Password Hashing:** Bcrypt
- **Environment Variables:** python-dotenv

## Prerequisites

- Python 3.11
- PostgreSQL database
- pip or poetry

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pupaakdev/fastapi-module6
cd fastapi-module6
```

2. Create a virtual environment:
```bash
python -m venv venv
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables by creating a `.env` file:
```env
DB_USER=postgres
DB_PASS=your_password
```

## Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The server will run at `http://localhost:8000`

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/users/register` | Register a new user | No |
| POST | `/users/login` | Login and get access token | No |
| GET | `/users/` | Get all users | Yes |
| DELETE | `/users/{id}` | Delete user by ID | Yes |

### Root

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message and routes list |

## Request/Response Examples

### Register User
```json
POST /users/register
Content-Type: application/json

{
    "username": "john_doe",
    "fullname": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response:**
```json
{
    "username": "john_doe",
    "email": "john@example.com"
}
```

### Login
```json
POST /users/login
Content-Type: application/json

{
    "username": "john_doe",
    "password": "securepassword123"
}
```

**Response:**
```json
{
    "message": "Login successful!",
    "username": "john_doe",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access_token_type": "bearer"
}
```

### Get All Users
```json
GET /users/
Authorization: Bearer <access_token>
```

**Response:**
```json
[
    {
        "id": 1,
        "username": "john_doe",
        "fullname": "John Doe",
        "email": "john@example.com",
        "hashed_password": "$2b$12$..."
    }
]
```

## Project Structure

```
├── README.md
├── main.py              # FastAPI application entry point
├── database.py          # Database connection and session management
├── utils.py             # Password hashing and JWT utilities
├── models/
│   └── user.py          # SQLAlchemy models and Pydantic schemas
├── routers/
│   └── users.py         # User authentication routes
├── .env                 # Environment variables (create this)
└── requirements.txt     # Python dependencies
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_USER` | postgres | PostgreSQL username |
| `DB_PASS` | postgres | PostgreSQL password |

## Security Notes

- Passwords are hashed using bcrypt before storage
- JWT tokens expire after 30 minutes by default
- Protected routes require valid Bearer tokens
- Username and email must be unique

## License

MIT License