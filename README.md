# Product Fusion - AuthService

This application provides a robust authentication and organization management system for a multi-tenant SaaS platform.
It offers user authentication, organization creation, member management, and role-based access control, along with
statistical insights and email notifications for key user actions.


# Running the Project in Local

1. Add an `.env` file

```env
# Application settings
HOST=0.0.0.0
PORT=8000
WORKERS_COUNT=1
RELOAD=False
ENVIRONMENT=DEV
LOG_LEVEL=INFO

# OpenTelemetry settings
OPENTELEMETRY_ENDPOINT=

# Database settings
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/product_fusion

# Security settings
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=1440
JWT_ALGORITHM=HS256
REFRESH_TOKEN_EXPIRE_DAYS=30

# SMTP settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USERNAME=your_smtp_username_here
SMTP_PASSWORD=your_smtp_password_here
```

2. Install poetry

```bash
pip3 install --upgrade pip && pip3 install poetry
```

3. Install dependencies

```bash
poetry install
```

4. Run the project

```bash
hypercorn product_fusion_backend.web.application:pf_app --reload --bind "0.0.0.0:8000"
```
