# 🌐 IraqiCode Website

A modern, bilingual educational website built using **Flask** that allows users to explore programming-related content, products, blog posts, and interact via contact and admin features.

---

## 📌 Project Overview

**IraqiCode** is a full-featured web application aimed at supporting coding education in both Arabic and English. It provides:

- 🔍 Product display with filter and detail view  
- 🛒 Basic shopping cart system  
- 📊 Dashboard for product analytics  
- 📝 Blog section with author and date  
- 🌍 Multilingual support (English/Arabic)  
- 🔐 Admin panel for managing products  
- 💬 Comment system  
- 📱 Mobile responsive layout  
- 📧 Contact form with email integration  
- 🚀 Deployment-ready (Railway/GitHub)

---

## 🛠️ Technologies Used

| Technology        | Purpose                               |
|------------------|----------------------------------------|
| Flask            | Web framework (Python)                 |
| Flask-SQLAlchemy | Database ORM with SQLite               |
| Flask-Login      | User authentication                    |
| Flask-Mail       | Send contact messages via Gmail SMTP   |
| Flask-WTF        | Secure and clean form handling         |
| Flask-Babel      | Language localization (ar/en)          |
| Bootstrap 5      | Responsive UI design                   |
| Jinja2           | Template rendering                     |
| Chart.js         | Dashboard analytics chart              |
| Gunicorn         | Production WSGI server                 |

---

## 🧱 Main Features

- 🏠 Home, About, Services, Projects, Products, Blog, Contact pages
- ✍️ Admin panel: Add, edit, delete products
- 📂 Category filtering on products
- 🛍️ Add to cart + cart preview in navbar
- 📧 Contact form with live email support
- 🌐 Language switcher with Arabic RTL support
- 📊 Dashboard with total product count and graph
- 💬 Product comments system
- 🖼️ Product images with fallback
- ✨ Modern design with clean UI

---

## 🚀 How to Run Locally

1. Clone the repo:
```bash
git clone https://github.com/yourusername/iraqicode-website.git
cd iraqicode-website

1- Create virtual environment and activate:
python -m venv venv
venv\Scripts\activate

2- Install requirements:
pip install -r requirements.txt

3-Run the app:
python app.py

🌐 How to Deploy to Railway

1-Push your project to GitHub

2-Create Procfile:
web: gunicorn app:app

3-Connect Railway to GitHub

4-Click "Deploy"

5-Done!

💡 Future Ideas
- Full user registration & login

- Payment integration (Stripe/PayPal)

- Interactive programming quizzes

- API backend (RESTful)

- Enhanced product reviews & ratings

- Better mobile support and PWA

👤 Developed by
Name: [HUSSEIN MASHAAN METEAB]
Email: hussmash2@gmail.com
Project: IraqiCode
Supervised by: Prof. [Dr. FÜLEP Dávid]











