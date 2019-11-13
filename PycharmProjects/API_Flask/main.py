import yaml
import psycopg2
import pandas as pd
from flask import Flask, request
app = Flask(__name__)
all_posts_id = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10]

with open('confs/config.yml', 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)


def get_tables_from(date_from, date_to):

    connect = psycopg2.connect(dbname=config['database_name'], user=config['database_user'],
                               password=config['database_password'], host=config['database_host'])

    cursor = connect.cursor()

    cursor.execute("SELECT * FROM drugstore_positions "
                   "WHERE updated_at BETWEEN %(date_from)s AND %(date_to)s "
                   "ORDER BY updated_at DESC", {'date_from': date_from, 'date_to': date_to})
    drugstore_positions = cursor.fetchall()

    df = pd.DataFrame(drugstore_positions)

    connect.close()
    return df


@app.route('/')
def index_page():
    return 'Index page'


@app.route('/catalogue_products', methods=['GET', 'POST'])
def catalogue_products_page():
    date_from = request.form['date_from']
    date_to = request.form['date_to']
    return get_tables_from(date_from, date_to).to_html()


@app.route('/drugstore_positions', methods=['GET', 'POST'])
def drugstore_positions_page():
    date_from = request.form['date_from']
    date_to = request.form['date_to']
    return get_tables_from(date_from, date_to).to_html()


if __name__ == "__main__":
    app.run(debug=True, port=5600)
