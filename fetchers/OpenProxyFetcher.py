from .BaseFetcher import BaseFetcher
import requests


class OpenProxyFetcher(BaseFetcher):
    """
    https://openproxylist.xyz/socks4.txt
    https://openproxylist.xyz/socks5.txt
    """

    def fetch(self):

        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocol是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """
        target_list = [{
            "protocol": "socks4",
            "url": "https://openproxylist.xyz/socks4.txt"
        }, {
            "protocol": "socks5",
            "url": "https://openproxylist.xyz/socks5.txt"
        }]
        proxies = []
        for target in target_list:
            url = target["url"]
            protocol = target["protocol"]
            resp = requests.get(url).text.split("\n")
            for data in resp:
                if ":" not in data: continue
                ip, port = data.split(":")
                proxies.append((protocol, ip, int(port)))

        return list(set(proxies))
