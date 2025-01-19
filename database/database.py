import asyncpg

from decouple import config

class Database:
    def __init__(self):
        self.pool = None
        self.database_url = config('DATABASE_URL')
        print(f"Trying connect to Mikko_DB: {self.database_url}")

    async def connect(self):
        """Creating connection to database"""
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=1,
                max_size=10,
                ssl='require'
            )
            print('Connecting to database')

        except asyncpg.PostgresError as e:
            print(f"Error connecting to database: {e}")
            raise e
            
        except Exception as e:
            print(f'Error creating pool: {e}')
            raise e
