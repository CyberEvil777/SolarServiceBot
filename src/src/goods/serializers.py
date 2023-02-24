from rest_framework import serializers

from src.goods.models import Goods


class GoodsSerializer(serializers.ModelSerializer):

    photo = serializers.SerializerMethodField("convert_photo_base64")

    def convert_photo_base64(self, obj):
        return obj.get_convert_base64(obj)

    class Meta:
        model = Goods
        fields = ("id", "title", "price", "description", "photo")
