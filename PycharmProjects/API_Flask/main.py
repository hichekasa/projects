import yaml
import psycopg2
import pandas as pd
from flask import Flask, request, jsonify, redirect, url_for
app = Flask(__name__)

all_posts_id = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10]


def get_tables_from():
    with open("/Users/andrey/PycharmProjects/API_Flask/config.yml") as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.FullLoader)

    connect = psycopg2.connect(dbname=config['database_name'], user=config['database_user'],
                               password=config['database_password'], host=config['database_host'])

    cursor = connect.cursor()

    cursor.execute("SELECT * FROM drugstore_positions LIMIT 100")
    drugstore_positions = cursor.fetchall()

    df = pd.DataFrame(drugstore_positions)

    connect.close()
    return df


@app.route('/')
def index_page():
    return redirect(url_for('home_page'))


@app.route('/home')
def home_page():
    return 'Hello, world!'


@app.route('/posts/')
def posts_page():
    return 'The posts page'


@app.route('/database')
def database():
    return get_tables_from().to_html()


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    if post_id in all_posts_id:
        return 'post id=%d' % post_id
    else:
        return '404 error'


@app.route('/about')
def about_page():
    return 'The about page'


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        data = dict(id='1', name='name', email='@mail')
        response = jsonify(data)
        response.status_code = 202

        return response

    elif request.method == 'GET':
        data = dict(id='none', name='none', email='none')
        response = jsonify(data)
        response.status_code = 406

        return response


if __name__ == "__main__":
    app.run(debug=True)
