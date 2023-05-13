from .BaseFetcher import BaseFetcher
import requests
import time


class ProxyScanFetcher(BaseFetcher):
    """
    https://www.proxyscan.io/api/proxy?last_check=9800&uptime=50&limit=20&_t={{ timestamp }}
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocol是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """
        proxies = []
        # 此API为随机获取接口，获取策略为：重复取十次后去重
        for protocol in ['http', 'https', 'socks4', 'socks5']:
            url = f"https://www.proxyscan.io/download?type={protocol}&_t={time.time()}"
            resp = requests.get(url).text
            for data in resp.split("\n"):
                if data == "":
                    continue
                [ip, port] = data.split(":")
                proxies.append((protocol, ip, port))

        return list(set(proxies))
