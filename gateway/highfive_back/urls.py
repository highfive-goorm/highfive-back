"""
URL configuration for highfive_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include, re_path

from .views import AdminView, ProductProxyView, OrderProxyView, CartProxyView, AlertProxyView, RecommendProxyView, \
    LikeProxyView, BrandLikeProxyView, TrackingProxyView, PromotionProxyView

urlpatterns = [  # POST /product, GET /product?name=
    path('product', ProductProxyView.as_view()),
    path('product/<int:id>', ProductProxyView.as_view()),
    path('product/like/count/<str:user_id>', LikeProxyView.as_view()),
    path('product/<int:id>/like', LikeProxyView.as_view()),
    path('product/<int:id>/like/<str:user_id>', LikeProxyView.as_view()),
    path('brand/like/count/<str:user_id>', BrandLikeProxyView.as_view()),
    path('brand/<int:id>/like', BrandLikeProxyView.as_view()), # POST
    path('brand/<int:id>/like/<str:user_id>', BrandLikeProxyView.as_view()),
    path('admin', AdminView.as_view()),
    path('user', include('user.urls')),
    path('order', OrderProxyView.as_view()), # POST (주문 생성)
    path('order/<str:id>', OrderProxyView.as_view()), # GET (단일 주문), PUT, DELETE
    path('order/user/<str:user_id>', OrderProxyView.as_view()), # GET (사용자별 주문 목록)
    path('cart', CartProxyView.as_view()),
    path('cart/<str:user_id>', CartProxyView.as_view()),
    path('cart/<str:user_id>/<str:product_id>', CartProxyView.as_view()),
    path('alert', AlertProxyView.as_view()),
    path('alert/<int:id>', AlertProxyView.as_view()),
    path('recommend/<str:user_id>', RecommendProxyView.as_view()),
    path('ht/', include('health_check.urls')),
    # Tracking Service
    path('tracking/log/event', TrackingProxyView.as_view(), name='tracking_log_event'),
    # Promotion Service (Simplified URLs)
    path('promotion/active', PromotionProxyView.as_view(), {'action': 'active'}, name='promotion_active_list'),  # GET
    path('promotion', PromotionProxyView.as_view(), name='promotion_create'),  # POST
    path('promotion/<str:promotion_id>', PromotionProxyView.as_view(), name='promotion_detail_manage'),  # GET, PATCH, DELETE
    # KakaoPay Order Endpoints
    path('payment/kakao/ready', OrderProxyView.as_view(), name='kakao_payment_ready'), # POST
    path('payment/kakao/approve', OrderProxyView.as_view(), name='kakao_payment_approve'), # POST
]
