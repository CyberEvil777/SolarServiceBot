from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.goods.views import GoodsListView

urlpatterns = [
    path("goods/", GoodsListView.as_view()),
]
