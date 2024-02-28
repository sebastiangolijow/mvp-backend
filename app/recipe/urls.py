from django.urls import include
from django.urls import path
from recipe import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('recipes', views.RecipeViewSet) ### autogenerated urls
router.register('tags', views.TagViewSet)
app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]