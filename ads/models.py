from django.db import models


# ----------------------------------------------------------------------------------------------------------------------
# Create category model
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# ----------------------------------------------------------------------------------------------------------------------
# Create ad model
class Ad(models.Model):
    PUBLISHED = [(True, "Опубликовано"), (False, "Не опубликовано")]

    name = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=1000)
    address = models.CharField(max_length=200)
    is_published = models.BooleanField(choices=PUBLISHED, default=False)

    def __str__(self):
        return self.name
