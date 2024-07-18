GDOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.RandomProxyMiddleware': 543,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
}

# Path to the JSON file containing the proxy list
PROXY_FILE = 'proxies.json'
