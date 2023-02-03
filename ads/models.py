from django.db import models


# ----------------------------------------------------------------------------------------------------------------------
# Create category model
class Category(models.Model):
    name: str = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# ----------------------------------------------------------------------------------------------------------------------
# Create ad model
class Ad(models.Model):
    PUBLISHED: list[tuple] = [(True, "Опубликовано"), (False, "Не опубликовано")]

    name: str = models.CharField(max_length=200)
    author: str = models.CharField(max_length=50)
    price: int = models.PositiveIntegerField()
    description: str = models.CharField(max_length=1000)
    address: str = models.CharField(max_length=200)
    is_published: bool = models.BooleanField(choices=PUBLISHED, default=False)

    def __str__(self):
        return self.name
