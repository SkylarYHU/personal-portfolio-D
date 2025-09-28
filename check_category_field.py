#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from portfolioapp.models import SocialMediaPost

print('=== Checking SocialMediaPost Model Fields ===')
fields = [f.name for f in SocialMediaPost._meta.fields]
print('All fields:', fields)

if 'category' in fields:
    print('✓ Category field EXISTS in the model')
else:
    print('✗ Category field MISSING from the model')

# Also check database table structure
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'portfolioapp_socialmediapost';")
    db_columns = [row[0] for row in cursor.fetchall()]
    print('Database columns:', db_columns)
    
    if 'category' in db_columns:
        print('✓ Category column EXISTS in database')
    else:
        print('✗ Category column MISSING from database')