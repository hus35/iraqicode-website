from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # تحقق إذا كان موجود
    existing_user = User.query.filter_by(username='admin').first()
    if not existing_user:
        admin = User(
            username='admin',
            password=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created.")
    else:
        print("⚠️ Admin already exists.")
