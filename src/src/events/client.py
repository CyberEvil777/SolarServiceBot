import requests
from django.conf import settings


class ElasticSearchClient:
    """Клиент для взаимодействия с ElasticSearch"""

    URL_WAZUH = settings.URL_WAZUH
    ELASTIC_USER = settings.ELASTIC_USER
    ELASTIC_PASS = settings.ELASTIC_PASS
    ELASTIC_URL = settings.ELASTIC_URL

    def download_alerts(self):
        """Скачиваем данные с API"""
        response = requests.get(url=self.URL_WAZUH)
        json = response.json()
        return json

    def get_elasticsearch_events(self, query):
        headers = {"Content-Type": "application/json"}
        auth = (self.ELASTIC_USER, self.ELASTIC_PASS)
        try:
            response = requests.post(
                self.ELASTIC_URL,
                data=query,
                headers=headers,
                auth=auth,
                verify=False,
            )
            # j = json.loads(response.text)
            return response.json()
        except:
            return {}


class WriteAlert:
    File = settings.FILE_WAZUH_ALERT

    def write(self, json):
        """Запмсываем данные с инцидента в документ"""
        with open(self.File, "w") as file:
            file.write(json)
