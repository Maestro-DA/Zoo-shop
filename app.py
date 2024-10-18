# from flask import Flask, render_template, request, redirect
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, current_user
# from flask_login import UserMixin
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# # id tittle price isActive
# # 1  corm    200   true
# # 2  game    300   flass
#
# # тут
# # class Item(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     title = db.Column(db.String(100), nullable=False)
# #     price = db.Column(db.Integer, nullable=False)
# #     isActive = db.Column(db.Boolean, default=True)
# #     # text = db.Column(db.Text, nullable=False)
# #
# #
# #
# # # Нужно добавить отзывы пользователей через это
# # class Post(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     title = db.Column(db.String(300), nullable=False)
# #     text = db.Column(db.Text, nullable=False)
#
#
#
#
# @app.route('/index')
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
#
# @app.route("/create", methods=['POST', 'GET'])
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         text = request.form['text']
#
#         post = Post(title=title, text=text)
#
#         try:
#             db.session.add(post)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'Something wrong!'
#     else:
#         return render_template('create.html')
#
#
# @app.route("/cotolog")
# def cotolog():
#     return render_template('cotolog.html')
#
#
# @app.route("/register")
# def register():
#     return render_template('register.html')
#
#
# @app.route("/login")
# def login():
#     return render_template('login.html')
#
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# id tittle price isActive
# 1  corm    200   true
# 2  game    300   flass

# тут
# class Item(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     isActive = db.Column(db.Boolean, default=True)
#     # text = db.Column(db.Text, nullable=False)
#
#
#
# # Нужно добавить отзывы пользователей через это
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(300), nullable=False)
#     text = db.Column(db.Text, nullable=False)




@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/create", methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        post = Post(title=title, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return 'Something wrong!'
    else:
        return render_template('create.html')


@app.route("/cotolog")
def cotolog():
    return render_template('cotolog.html')


@app.route("/register")
def register():
    return render_template('register.html')


@app.route("/login")
def login():
    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)




