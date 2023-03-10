from typing import TypedDict

from rest_framework import serializers


class RuleDescriptionDTO(TypedDict):
    """
    {
    keyfields: id Ключь с ElasticSearch,
    rule_description: описание инцидента,
    }
    """

    keyfields: str
    rule_description: str


class EventListSerializer(serializers.Serializer):
    """Сериализация списка событий"""

    _source = serializers.DictField()


class EventSerializer(serializers.Serializer):
    """Сериализатор полей для Инцидентов"""

    rule_info = serializers.CharField()
    rule_descriptions = serializers.SerializerMethodField(
        method_name="rule_description",
    )
    IncidentID = serializers.CharField()
    user_info = serializers.SerializerMethodField(
        method_name="user_info",
    )

    def rule_description(self, obj):
        """id Ключь с ElasticSearch, описание инцидента"""
        rule_description_list = obj.get("rule_description").split("| -+- |")
        return RuleDescriptionDTO(
            keyfields=rule_description_list[0],
            rule_description=rule_description_list[1],
        )

    def user_info(self, obj):
        return obj.get("user_info", "")
