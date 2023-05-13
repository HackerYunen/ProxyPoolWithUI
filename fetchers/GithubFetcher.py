from .BaseFetcher import BaseFetcher
import requests


class GithubFetcher(BaseFetcher):
    """
    https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt
    https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt
    https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt
    https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt
    https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt
    https://openproxylist.xyz/socks4.txt
    https://openproxylist.xyz/socks5.txt
    https://paste.wtf/paste.php?download&id=96
    https://paste.wtf/paste.php?download&id=97
    https://paste.wtf/paste.php?download&id=98
    """

    def fetch(self):

        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocol是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """
        target_list = [{
            "protocol": "http",
            "url": "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
        }, {
            "protocol": "socks4",
            "url": "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt"
        }, {
            "protocol": "socks5",
            "url": "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"
        }, {
            "protocol": "socks5",
            "url": "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"
        }, {
            "protocol": "http",
            "url": "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"
        }, {
            "protocol": "http",
            "url": "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt"
        }, {
            "protocol": "https",
            "url": "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt"
        }, {
            "protocol": "socks4",
            "url": "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt"
        }, {
            "protocol": "socks5",
            "url": "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt"
        }, {
            "protocol": "http",
            "url": "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt"
        }, {
            "protocol": "socks4",
            "url": "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt"
        }, {
            "protocol": "socks5",
            "url": "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt"
        }]
        proxies = []
        for target in target_list:
            url = target["url"]
            protocol = target["protocol"]
            url = url.replace("https://raw.githubusercontent.com/", "http://raw.yunen.ml/")
            resp = requests.get(url).text.split("\n")
            for data in resp:
                if ":" not in data:
                    continue
                ip, port = data.split(":")
                proxies.append((protocol, ip, int(port)))

        return list(set(proxies))
