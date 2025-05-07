from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_babel import Babel, _
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import IntegerField
from datetime import datetime
from flask_babel import get_locale as babel_get_locale
from flask import session



import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hussmash2@gmail.com'
app.config['MAIL_PASSWORD'] = 'xgeu ouyq ndrq zpkf'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['SESSION_TYPE'] = 'filesystem'
babel = Babel(app)

db = SQLAlchemy(app)
mail = Mail(app)
babel = Babel(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class ContactForm(FlaskForm):
    name = StringField(_('Name'), validators=[DataRequired()])
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    message = TextAreaField(_('Message'), validators=[DataRequired()])
    submit = SubmitField(_('Send'))

class ProductForm(FlaskForm):
    name = StringField(_('Product Name'), validators=[DataRequired()])
    description = TextAreaField(_('Description'), validators=[DataRequired()])
    price = DecimalField(_('Price'), validators=[DataRequired()])
    image_url = StringField(_('Image URL'))
    category = StringField(_('Category'))  # ✅ مضاف سابقاً
    rating = IntegerField(_('Rating'))     # ⭐ جديد
    submit = SubmitField(_('Add Product'))

class LoginForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    submit = SubmitField(_('Login'))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(300), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    rating = db.Column(db.Integer, default=0)  # ⭐ جديد

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product', backref=db.backref('comments', cascade='all, delete-orphan'))

class CommentForm(FlaskForm):
    username = StringField(_('Name'), validators=[DataRequired()])
    content = TextAreaField(_('Comment'), validators=[DataRequired()])
    submit = SubmitField(_('Submit Comment'))

@babel.localeselector
def get_locale():
    return request.args.get('lang') or 'en'

@app.before_request
def set_language():
    g.lang = get_locale()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/products')
def products():
    selected_category = request.args.get('category', 'all')

    if selected_category == 'all':
        products = Product.query.all()
    else:
        products = Product.query.filter_by(category=selected_category).all()

    # استخراج التصنيفات الفريدة من قاعدة البيانات
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]  # تأكد من تجاهل None أو الفارغ

    return render_template(
        'products.html',
        products=products,
        categories=categories,
        selected_category=selected_category
    )

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter(Product.id != product.id).limit(3).all()

    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(
            username=form.username.data,
            content=form.content.data,
            product_id=product.id
        )
        db.session.add(new_comment)
        db.session.commit()
        flash(_('Comment added successfully!'), 'success')
        return redirect(url_for('product_detail', product_id=product.id))

    comments = Comment.query.filter_by(product_id=product.id).order_by(Comment.created_at.desc()).all()
    return render_template('product_detail.html', product=product, related_products=related_products,
                           form=form, comments=comments)

@app.route('/blog')
def blog():
    posts = [
        {
            'title': 'First Post',
            'author': 'Admin',
            'content': 'This is a short intro to the post.',
            'image': '/static/img/blog1.jpg',
            'date': datetime(2024, 5, 1)
        },
        {
            'title': 'Second Post',
            'author': 'User',
            'content': 'Another great blog article here.',
            'image': '/static/img/blog2.jpg',
            'date': datetime(2024, 5, 2)
        }
    ]
    return render_template('blog.html', posts=posts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            msg = Message('New Contact Message', sender=form.email.data, recipients=['your_email@gmail.com'])
            msg.body = f"Name: {form.name.data}\nEmail: {form.email.data}\n\nMessage:\n{form.message.data}"
            mail.send(msg)
            flash(_('Your message has been sent successfully!'), 'success')
            return redirect(url_for('contact', lang=g.get('lang', 'en')))
        except Exception as e:
            print(e)
            flash(_('An error occurred. Please try again later.'), 'danger')
    return render_template('contact.html', form=form)

@app.route('/admin')
@login_required
def admin():
    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image_url=form.image_url.data,
            category=form.category.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash(_('Product added successfully!'), 'success')
        return redirect(url_for('admin', lang=g.get('lang', 'en')))
    return render_template('add_product.html', form=form)

@app.route('/delete-product/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(_('Product deleted successfully!'), 'success')
    return redirect(url_for('admin', lang=g.get('lang', 'en')))

@app.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.image_url = form.image_url.data
        product.category = form.category.data
        db.session.commit()
        flash(_('Product updated successfully!'), 'success')
        return redirect(url_for('admin', lang=g.get('lang', 'en')))
    return render_template('edit_product.html', form=form, product=product)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(_('Welcome back!'), 'success')
            return redirect(url_for('dashboard'))

        else:
            flash(_('Invalid username or password'), 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    total_products = Product.query.count()
    categories = db.session.query(Product.category).distinct().count()
    latest_product = Product.query.order_by(Product.id.desc()).first()

    # بيانات التصنيفات وعدد المنتجات لكل تصنيف
    category_data = db.session.query(Product.category, db.func.count(Product.id)).group_by(Product.category).all()
    chart_labels = [cat[0] for cat in category_data]
    chart_counts = [cat[1] for cat in category_data]

    return render_template('dashboard.html',
                           total_products=total_products,
                           categories=categories,
                           latest_product=latest_product,
                           chart_labels=chart_labels,
                           chart_counts=chart_counts)


@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
        session['cart'] = cart
        flash(_('Product added to cart!'), 'success')
    return redirect(url_for('products'))

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    products = Product.query.filter(Product.id.in_(cart)).all()
    return render_template('cart.html', products=products)

@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
        session['cart'] = cart
        flash(_('Product removed from cart.'), 'info')
    return redirect(url_for('cart'))

@app.route('/analytics')
@login_required
def analytics():
    product_count = Product.query.count()
    categories = db.session.query(Product.category, db.func.count(Product.id)).group_by(Product.category).all()

    category_labels = [c[0] for c in categories]
    category_counts = [c[1] for c in categories]

    return render_template('analytics.html', 
                           product_count=product_count,
                           category_labels=category_labels, 
                           category_counts=category_counts)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('You have been logged out.'), 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
