from django.db                      import models
from django.contrib.auth.models     import User
from django.conf                    import settings
from django.dispatch                import receiver
from django.core.validators         import MaxValueValidator, MinValueValidator
from django.core.validators         import MinValueValidator
from django.core.exceptions         import ValidationError
from datetime                       import datetime

from .base import Author


class Ingredient(Author):
    unit_enum = [
        (0, '/kg'),
        (1, '/pc')
    ]
    name = models.CharField(max_length=240)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.IntegerField(choices=unit_enum, default=0)

    def __str__(self):
        return self.name

class Pastry(Author):
    name = models.CharField(max_length=240, unique=True)
    def __str__(self):
        return self.name

    class Meta: 
      verbose_name_plural = 'Pastries'


class PastryIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE)
    pastry = models.ForeignKey(
        Pastry, on_delete=models.CASCADE)
    unit = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return f'{self.pastry}-{self.ingredient}'

    class Meta:
      unique_together = ('ingredient', 'pastry')
