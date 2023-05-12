import json

import requests

API_TOKEN_ABUSEIPDB = (
    "6e055355e503033b59018c47e5b8536e88345d31377815ad6d17b9468866c6da3ce0433f8f586f41"
)
API_TOKEN_VT = "ab232abf37ff843d9fef731011dc27f4f8d5cd30a18792af516fb1f2508eb288"
API_TOKEN_GREYNOISE = (
    "cpDHlt8response_json0ySYXhX06SLW7OPbxrmvd0QFz3IESNaxW61u2frSBz90EFsFVLmLn6So"
)
ELASTIC_USER = "admin"
ELASTIC_PASS = "zKN7KhZRfM?4nE+peIqVVgw9gr7Hi++J"
ELASTIC_IP = "192.168.100.11"


def abuseipdb_check(susp_ip):
    result = {"is_whitelisted": "", "abuse_score": "", "total_reports": ""}
    params = {"ipAddress": susp_ip, "verbose": ""}
    headers = {"Key": API_TOKEN_ABUSEIPDB, "Accept": "application/json"}
    try:
        response = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            params=params,
            headers=headers,
            verify=False,
        )
        response_json = json.loads(response.text)
        result["is_whitelisted"] = response_json["data"]["isWhitelisted"]
        result["abuse_score"] = int(response_json["data"]["abuseConfidenceScore"])
        result["total_reports"] = int(response_json["data"]["totalReports"])
        return result
    except:
        result["is_whitelisted"] = "Connection error or Request limit"
        result["abuse_score"] = "Connection error or Request limit"
        result["total_reports"] = "Connection error or Request limit"
        return result


def virustotal_check(susp_ip):
    result = {"virustotal_malicious": ""}
    headers = {"x-apikey": API_TOKEN_VT}
    try:
        response = requests.get(
            f"https://www.virustotal.com/api/v3/ip_addresses/{susp_ip}",
            headers=headers,
            verify=False,
        )
        response_json = json.loads(response.text)
        result["virustotal_malicious"] = response_json["data"]["attributes"][
            "last_analysis_stats"
        ]["malicious"]
        return result
    except:
        result["virustotal_malicious"] = "Connection error or Request limit"
        return result


def hosting_check(susp_ip):
    result = {"domains_number": ""}
    params = {"ip": susp_ip, "apikey": API_TOKEN_VT}
    try:
        response = requests.get(
            "http://www.virustotal.com/vtapi/v2/ip-address/report",
            params=params,
            verify=False,
        )
        response_json = json.loads(response.text)
        result["domains_number"] = len(response_json["resolutions"])
        return result
    except:
        result["domains_number"] = "Connection error or Request limit"
        return result


def greynoise_check(susp_ip):
    result = {"greynoise_classification": ""}
    headers = {"accept": "application/json", "key": API_TOKEN_GREYNOISE}
    try:
        response = requests.get(
            f"https://api.greynoise.io/v3/community/{susp_ip}",
            headers=headers,
            verify=False,
        )
        response_json = json.loads(response.text)
        if response_json["message"] == "Success":
            result["greynoise_classification"] = response_json["classification"]
        else:
            result["greynoise_classification"] = "unknown"
        return result
    except:
        result["greynoise_classification"] = "Connection error or Request limit"
        return result


def elasticsearch_count(query):
    headers = {"Content-Type": "application/json"}
    auth = (ELASTIC_USER, ELASTIC_PASS)
    try:
        r = requests.post(
            f"https://{ELASTIC_IP}:9200/_count",
            data=query,
            headers=headers,
            auth=auth,
            verify=False,
        )
        j = json.loads(r.text)
        return j["count"]
    except:
        return "Error"


def elasticsearch_search(query, size=50):
    size = size if size <= 10000 else 10000
    headers = {"Content-Type": "application/json"}
    auth = (ELASTIC_USER, ELASTIC_PASS)
    try:
        r = requests.post(
            f"https://{ELASTIC_IP}:9200/_search?size={size}",
            data=query,
            headers=headers,
            auth=auth,
            verify=False,
        )
        return json.loads(r.text)
    except:
        return "Error"


def elasticsearch_count_30m_from_src_ip(susp_ip, src_ip):
    query = (
        '''{
        "query": {
            "bool": {
                "must": [{
                        "match": {
                            "data_win_eventdata_sourceIp": "'''
        + src_ip
        + '''"
                        }
                    },
                    {
                        "match": {
                            "data_win_eventdata_destinationIp": "'''
        + susp_ip
        + """"
                        }
                    },
                    {
                        "range": {
                            "timestamp": {
                                "gte": "now-30m",
                                "lt": "now"
                            }
                        }
                    }
                ]
            }
        }
    }"""
    )
    return elasticsearch_count(query)


def elasticsearch_count_24h_from_src_ip(susp_ip, src_ip):
    query = (
        '''{
        "query": {
            "bool": {
                "must": [{
                        "match": {
                            "data_win_eventdata_sourceIp": "'''
        + src_ip
        + '''"
                        }
                    },
                    {
                        "match": {
                            "data_win_eventdata_destinationIp": "'''
        + susp_ip
        + """"
                        }
                    },
                    {
                        "range": {
                            "timestamp": {
                                "gte": "now-24h",
                                "lt": "now"
                            }
                        }
                    }
                ]
            }
        }
    }"""
    )
    return elasticsearch_count(query)


def elasticsearch_count_24h_from_all_ip(susp_ip, src_ip):
    query = (
        '''{
        "query": {
            "bool": {
                "must": [{
                        "match": {
                            "data_win_eventdata_destinationIp": "'''
        + susp_ip
        + """"
                        }
                    },
                    {
                        "range": {
                            "timestamp": {
                                "gte": "now-24h",
                                "lt": "now"
                            }
                        }
                    }
                ]
            }
        }
    }"""
    )
    return elasticsearch_count(query)


def elasticsearch_hosts_to_susp_ip(susp_ip, src_ip):
    query = (
        '''{
        "query": {
            "bool": {
                "must": [{
                        "match": {
                            "data_win_eventdata_destinationIp": "'''
        + susp_ip
        + """"
                        }
                    },
                    {
                        "range": {
                            "timestamp": {
                                "gte": "now-24h",
                                "lt": "now"
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "genres": {
                "terms": {
                    "field": "data_win_eventdata_sourceIp"
                }
            }
        }
    }"""
    )
    j = elasticsearch_search(query)
    if j == "Error":
        return "Error", "Error"
    else:
        hosts = []
        for i in j["aggregations"]["genres"]["buckets"]:
            hosts.append(i["key"])
        return len(hosts), hosts


def elasticsearch_hosts_from_susp_ip(susp_ip, src_ip):
    query = (
        '''{
        "query": {
            "bool": {
                "must": [{
                        "match": {
                            "data_win_eventdata_sourceIp": "'''
        + susp_ip
        + """"
                        }
                    },
                    {
                        "range": {
                            "timestamp": {
                                "gte": "now-24h",
                                "lt": "now"
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "genres": {
                "terms": {
                    "field": "data_win_eventdata_destinationIp"
                }
            }
        }
    }"""
    )
    j = elasticsearch_search(query)
    if j == "Error":
        return "Error", "Error"
    else:
        hosts = []
        for i in j["aggregations"]["genres"]["buckets"]:
            hosts.append(i["key"])
        return len(hosts), hosts


def elasticsearch_processes(susp_ip, src_ip):
    query = (
        '''{
        "query": {
            "bool": {
                "must": [{
                        "match": {
                            "data_win_eventdata_destinationIp": "'''
        + susp_ip
        + """"
                        }
                    },
                    {
                        "range": {
                            "timestamp": {
                                "gte": "now-24h",
                                "lt": "now"
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "genres": {
                "terms": {
                    "field": "data_win_eventdata_image"
                }
            }
        }
    }"""
    )
    j = elasticsearch_search(query)
    if j == "Error":
        return "Error", "Error"
    else:
        processes = []
        for i in j["aggregations"]["genres"]["buckets"]:
            processes.append(i["key"])
        return processes


def elasticsearch_users(susp_ip, src_ip):
    query = (
        '''{
        "query": {
            "bool": {
                "must": [{
                        "match": {
                            "data_win_eventdata_destinationIp": "'''
        + susp_ip
        + """"
                        }
                    },
                    {
                        "range": {
                            "timestamp": {
                                "gte": "now-24h",
                                "lt": "now"
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "genres": {
                "terms": {
                    "field": "data_win_eventdata_user"
                }
            }
        }
    }"""
    )
    j = elasticsearch_search(query)
    if j == "Error":
        return "Error", "Error"
    else:
        users = []
        for i in j["aggregations"]["genres"]["buckets"]:
            users.append(i["key"])
        return users


def elasticsearch_investigation(susp_ip, src_ip):
    result = {
        "count_30m_from_src_ip": 0,
        "count_24h_from_src_ip": 0,
        "count_24h_from_all_ip": 0,
        "count_hosts_to_susp_ip": 0,
        "hosts_to_susp_ip": [],
        "count_hosts_from_susp_ip": 0,
        "hosts_from_susp_ip": [],
        "processes": [],
        "users": [],
    }
    result["count_30m_from_src_ip"] = elasticsearch_count_30m_from_src_ip(
        susp_ip, src_ip
    )
    result["count_24h_from_src_ip"] = elasticsearch_count_24h_from_src_ip(
        susp_ip, src_ip
    )
    result["count_24h_from_all_ip"] = elasticsearch_count_24h_from_all_ip(
        susp_ip, src_ip
    )
    (
        result["count_hosts_to_susp_ip"],
        result["hosts_to_susp_ip"],
    ) = elasticsearch_hosts_to_susp_ip(susp_ip, src_ip)
    (
        result["count_hosts_from_susp_ip"],
        result["hosts_from_susp_ip"],
    ) = elasticsearch_hosts_from_susp_ip(susp_ip, src_ip)
    result["processes"] = elasticsearch_processes(susp_ip, src_ip)
    result["users"] = elasticsearch_users(susp_ip, src_ip)
    return result


def investigation(susp_ip, src_ip):
    requests.packages.urllib3.disable_warnings()
    res_of_invest = {
        **hosting_check(susp_ip),
        **abuseipdb_check(susp_ip),
        **virustotal_check(susp_ip),
        **greynoise_check(susp_ip),
        **elasticsearch_investigation(susp_ip, src_ip),
    }
    message = ""
    if (
        len(res_of_invest.values()) == 1
        and res_of_invest.values()[0] == "Connection error or Request limit"
    ):
        message = "нет данных"
    elif (
        res_of_invest["domains_number"] != "Connection error or Request limit"
        and res_of_invest["domains_number"] > 50
    ):
        message = "FP (предположительно хостинг)"
    elif (
        res_of_invest["is_whitelisted"] != "Connection error or Request limit"
        and res_of_invest["is_whitelisted"]
    ):
        message = "FP (в белом списке AbuseIPDB)"
    elif (
        (
            res_of_invest["abuse_score"] != "Connection error or Request limit"
            and res_of_invest["abuse_score"] < 10
        )
        and (
            res_of_invest["virustotal_malicious"] != "Connection error or Request limit"
            and res_of_invest["virustotal_malicious"] <= 1
        )
        and (
            res_of_invest["greynoise_classification"]
            != "Connection error or Request limit"
            and res_of_invest["greynoise_classification"] != "malicious"
        )
    ):
        message = "FP (подозрительной активности не зафиксировано)"
    else:
        message = "Не FP"

    return {**res_of_invest, "message": message}


def demo_print(susp_ip, src_ip):
    result = investigation(susp_ip, src_ip)
    print(f"Исследуемый IP: {susp_ip}")
    print(f'Количество доменов на IP: {result["domains_number"]}')
    print(f'Белый список на AbuseIPDB: {result["is_whitelisted"]}')
    print(f'Abuse Score: {result["abuse_score"]}')
    print(f'Количество репортов на AbuseIPDB: {result["total_reports"]}')
    print(f'Количество сработок на VirusTotal: {result["virustotal_malicious"]}')
    print(f'Классификация GreyNoise: {result["greynoise_classification"]}')
    print(f'Результат расследования: {result["message"]}')
    print(
        f'Количество запросов с {src_ip} к {susp_ip} за последние 30 минут: {result["count_30m_from_src_ip"]}'
    )
    print(
        f'Количество запросов с {src_ip} к {susp_ip} за последние 24 часа: {result["count_24h_from_src_ip"]}'
    )
    print(
        f'Количество запросов со всех хостов к {susp_ip} за последние 24 часа: {result["count_24h_from_all_ip"]}'
    )
    print(
        f'Запросов к {susp_ip} за последние 24 часа были с {result["count_hosts_to_susp_ip"]} хостов: {result["hosts_to_susp_ip"]}'
    )
    print(
        f'Запросов с {susp_ip} за последние 24 часа были к {result["count_hosts_from_susp_ip"]} хостам: {result["hosts_from_susp_ip"]}'
    )
    print(f'Процессы, которые инициировали соединение: {result["processes"]}')
    print(f'Пользователи, которые инициировали соединение: {result["users"]}')
    print()


demo_print("192.168.100.110", "10.6.0.2")
demo_print("10.10.100.37", "10.6.0.2")
# demo_print('77.88.55.242', '')
# demo_print('12.23.34.45', '')
# demo_print('8.8.8.8', '')
# demo_print('102.130.127.117', '')
