# Kinakata.com

## Project Description
Kinakata.com is a complete eCommerce backend solution developed using Django REST Framework (DRF). It offers a secure, scalable, and role-based API system for building a full-featured online shopping platform.
The project is designed to support three user roles: Admin, Seller, and Customer—each with separate dashboards and permissions. Admins can manage the entire platform, sellers can manage their own products and orders, and customers can browse products and place orders. This modular architecture makes it easy to integrate with any modern frontend (React, Vue, Next.js, etc.).

🚀 Features
🧑‍💼 Admin Features

## Full-featured admin dashboard
## Manage all users: admins, sellers, and customers
## Perform CRUD operations on all products
## View and manage all customer orders
## Platform moderation and system-wide access

🛍️ Seller Features

## Dedicated seller dashboard
## Perform CRUD operations only on their own products
## Track orders made on their products
## View and manage their inventory

👤 Customer Features

## Secure registration and login system
## Browse products by category or search
## View detailed product information
## Place orders and view personal order history
## JWT-based authentication for safe and smooth API usage

🛠️ Technology Stack
## Backend : Django,Django Rest Framework (DRF)
## Frontend : HTML,css,Vanilla JS
## Database : PostgreSQL, Default(sqlite3)
## Deployment : Render.com , Supabase(for postgres DB)

###API Documentation
http://127.0.0.1:8000/api/docs/
http://127.0.0.1:8000/api/redoc/

🧩 Installation & Setup Guide

1. Clone the Repository
    git clone https://github.com/rakibulislam93/online-shop-backend.git
    cd online-shop-backend
2. Create Virtual environment :
     python -m venv venv
  #.....Activate it......#
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
3. Install Dependencies :
   
     pip install -r requirements.txt
   
5. Create .env file :
   <details>
       <summary>📄 Create `.env` File</summary>
       EMAIL_HOST_USER=your_email_name
        EMAIL_HOST_PASSWORD=your_email_password

    DB_NAME=your_postgres_db_name
    DB_USER=your_postgres_user
    DB_PASSWORD=your_postgres_password
    DB_HOST=your_db_host
    DB_PORT=your_db_port

   OPENROUTER_API_KEY=your_deepseek_api_key
   </details>
   
7. Apply Migrations :
   python manage.py makemigrations
   python manage.py migrate
8. Create Superuser :
   python manage.py createsuperuser
   
9. Run the Development Server : 
   **python manage.py runserver**

## 👤 Author

**Rakibul Islam**  
🔗 [GitHub](https://github.com/rakibulislam93) 
   
