import json
from itertools import islice

from src.events.client import ElasticSearchClient
from src.events.models import EventMessage
from src.events.serializers import EventListSerializer, EventSerializer

# Opening JSON file
file = open("src/events/wazuh_hight_level_alert_2.json")

query = """{
   "query": {
     "range": {
       "recive_time": {
         "gt": "now-30m",
         "lte": "now"
       }
     }
   }
 }'"""

# file = ElasticSearchClient().get_elasticsearch_events(query=query)


wazuh_hight_level_alert = json.load(file)
wazuh_hight_serializer = EventSerializer(wazuh_hight_level_alert, many=True)

wazuh_hight_serializer = EventSerializer(
    list(
        map(
            lambda x: x.get("_source"),
            EventListSerializer(
                wazuh_hight_level_alert.get("hits").get("hits"), many=True
            ).data,
        )
    ),
    many=True,
).data


def filter_events(raw_wazuh_hight_level_alerts):
    """Фильтруем события, которые уже сохранены в бд"""
    events = EventMessage.objects.all().values_list("keyfields", flat=True)

    return list(
        filter(
            lambda x: x.get("rule_descriptions").get("keyfields") not in events,
            raw_wazuh_hight_level_alerts,
        )
    )


def load_events(raw_wazuh_hight_level_alerts):
    wazuh_hight_level_alerts = filter_events(raw_wazuh_hight_level_alerts)
    batch_size = 100
    objs = (
        EventMessage(
            rule_info=event.get("rule_info"),
            keyfields=event.get("rule_descriptions").get("keyfields"),
            rule_description=event.get("rule_descriptions").get("rule_description"),
            id_incident=event.get("IncidentID"),
            user_info=event.get("user_info_data"),
        )
        for event in wazuh_hight_level_alerts
    )
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        EventMessage.objects.bulk_create(batch, batch_size)
