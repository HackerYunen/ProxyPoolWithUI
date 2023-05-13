from .BaseFetcher import BaseFetcher
import requests
import re


class SocksProxyFetcher(BaseFetcher):
    def fetch(self):
        """
        https://www.socks-proxy.net/
        """
        rec = re.compile("onclick=\"select\(this\)\">([^<]+)</textarea>")
        resp = requests.get('http://dl.yunen.ml/skp/').text
        result = rec.findall(resp)
        proxies = []
        for proxy_item in result[0].split('\n'):
            if ":" not in proxy_item:
                continue
            elif 'UTC' in proxy_item:
                continue
            ip, port = proxy_item.split(":")
            proxies.append(('socks4', ip, int(port)))

        return list(set(proxies))
