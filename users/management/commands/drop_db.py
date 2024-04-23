import os

from django.core.management.base import BaseCommand
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Command(BaseCommand):
    help = 'Create or recreate PostgreSQL database'

    def handle(self, *args, **options):
        conn = psycopg2.connect(user=os.getenv('POSTGRES_USER'),
                                password=os.getenv('POSTGRES_PASSWORD'),
                                host=os.getenv('HOST'),
                                port=os.getenv('PORT'), )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = conn.cursor()

        db_name = os.getenv('POSTGRES_DB')

        cursor.execute(
            sql.SQL("DROP DATABASE {}").format(
                sql.Identifier(db_name)
            )
        )
        self.stdout.write(self.style.SUCCESS("Database successfully destroyed."))

        cursor.close()
        conn.close()
