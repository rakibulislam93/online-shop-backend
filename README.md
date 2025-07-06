# 🛒 Kinakata.com — eCommerce Backend (Django REST Framework)

**Kinakata.com** is a complete eCommerce backend solution developed using **Django REST Framework (DRF)**. It provides a secure, scalable, and role-based API system, making it easy to build and integrate with any modern frontend like React, Vue, or plain HTML/JS.

The backend supports **three user roles** with distinct features and dashboards:

- **Admin** — full control over the platform
- **Seller** — manage own products and orders
- **Customer** — browse, order, and view purchase history

> 📁 **Frontend Repo:** [Kinakata Frontend](https://github.com/rakibulislam93/online-shop-frontend)

---

## 🚀 Features

### 🧑‍💼 Admin Features
- Full-featured admin dashboard
- Manage all users (admins, sellers, customers)
- CRUD operations on all products
- View and manage all orders
- Platform moderation

### 🛍️ Seller Features
- Dedicated seller dashboard
- CRUD operations on **own products**
- View & track orders on own products
- Inventory management

### 👤 Customer Features
- Secure registration & login system
- Browse products by category or search
- View product details
- Place orders & view order history
- JWT-based authentication

---

## 🛠️ Technology Stack

- **Backend:** Django, Django REST Framework (DRF)  
- **Frontend:** HTML, CSS, Vanilla JavaScript *(separate repo)*  
- **Database:** PostgreSQL / SQLite3 (default)  
- **Deployment:** Render.com (Backend), Supabase (PostgreSQL)  

---

## 📚 API Documentation

- Swagger UI: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- Redoc UI: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)

---

## ⚙️ Installation & Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/rakibulislam93/online-shop-backend.git
cd online-shop-backend


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
   
# Example .env file
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Email Config
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password

# PostgreSQL DB config (if used)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
   
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
   
