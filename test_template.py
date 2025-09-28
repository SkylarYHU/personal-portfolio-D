#!/usr/bin/env python
import os
import django
from django.conf import settings
from django.template import Template, Context
from django.template.loader import get_template

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

try:
    # Try to load the template
    template = get_template('portfolioapp/ecommerce_detail.html')
    print("Template loaded successfully!")
    
    # Try to render with minimal context
    context = Context({
        'ecommerce_project': {
            'title': 'Test Project',
            'description': 'Test Description'
        }
    })
    
    rendered = template.render(context)
    print("Template rendered successfully!")
    
except Exception as e:
    print(f"Template error: {e}")
    import traceback
    traceback.print_exc()