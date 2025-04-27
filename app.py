from flask import Flask, render_template, request, redirect, url_for, flash
from flask_babel import Babel, _
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

# إعداد التطبيق
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # غيّرها عند رفع الموقع

# إعداد اللغات
babel = Babel(app)

LANGUAGES = {
    'en': 'English',
    'ar': 'Arabic'
}

# إعداد قاعدة البيانات
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# إعداد تسجيل الدخول
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# موديل المنتج
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'

# تعريف مستخدم وهمي
class User(UserMixin):
    id = 1
    username = "admin"
    password = "admin123"

# تحميل المستخدم
@login_manager.user_loader
def load_user(user_id):
    if user_id == "1":
        return User()
    return None

# نموذج الاتصال
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send')

# نموذج المنتج
class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    price = StringField('Price', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[Length(max=200)])
    submit = SubmitField('Save')

# تحديد اللغة
@app.context_processor
def inject_lang():
    return dict(current_lang=get_locale())

@babel.localeselector
def get_locale():
    return request.args.get('lang') or 'en'

# الصفحات الأساسية
@app.route('/')
def index():
    return render_template('index.html', page_title=_('IraqiCode - Learn Programming'), page_description=_('Learn programming and web development easily with IraqiCode.'))

@app.route('/services')
def services():
    return render_template('services.html', page_title=_('Our Services - IraqiCode'), page_description=_('Discover our professional programming and web development services.'))

@app.route('/projects')
def projects():
    return render_template('projects.html', page_title=_('Our Projects - IraqiCode'), page_description=_('Browse our successful projects and collaborations.'))

@app.route('/about')
def about():
    return render_template('about.html', page_title=_('About Us - IraqiCode'), page_description=_('Learn more about the mission and vision of IraqiCode.'))

@app.route('/blog')
def blog():
    return render_template('blog.html', page_title=_('Blog - IraqiCode'), page_description=_('Read the latest articles and tips in programming and web development.'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash(_('Your message has been sent successfully!'), 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form, page_title=_('Contact Us - IraqiCode'), page_description=_('Get in touch with us for any inquiries or collaborations.'))

# لوحة التحكم Admin
@app.route('/admin')
@login_required
def admin():
    products = Product.query.all()
    return render_template('admin.html', products=products, page_title=_('Dashboard - IraqiCode'), page_description=_('Manage your products and content easily from the dashboard.'))

# إضافة منتج
@app.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=float(form.price.data),
            image_url=form.image_url.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash(_('Product added successfully!'), 'success')
        return redirect(url_for('admin'))
    return render_template('add_product.html', form=form, page_title=_('Add Product - IraqiCode'), page_description=_('Add new products to your store easily.'))

# تعديل منتج
@app.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = float(form.price.data)
        product.image_url = form.image_url.data
        db.session.commit()
        flash(_('Product updated successfully!'), 'success')
        return redirect(url_for('admin'))
    return render_template('edit_product.html', form=form, product=product, page_title=_('Edit Product - IraqiCode'), page_description=_('Edit your product details easily.'))

# حذف منتج
@app.route('/delete-product/<int:product_id>', methods=['GET'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(_('Product deleted successfully!'), 'success')
    return redirect(url_for('admin'))

# عرض جميع المنتجات
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products, page_title=_('Our Products - IraqiCode'), page_description=_('Explore our range of professional products.'))

# ✅ عرض تفاصيل منتج مع منتجات مشابهة
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter(Product.id != product_id).limit(3).all()

    return render_template(
        'product_detail.html',
        product=product,
        related_products=related_products,
        page_title=f"IraqiCode - {product.name}",
        page_description=product.description[:150]
    )

# تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "admin" and password == "admin123":
            user = User()
            login_user(user)
            flash(_('Logged in successfully!'), 'success')
            return redirect(url_for('admin'))
        else:
            flash(_('Invalid username or password'), 'danger')

    return render_template('login.html', page_title=_('Login - IraqiCode'), page_description=_('Access your admin dashboard securely.'))

# تسجيل الخروج
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('Logged out successfully!'), 'info')
    return redirect(url_for('login'))

# صفحة الخطأ 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', page_title=_('404 - Page Not Found'), page_description=_('Sorry, the page you are looking for does not exist.')), 404

# تفعيل الكاش
@app.after_request
def add_header(response):
    response.cache_control.max_age = 2592000
    response.cache_control.public = True
    return response

# تشغيل التطبيق
if __name__ == "__main__":
    app.run(debug=True)
