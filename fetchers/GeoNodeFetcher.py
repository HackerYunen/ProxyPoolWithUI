from .BaseFetcher import BaseFetcher
import requests


class GeoNodeFetcher(BaseFetcher):
    def fetch(self):
        """
        'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1'
        """
        page = 0
        proxies = []
        while True:
            page += 1
            url = f"https://proxylist.geonode.com/api/proxy-list?limit=500&page={page}"
            headers = {
                "content-type": "application/json",
                "origin": "https://proxylist.geonode.com",
                "referer": "https://proxylist.geonode.com/",
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
            }
            resp = requests.get(url, headers=headers).json()
            for proxy_item in resp['data']:
                ip = proxy_item['ip']
                port = proxy_item["port"]
                protocol = proxy_item['protocols'][0]
                proxies.append((protocol, ip, int(port)))
            if resp["total"] < page * 500:
                break
        return list(set(proxies))
