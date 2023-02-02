import csv
import os

import django
from django.apps import apps

# ----------------------------------------------------------------------------------------------------------------------
# Setup env settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Homework_27_PD12.settings')
django.setup()

# ----------------------------------------------------------------------------------------------------------------------
# Add models
Category = apps.get_model('ads', 'Category')
Ad = apps.get_model('ads', 'Ad')

# ----------------------------------------------------------------------------------------------------------------------
# Write data from file to database
with open("categories.csv", encoding="utf-8") as f:
    data = csv.DictReader(f)

    for row in data:
        Category.objects.create(name=row.get('name'))

# ----------------------------------------------------------------------------------------------------------------------
# Write data from file to database
with open("ads.csv", encoding="utf-8") as f:
    data = csv.DictReader(f)

    for row in data:
        is_published = True if row.get('is_published') == "TRUE" else False
        data = {"name": row.get('name'),
                "author": row.get('author'),
                "price": row.get('price'),
                "description": row.get('description'),
                "address": row.get('address'),
                "is_published": is_published
                }

        Ad.objects.create(**data)

# ----------------------------------------------------------------------------------------------------------------------
# Success message
print("Success")
