import random
import json
import base64
class RandomProxyMiddleware:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        proxy_file = settings.get('PROXY_FILE')
        with open(proxy_file, 'r') as f:
            proxies = json.load(f).get('proxies', [])
        return cls(proxies)

    def process_request(self, request, spider):
        proxy = random.choice(self.proxy_list)
        request.meta['proxy'] = proxy

        # Handle proxy authentication
        if '@' in proxy:
            user_pass = proxy.split('@')[0].replace('http://', '').replace('https://', '')
            encoded_user_pass = base64.b64encode(user_pass.encode('utf-8')).decode('utf-8')
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
