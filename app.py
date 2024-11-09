
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship




app = Flask(__name__)
app.config['SECRET_KEY'] = 'baffvdvdzxcdfvv654524vbg54fb4'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# id tittle price isActive
# 1  corm    200   true
# 2  game    300   flass




# User model
# id
# username
# name
# email
# password

# User модель с каскадным удалением отзывов
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # Связь с отзывами, с каскадным удалением
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')




@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')










# Каталог

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Кошки, собаки, птицы и т.д.
    is_active = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(300), nullable=True)

@app.route('/shop')
@app.route('/shop/<category>')
def shop(category=None):
    categories = ['Кошки', 'Собаки', 'Птицы', 'Ящерицы', 'Грызуны']
    products_count = {cat: Product.query.filter_by(category=cat, is_active=True).count() for cat in categories}

    if category:
        products = Product.query.filter_by(category=category, is_active=True).all()
    else:
        products = Product.query.filter_by(is_active=True).all()

    return render_template('shop.html', products=products, categories=categories, products_count=products_count)


# Add product


# @app.route("/cotolog")
# def cotolog():
#     return render_template('shop.html')




# Admin panel

# didn't worj let's debug
# class PetProduct(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)  # Ensure this line exists
#     price = db.Column(db.Float, nullable=False)
#     category = db.Column(db.String(50), nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     is_active = db.Column(db.Boolean, default=True)  # Ensure this line exists
#
#
#
# @app.route('/add_product', methods=['POST'])
# def add_product():
#     name = request.form.get('name')
#     price = request.form.get('price')
#     category = request.form.get('category')
#     description = request.form.get('description')
#
#     # Create a new instance of PetProduct
#     new_product = PetProduct(name=name, price=price, category=category, description=description)
#
#     # Add to the session and commit
#     db.session.add(new_product)
#     db.session.commit()
#
#     return redirect(url_for('add_product'))









# @app.route("/register")
# def register():
#     return render_template('register.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        if password != password_confirm:
            flash('Пароли не совподают!')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, name=name, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except:
            flash('User already exists!')
            return redirect(url_for('register'))

    return render_template('register.html')







@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            if remember:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!')

    return render_template('login.html')









#
# @app.route("/login_handler", methods=['POST'])
# def login_handler():
#     # Логика для обработки входа
#     # Если вы используете его, убедитесь, что форма также отправляет запрос на этот маршрут
#
#


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы вышли из аккаунта')
    return redirect(url_for('index'))



@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Пожалуйста, войдите, чтобы получить доступ к профилю.')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        if 'delete_account' in request.form:
            db.session.delete(user)  # Удаление пользователя
            db.session.commit()
            session.pop('user_id', None)  # Выход из аккаунта после удаления
            flash('Ваш аккаунт был успешно удален.')
            return redirect(url_for('index'))
        else:
            user.name = request.form.get('name')
            user.email = request.form.get('email')
            db.session.commit()
            flash('Профиль успешно обновлен!')

    return render_template('profile.html', user=user)
# Отзывы




# Модель Review с внешним ключом на пользователя
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', back_populates='reviews')


















@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Please log in to leave a review.')
            return redirect(url_for('login'))

        content = request.form.get('content')
        if content:
            new_review = Review(user_id=session['user_id'], content=content)
            db.session.add(new_review)
            db.session.commit()
            flash('Your review has been submitted!')
        else:
            flash('Review content cannot be empty.')

    all_reviews = Review.query.order_by(Review.date_created.desc()).all()
    return render_template('reviews.html', reviews=all_reviews)




# Uchebnik

@app.route('/booking')
def booking():
    return render_template('booking.html')


# Quiz


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Получение ответов пользователя из формы
        activity_level = request.form.get('activity-level')
        space_available = request.form.get('space-available')
        allergies = request.form.get('allergies')
        time_available = request.form.get('time-available')

        # Определение подходящего питомца и изображения на основе ответов
        suggestion = ''
        image_url = ''
        if activity_level == 'high' and space_available == 'large' and allergies == 'no':
            suggestion = 'Собака может быть идеальным питомцем для вас! Они любят активные прогулки и нуждаются в пространстве для игр.'
            image_url = '/static/img/dog.gif'
        elif activity_level == 'medium' and space_available != 'small':
            suggestion = 'Кошка может стать отличным компаньоном. Они умеренно активны и адаптируются к различным условиям.'
            image_url = '/static/img/cat.gif'
        elif allergies == 'yes':
            suggestion = 'Рассмотрите возможность завести гипоаллергенного питомца, например, ящерицу или рыбку.'
            image_url = '/static/img/snail.gif'
        elif space_available == 'small' and time_available == 'little':
            suggestion = 'Маленькие питомцы, такие как хомяки, мыши или птицы, могут быть подходящими, так как не требуют много места и времени.'
            image_url = '/static/img/mouse.gif'
        else:
            suggestion = 'Возможно, вам подойдут птицы или мелкие млекопитающие, такие как кролики или морские свинки, которые требуют умеренной активности и пространства.'
            image_url = '/static/img/bird.gif'

        return render_template('quiz_result.html', suggestion=suggestion, image_url=image_url)

    return render_template('quiz.html')









if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц в базе данных
    app.run(debug=True)




