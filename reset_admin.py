from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # حذف كل المستخدمين من الجدول
    db.session.execute(db.delete(User))
    db.session.commit()
    print("🗑️ تم حذف جميع المستخدمين!")

    # إنشاء مستخدم أدمن جديد
    admin = User(
        username='admin',
        password=generate_password_hash('admin123')  # كلمة السر مشفرة
    )
    db.session.add(admin)
    db.session.commit()
    print("✅ تمت إضافة مستخدم أدمن جديد بنجاح (admin / admin123)")
