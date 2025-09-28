from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

class Command(BaseCommand):
    help = 'Fix migration history inconsistency'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Check if the migration already exists
            cursor.execute("""
                SELECT COUNT(*) FROM django_migrations 
                WHERE app = 'portfolioapp' AND name = '0023_auto_20250928_1256'
            """)
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Mark the problematic migration as applied
                cursor.execute("""
                    INSERT INTO django_migrations (app, name, applied)
                    VALUES ('portfolioapp', '0023_auto_20250928_1256', %s)
                """, [timezone.now()])
                
                self.stdout.write(
                    self.style.SUCCESS('Successfully fixed migration history')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('Migration already exists in database')
                )
