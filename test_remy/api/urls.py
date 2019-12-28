from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
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

urlpatterns = [
    path('', include(router.urls)),
    path('dish_details/', views.get_dish),
    path('add/', views.post_dish),
    path('menu/', views.get_menu),
    path('new_order/', views.post_order),
    path('open_orders/', views.get_open_orders),
    path('track_order/', views.track_order),
    path('queue/', views.queue_time),

]