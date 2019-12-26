from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'dish_type', views.DishTypeViewSet)
router.register(r'dish_temperature', views.DishTemperatureViewSet)
router.register(r'ingredient', views.IngredientViewSet)
router.register(r'time_units', views.TimeUnitsViewSet)
router.register(r'dish_ingredients', views.DishIngredientsViewSet)
router.register(r'dish_steps', views.DishStepsViewSet)
router.register(r'dish', views.DishViewSet)
router.register(r'dish_available', views.DishAvailableViewSet)
router.register(r'client', views.ClientViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'order_track', views.OrderTrackViewSet)
router.register(r'client_address', views.ClientAddressViewSet)
router.register(r'order_dishes', views.OrderDishesViewSet)
router.register(r'client_dish', views.ClientDishViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('add_dish/', views.add_new_dish),
    path('add/', views.add_dish),
    path('post/', views.post_dish),
]