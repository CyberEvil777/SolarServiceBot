from rest_framework import generics

from src.goods.models import Goods
from src.goods.serializers import GoodsSerializer
from src.shop.models import WinnerShop


class GoodsListView(generics.ListAPIView):
    serializer_class = GoodsSerializer

    def get_queryset(self):
        return Goods.objects.filter(
            shop=WinnerShop.objects.all().only("shop").first().shop
        )
