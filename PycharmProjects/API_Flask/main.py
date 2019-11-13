import yaml
import psycopg2
import pandas as pd
from flask import Flask, request, jsonify, redirect, url_for
app = Flask(__name__)
all_posts_id = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10]

with open('confs/config.yml', 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)


def get_tables_from():

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
    return 'Index page'


@app.route('/catalogue_products')
def catalogue_products_page():
    return get_tables_from().to_html()


@app.route('/drugstore_positions')
def drugstore_positions_page():
    return get_tables_from().to_html()


if __name__ == "__main__":
    app.run(debug=True)
