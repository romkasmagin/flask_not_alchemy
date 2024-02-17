import psycopg2

from data_for_connection import connection_data


def get_connection():
    conn = psycopg2.connect(
        dbname=connection_data.dbname,
        host=connection_data.host,
        port=connection_data.port,
        user=connection_data.user,
        password=connection_data.password
    )
    return conn


def main():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS categories(
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS task(
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    status BOOLEAN NOT NULL,
                    categories INT REFERENCES categories(id) NOT NULL
                );
                """
            )

            cursor.execute(
                """
                INSERT INTO categories (title)
                VALUES ('Make git commits');
                """
            )

            cursor.execute(
                """
                INSERT INTO task (title, description, status, categories)
                VALUES ('Create main page', 'Create commits', FALSE, 2),
                ('Create edit page', 'Create commits', FALSE, 2),
                ('Create delete function', 'Create commits', FALSE, 2)
                """
            )


if __name__ == '__main__':
    main()
