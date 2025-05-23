# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/products.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # إعدادات البريد لإرسال الرسائل عبر Gmail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'بريدك@gmail.com'
    MAIL_PASSWORD = 'كلمة مرور التطبيقات الخاصة بك'
