from datetime import datetime
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras
import os

if 'DATABASE_URL' not in os.environ:
    load_dotenv("secret.env")

DATABASE_URL = os.getenv('DATABASE_URL')

class URLsRepository:

    def save(self, url):
        existed_url = self.check_url_by_name(url)

        if existed_url is None:
            conn = psycopg2.connect(DATABASE_URL)
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
                curs.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;', (url, datetime.today().strftime('%Y-%m-%d')))
                new_id = curs.fetchone()['id']
            conn.commit()
            conn.close()
        else:
            new_id = existed_url['id']
        return new_id
    
    def save_check(self, url):

        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
            curs.execute('INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s) RETURNING url_id;', (url['id'], 200, '', '', '', datetime.today().strftime('%Y-%m-%d')))
            new_id = curs.fetchone()
        conn.commit()
        conn.close()
        return new_id

    def check_url_by_id(self, url_id):

        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
            curs.execute('SELECT * FROM urls WHERE id = %s;', (url_id,))
            url = curs.fetchall()
        conn.close()
        return url
    
    def get_all_checks(self, url_id):

        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
            curs.execute('SELECT * FROM url_checks WHERE url_id = %s;', (url_id,))
            url = curs.fetchall()
        conn.close()
        return url

    def check_url_by_name(self, url_name):

        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
            curs.execute('SELECT id FROM urls WHERE name = %s;', (url_name,))
            url = curs.fetchone()
        conn.close()
        return url

    def get_all(self,):
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
            curs.execute('SELECT u.id, name, uc.created_at, uc.status_code FROM urls as u LEFT JOIN url_checks as uc on u.id=uc.url_id WHERE uc.created_at = (SELECT MAX(uc.created_at) FROM url_checks as uc WHERE uc.url_id = u.id) GROUP BY u.id, name, uc.created_at, uc.status_code;')
            url = curs.fetchall()
        conn.close()
        return url