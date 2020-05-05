from data import db_session
from data import users
from data import products
from data import review
from data import orders
import datetime
from flask import Flask, make_response, request, redirect, render_template, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from loginform import LoginForm, RegisterForm, NewsForm, ReviewForm
from werkzeug.exceptions import abort
import news_resources
from flask_restful import Api
from check import check_order, const, check_True

courier_password = str(open('courier_password', 'r').read())

app = Flask(__name__)

# защита от межсайтовой подделки запросов
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


@app.route("/")
@app.route("/main")
def head():
    return render_template('main.html', courier_password=courier_password)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # проверка на валидацию
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/main")


def all_news(type):
    session = db_session.create_session()
    if type == 'products':
        news = session.query(products.Products)
    else:
        news = session.query(review.Reviews)
    return news


def add_news(type):
    form = NewsForm()
    if type == 'review':
        form = ReviewForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        news = products.Products()
        if type == 'review':
            news = review.Reviews()
        news.title = form.title.data
        news.content = form.content.data
        if type == 'product':
            news.prices = form.prices.data
            current_user.products.append(news)
        else:
            current_user.review.append(news)
        session.merge(current_user)
        session.commit()


@app.route("/products")
def all_products():
    if current_user.is_authenticated:
        return render_template("all_news.html", news=all_news('products'), page="Продукты",
                               type="Добавление продукта", courier_password=courier_password)


@app.route('/product', methods=['GET', 'POST'])
@login_required
def add_products():
    form = NewsForm()
    add_news('product')
    if form.validate_on_submit():
        return redirect('/products')
    return render_template('news.html', form=form, page='Добавление продукта',
                           courier_password=courier_password)


@app.route('/products/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_products(id):
    form = NewsForm()
    if request.method == "GET":
        session = db_session.create_session()
        news = session.query(products.Products)
        if news:
            form.title.data = news.title
            form.content.data = news.content
        else:
            abort(404)
    elif form.validate_on_submit():
        session = db_session.create_session()
        news = session.query(products.Products)
        if news:
            news.title = form.title.data
            news.content = form.content.data
            session.commit()
            return redirect('/product')
        else:
            abort(404)
    return render_template('news.html', page='Редактирование товара', form=form,
                           courier_password=courier_password)


@app.route('/products_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def products_delete(id):
    session = db_session.create_session()
    news = session.query(products.Products).filter(products.Products.id == id,
                                                   products.Products.user == current_user).first()
    if news:
        session.delete(news)
        session.commit()
    else:
        abort(404)
    return redirect('/product')


@app.route("/reviews")
def all_reviews():
    return render_template("all_news.html", news=all_news('reviews'), page="Отзывы",
                           type="Добавление отзыва", courier_password=courier_password)


@app.route('/review', methods=['GET', 'POST'])
@login_required
def add_reviews():
    form = ReviewForm()
    add_news('review')
    if form.validate_on_submit():
        return redirect('/reviews')
    return render_template('news.html', page='Добавление отзыва', form=form,
                           courier_password=courier_password)


@app.route('/reviews/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_reviews(id):
    form = ReviewForm()
    if request.method == "GET":
        session = db_session.create_session()
        news = session.query(review.Reviews).filter(review.Reviews.id == id,
                                                    review.Reviews.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        news = session.query(review.Reviews).filter(review.Reviews.id == id,
                                                    review.Reviews.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            session.commit()
            return redirect('/reviews')
        else:
            abort(404)
    return render_template('news.html', page='Редактирование отзыва', form=form,
                           courier_password=courier_password)


@app.route('/reviews_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def reviews_delete(id):
    session = db_session.create_session()
    news = session.query(review.Reviews).filter(review.Reviews.id == id,
                                                review.Reviews.user == current_user).first()
    if news:
        session.delete(news)
        session.commit()
    else:
        abort(404)
    return redirect('/reviews')


@app.route("/basket", methods=['POST', 'GET'])
def basket():
    global intermediate_prices
    if request.method == 'GET':
        return render_template('basket.html')
    elif request.method == 'POST':
        args = [request.form['tel'], request.form['address1'],
                request.form['address2'], request.form['order'],
                request.form['payment']]
        check_order(args)
        print(check_True(const))
        if check_True(const):
            print('Всё хорошо')
            session = db_session.create_session()
            order = orders.Orders(
                tel=args[0],
                addresses=f"{args[1]}, {args[2]}",
                order=args[3],
                payment=args[4],
                price=const['price']
            )
            session.add(order)
            session.commit()
        return render_template('expectation.html', **const, courier_password=courier_password)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    app.debug = True
    # вызов всего, что связано с базой данных
    db_session.global_init("db/blogs0.sqlite")
    api.add_resource(news_resources.NewsListResource, '/api/v2/news')
    api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
