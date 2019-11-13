import yaml
import psycopg2
import pandas as pd
from flask import Flask, request

with open('configs/config.yml', 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)


def get_tables_from(table_name, date_from, date_to):

    connect = psycopg2.connect(dbname=config['database_name'], user=config['database_user'],
                               password=config['database_password'], host=config['database_host'])

    cursor = connect.cursor()

    sql_query = 'SELECT * FROM ' + table_name
    cursor.execute(sql_query +
                   " WHERE updated_at BETWEEN %(date_from)s AND %(date_to)s "
                   "ORDER BY updated_at DESC", {'date_from': date_from, 'date_to': date_to})
    drugstore_positions = cursor.fetchall()

    df = pd.DataFrame(drugstore_positions)

    connect.close()
    return df.to_html()


app = Flask(__name__)


@app.route('/')
def index_page():
    return 'Index page'


@app.route('/catalogue_products')
def catalogue_products_page():
    table_name = 'catalogue_products'
    date_from = request.form['date_from']
    date_to = request.form['date_to']
    return get_tables_from(str(table_name), date_from, date_to)


@app.route('/drugstore_positions')
def drugstore_positions_page():
    table_name = 'drugstore_positions'
    date_from = request.form['date_from']
    date_to = request.form['date_to']
    return get_tables_from(str(table_name), date_from, date_to)


if __name__ == "__main__":
    app.run(debug=True, port=5600)
