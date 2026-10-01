
# Online Doctor Appointment System

The Online Doctor Appointment System is a platform that allows users to book appointments with doctors, manage their accounts, and search for doctors. Admins can update doctor information, and users can fund their wallets. The system is secured using OTP authentication via **pyotp** and integrates with Google services.

## Features

- User Registration & Login
- Doctor Search & Booking
- Wallet Management
- Reviews for Doctors
- Secure OTP-only Login (via pyotp)
- Admin Panel for Managing Doctors
- Integrated Google Services

---

## Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-repo/online-doctor-appointment.git
cd online-doctor-appointment
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a .env file in the root directory with the following content:

```
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost, 127.0.0.1

# PostgreSQL configuration
POSTGRES_DB=mydb
POSTGRES_USER=user
POSTGRES_PASSWORD=password
DATABASE_URL=postgres://user:password@db:5432/mydb

# Google API credentials
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### 4. Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the project

```bash
python manage.py runserver
```

Or using Docker:

```bash
docker-compose up --build
```

---

## Running Tests

This project uses **Django's test framework** for unit tests. You can run all the tests using the following command:

```bash
python manage.py test
```

---

## Docker Setup

If you prefer running the project with Docker, use the following setup:

1. Ensure Docker and Docker Compose are installed on your system.
2. Run the app using Docker Compose:

```bash
docker-compose up --build
```

3. The app will be available at `http://localhost:8000`.

### Dockerfile:

```Dockerfile
# Base image
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project_name.wsgi:application"]
```

### docker-compose.yml:

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn --bind 0.0.0.0:8000 your_project_name.wsgi:application
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
  db:
    image: postgres
    environment:
      POSTGRES_DB=mydb
      POSTGRES_USER=user
      POSTGRES_PASSWORD=password
```
