from django.urls import path

from . import views


app_name = 'sellers'
urlpatterns = [
    path("increase/<int:seller_id>/", views.IncreaseCreditView.as_view(), name="increase_credit"),
    path("decrease/<int:seller_id>/", views.DecreaseCreditView.as_view(), name="decrease_credit"),
    path("sell-charge/<int:seller_id>/", views.SellChargeView.as_view(), name="sell_charge")
]


