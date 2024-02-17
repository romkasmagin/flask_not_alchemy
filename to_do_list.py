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


def get_category_tasks(category_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT task.id, task.title, 
                task.description, task.created, task.status, categories.title
                FROM task 
                INNER JOIN categories ON categories.id = task.categories

                WHERE task.categories = {category_id};
                """
            )
            my_tasks = cursor.fetchall()

    tasks_data = list()

    for task in my_tasks:
        tasks_data.append(
            {
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'created': task[3],
                'status': task[4],
                'category': task[5]
            }
        )

    return tasks_data


@app.route('/')
def index():
    categories = get_all_categories()
    return render_template('index.html', categories=categories)


@app.route('/<int:category_id>/tasks')
def tasks(category_id):
    categories_tasks = get_category_tasks(category_id)
    return render_template('category_tasks.html', tasks=categories_tasks)


if __name__ == '__main__':
    app.run(debug=True)
