#!/usr/bin/env python
"""
Fix Heroku migration inconsistencies by creating a clean migration state
"""
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

def fix_migrations():
    """Fix migration inconsistencies on Heroku"""
    print("Fixing Heroku migration inconsistencies...")
    
    with connection.cursor() as cursor:
        # Check if MotionGraphicsProject table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='portfolioapp_motiongraphicsproject';
        """)
        
        if cursor.fetchone():
            print("MotionGraphicsProject table already exists!")
            return
        
        # Create MotionGraphicsProject table manually
        print("Creating MotionGraphicsProject table...")
        cursor.execute("""
            CREATE TABLE "portfolioapp_motiongraphicsproject" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "title" varchar(128) NOT NULL,
                "description" text NOT NULL,
                "video_file" varchar(100) NOT NULL,
                "video_url" varchar(200) NOT NULL,
                "preview_image" varchar(100) NOT NULL,
                "about_project" text NOT NULL,
                "goals" text NOT NULL,
                "tools_software" text NOT NULL,
                "process_image" varchar(100) NOT NULL,
                "storyboard_image" varchar(100) NOT NULL,
                "final_output_image" varchar(100) NOT NULL,
                "date_posted" datetime,
                "order" integer NOT NULL,
                "is_active" bool NOT NULL
            );
        """)
        
        # Create the many-to-many table for tags
        cursor.execute("""
            CREATE TABLE "portfolioapp_motiongraphicsproject_tags" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "motiongraphicsproject_id" bigint NOT NULL REFERENCES "portfolioapp_motiongraphicsproject" ("id") DEFERRABLE INITIALLY DEFERRED,
                "tag_id" bigint NOT NULL REFERENCES "portfolioapp_tag" ("id") DEFERRABLE INITIALLY DEFERRED
            );
        """)
        
        # Create indexes
        cursor.execute("""
            CREATE INDEX "portfolioapp_motiongraphicsproject_order_4a8b5c" 
            ON "portfolioapp_motiongraphicsproject" ("order");
        """)
        
        cursor.execute("""
            CREATE UNIQUE INDEX "portfolioapp_motiongraphicsproject_tags_motiongraphicsproject_id_tag_id_8c8b5c_uniq" 
            ON "portfolioapp_motiongraphicsproject_tags" ("motiongraphicsproject_id", "tag_id");
        """)
        
        cursor.execute("""
            CREATE INDEX "portfolioapp_motiongraphicsproject_tags_motiongraphicsproject_id_8c8b5c" 
            ON "portfolioapp_motiongraphicsproject_tags" ("motiongraphicsproject_id");
        """)
        
        cursor.execute("""
            CREATE INDEX "portfolioapp_motiongraphicsproject_tags_tag_id_8c8b5c" 
            ON "portfolioapp_motiongraphicsproject_tags" ("tag_id");
        """)
        
        # Mark the migration as applied
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied) 
            VALUES ('portfolioapp', '0037_auto_20251002_2329', datetime('now'));
        """)
        
        print("MotionGraphicsProject table created successfully!")
        print("Migration 0037 marked as applied.")

if __name__ == '__main__':
    fix_migrations()
