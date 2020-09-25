"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'core'

urlpatterns = [
    path('test/', test_view, name='list'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('add_coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('', HomeView.as_view(), name='item-list'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('product/<slug>/', ItemDetialView.as_view(), name='product'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),

]
