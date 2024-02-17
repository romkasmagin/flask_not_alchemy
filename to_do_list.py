from flask import Flask, render_template, url_for, request, redirect, flash
import psycopg2

from data_for_connection import connection_data


app = Flask(__name__)
app.config['SECRET_KEY'] = '123'


def get_connection():
    conn = psycopg2.connect(
        dbname=connection_data.dbname,
        host=connection_data.host,
        port=connection_data.port,
        user=connection_data.user,
        password=connection_data.password
    )
    return conn


def get_all_categories():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title FROM categories;
                """
            )
            categories = cursor.fetchall()

    categories_data = list()

    for category in categories:
        categories_data.append(
            {
                'id': category[0],
                'title': category[1]
            }
        )

    return categories_data


@app.route('/')
def index():
    categories = get_all_categories()
    return render_template('index.html', categories=categories)


if __name__ == '__main__':
    app.run(debug=True)