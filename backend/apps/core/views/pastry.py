from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from ..models.pastry import *
from ..serializers.pastry import *


class PastryView(viewsets.ViewSet):
    permission_classes = []

    def retrieve(self, request, pk=None):
        queryset = Pastry.objects.all()
        serializer = PastrySerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
      r = request.data
      try:
        pastry = Pastry.objects.get(id=r['id'])
        pastry.name = r['name']
        pastry.save()

        serializer = PastrySerializer(pastry)
        return Response(serializer.data)
      except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class IngredientsView(viewsets.ViewSet):
    permission_classes = []

    def retrieve(self, request, pk=None):
        queryset = Ingredient.objects.all()
        serializer = IngredientSerializer(queryset, many=True)
        return Response(serializer.data)


class PastryIngredientsView(viewsets.ViewSet):
    permission_classes = []

    def retrieve(self, request, pk=None):
        params = self.request.query_params
        queryset = PastryIngredient.objects.filter(pastry=params['id'])
        serializer = PastryIngredientSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
      r = request.data

      try:
        q = PastryIngredient.objects.get(id=r['id']['id'])
        q.unit = int(r['value'])
        q.save()
        serializer = PastryIngredientSerializer(q)
        return Response(serializer.data)
      except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
      r = request.data
      try:
        p = Pastry.objects.get(id=r['iid'])
        i = Ingredient.objects.get(id=r['value']['id'])
        
        pi = PastryIngredient.objects.create(
          pastry = p,
          ingredient = i
        )
        serializer = PastryIngredientSerializer(pi)
        return Response(serializer.data)
      except IntegrityError as e: return Response({"msg": "Already Exists"} ,status=status.HTTP_409_CONFLICT)
      except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
      r = request.data
      try:
        pi = PastryIngredient.objects.get(id=r['iid']['id'])
        pi.delete()
        return Response({'msg': 'Successful', 'id': r['iid']['id']})
      except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

