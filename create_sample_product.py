from app import app, db, Product

with app.app_context():
    p = Product(
        name='Smart Speaker',
        description='A high-quality smart speaker with voice control.',
        price=59.99,
        image_url='static/images/smart_speaker.png',
        category='Electronics'
    )
    db.session.add(p)
    db.session.commit()
    print("✅ Sample product added successfully.")
