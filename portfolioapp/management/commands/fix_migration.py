from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Fix migration history inconsistency'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Mark the problematic migration as applied
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied)
                VALUES ('portfolioapp', '0023_auto_20250928_1256', NOW())
                ON CONFLICT (app, name) DO NOTHING;
            """)
            
            self.stdout.write(
                self.style.SUCCESS('Successfully fixed migration history')
            )
