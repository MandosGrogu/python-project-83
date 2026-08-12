import os
import asyncpg

import datetime
from dotenv import load_dotenv

if 'DATABASE_URL' not in os.environ:
    load_dotenv("secret.env")

DATABASE_URL = os.getenv('DATABASE_URL')

class URLsRepository:

    async def save(self, url):
        existed_url =  await self.check_url_by_name(url)

        if existed_url is None:
            conn = await asyncpg.connect(DATABASE_URL)
            async with conn.transaction():
                new_id = await conn.fetchrow('INSERT INTO urls (name, created_at) VALUES ($1, $2) RETURNING id;', url, datetime.date.today(),)
            await conn.close()
        else:
            new_id = existed_url
        return new_id
    
    async def save_check(self, url, status_code, h1, title, descr):

        conn = await asyncpg.connect(DATABASE_URL)
        async with conn.transaction():
            await conn.fetchrow('INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES ($1::integer, $2::integer, $3, $4, $5, $6);', int(url['id']), status_code, h1, title, descr, datetime.date.today(),)
        await conn.close()

    async def check_url_by_id(self, url_id):

        conn = await asyncpg.connect(DATABASE_URL)
        async with conn.transaction():
            url = await conn.fetchrow('SELECT * FROM urls WHERE id = $1::integer;', int(url_id),)
        await conn.close()
        return url
    
    async def get_all_checks(self, url_id):

        conn = await asyncpg.connect(DATABASE_URL)
        async with conn.transaction():
            url = await conn.fetch('SELECT * FROM url_checks WHERE url_id = $1::integer;', int(url_id),)
        await conn.close()
        return url

    async def check_url_by_name(self, url_name):

        conn = await asyncpg.connect(DATABASE_URL)
        async with conn.transaction():
            url = await conn.fetchrow('SELECT id FROM urls WHERE name = $1;', url_name,)
        await conn.close()
        return url

    async def get_all(self,):
        conn = await asyncpg.connect(DATABASE_URL)
        async with conn.transaction():
            url = await conn.fetch('SELECT DISTINCT ON (u.id) u.id, u.name, uc.created_at, uc.status_code FROM urls as u LEFT JOIN url_checks as uc ON u.id = uc.url_id ORDER BY u.id, uc.created_at DESC NULLS LAST;')
        await conn.close()
        return url