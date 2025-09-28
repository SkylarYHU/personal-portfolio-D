from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Fix missing category field in SocialMediaPost table'

    def handle(self, *args, **options):
        self.stdout.write("Checking and fixing category field...")
        
        try:
            with connection.cursor() as cursor:
                # Check if category column exists
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='portfolioapp_socialmediapost' 
                    AND column_name='category';
                """)
                
                result = cursor.fetchone()
                
                if result:
                    self.stdout.write(self.style.SUCCESS("✓ Category field already exists"))
                else:
                    self.stdout.write("Adding category field...")
                    cursor.execute("""
                        ALTER TABLE portfolioapp_socialmediapost 
                        ADD COLUMN category VARCHAR(128) DEFAULT '';
                    """)
                    self.stdout.write(self.style.SUCCESS("✓ Category field added successfully"))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
            
        # Verify the field was added
        try:
            from portfolioapp.models import SocialMediaPost
            fields = [f.name for f in SocialMediaPost._meta.fields]
            if 'category' in fields:
                self.stdout.write(self.style.SUCCESS("✓ Category field is now available in the model"))
            else:
                self.stdout.write(self.style.ERROR("✗ Category field is still missing from the model"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error checking model: {e}"))