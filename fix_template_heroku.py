#!/usr/bin/env python3
"""
Script to fix the template file on Heroku
"""

import os
import shutil

def fix_template():
    # Define file paths
    source_file = 'portfolioapp/templates/portfolioapp/ecommerce_detail_fixed.html'
    target_file = 'portfolioapp/templates/portfolioapp/ecommerce_detail.html'
    
    # Check if source file exists
    if not os.path.exists(source_file):
        print(f"Source file {source_file} does not exist")
        return False
    
    # Copy the fixed template to replace the broken one
    try:
        shutil.copy2(source_file, target_file)
        print(f"Successfully replaced {target_file} with fixed version")
        return True
    except Exception as e:
        print(f"Error copying file: {e}")
        return False

if __name__ == "__main__":
    if fix_template():
        print("Template fix completed successfully")
    else:
        print("Template fix failed")