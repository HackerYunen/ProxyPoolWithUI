from .BaseFetcher import BaseFetcher
import requests


class FreeProxyApiFetcher(BaseFetcher):
    def fetch(self):
        """
        'https://public.freeproxyapi.com/api/Download/Json'
        """
        proxies = []
        url = 'https://public.freeproxyapi.com/api/Download/Json'
        data = '{"types":[1,2,3,4],"levels":[],"countries":[],"type":"json","resultModel":"Mini"}'
        headers = {
            "content-type": "application/json",
            "origin": "https://freeproxyapi.com",
            "referer": "https://freeproxyapi.com/",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }
        resp = requests.post(url, headers=headers, data=data).json()
        protocol_list = ['socks4', 'socks5', 'http', 'https']
        for proxy_item in resp:
            ip = proxy_item['Host']
            port = proxy_item["Port"]
            protocol = protocol_list[proxy_item['Type'] - 1]
            proxies.append((protocol, ip, int(port)))
        return list(set(proxies))
