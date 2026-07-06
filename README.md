# ERP Backend Auth API

This project provides a Django REST API with JWT-based authentication and an ERP-style module layer for:
- signup
- login
- forgot password
- reset password
- protected dashboard access
- token refresh
- logout
- employees CRUD
- leads CRUD
- vendors CRUD
- products CRUD
- invoices CRUD
- projects CRUD
- Meta ad campaign simulation from the dashboard

## Requirements
- Python 3.9+
- Django 4.2+
- Django REST Framework
- djangorestframework-simplejwt

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Authentication Endpoints

Base URL:
```text
http://127.0.0.1:8000/auth/
```

### 1. Signup
- Method: POST
- Path: `/auth/signup/`
- Body:
  ```json
  {
    "email": "user@example.com",
    "password": "StrongPass123!",
    "full_name": "John Doe"
  }
  ```

### 2. Login
- Method: POST
- Path: `/auth/login/`
- Body:
  ```json
  {
    "email": "user@example.com",
    "password": "StrongPass123!"
  }
  ```

### 3. Forgot Password
- Method: POST
- Path: `/auth/forgot-password/`
- Body:
  ```json
  {
    "email": "user@example.com"
  }
  ```

### 4. Reset Password
- Method: POST
- Path: `/auth/reset-password/`
- Body:
  ```json
  {
    "email": "user@example.com",
    "token": "<reset_token>",
    "new_password": "NewStrongPass123!"
  }
  ```

### 5. Protected Dashboard
- Method: GET
- Path: `/auth/dashboard/`
- Header:
  ```http
  Authorization: Bearer <access_token>
  ```

### 6. Refresh Token
- Method: POST
- Path: `/auth/token/refresh/`
- Body:
  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```

### 7. Logout
- Method: POST
- Path: `/auth/logout/`
- Body:
  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```

## ERP Modules

The app now includes module pages and REST APIs for:
- Employees: `/api/employees/`
- Leads: `/api/leads/`
- Vendors: `/api/vendors/`
- Products: `/api/products/`
- Customers: `/api/customers/`
- Orders: `/api/orders/`
- Inventory: `/api/inventory/`
- Reports: `/api/reports/`
- Invoices: `/api/invoices/`
- Projects: `/api/projects/`

You can also open the ERP-style module pages in the browser at:
- `/modules/employees/`
- `/modules/leads/`
- `/modules/vendors/`
- `/modules/products/`
- `/modules/customers/`
- `/modules/orders/`
- `/modules/inventory/`
- `/modules/reports/`
- `/modules/invoices/`
- `/modules/projects/`

The dashboard reads live counts, recent products, orders, inventory, employees, and leads from the database.

## Testing

Run the full test suite:
```bash
python manage.py test erp_modules accounts
```

You can also test the API live with Postman using the collection file:
- [postman_collection.json](postman_collection.json)
