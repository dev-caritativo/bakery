from rest_framework import serializers
from ..models.pastry import *


class PastrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pastry
        fields = ['id', 'name']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'price', 'unit']

class PastryIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastryIngredient
        fields = ['id', 'unit', 'ingredient', 'pastry']
