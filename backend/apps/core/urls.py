from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from .views import *

from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
router = routers.DefaultRouter()
# router.register('properties', view)

app_name = 'core'
urlpatterns = [
    path('', include(router.urls)),
    path('token/', include([
        path('', jwt_views.TokenObtainPairView.as_view(),
             name='token_obtain_pair'),
        path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    ])),
    path('auth/', include([
        path('credential/', auth.GetCredential.as_view(), name='get-credential'),
        path('user/', auth.GetUser.as_view(), name='get-credential'),

    ])),

    path('', include([
        path('pastry/', include([
            path('', pastry.PastryView.as_view(
                {'get': 'retrieve', 'put': 'update'}), name='pastry-list'),
            path('ingredients', pastry.PastryIngredientsView.as_view(
                {'get': 'retrieve','put': 'update', 'post':'create', 'delete':'destroy'}), name='pastry-ingredients-list'),
        ])),
        path('ingredients/', pastry.IngredientsView.as_view(
            {'get': 'retrieve' }), name='ingredients-list'),
    ])),

]
