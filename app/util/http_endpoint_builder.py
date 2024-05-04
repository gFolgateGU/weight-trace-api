class HttpEndpointBuilder:
    def __init__(self, http_url):
        self.http_url = http_url

    @classmethod
    def create(cls, base_url, route, param_dict=None):
        if param_dict is None:
            http_url = base_url + "/" + route
            return cls(http_url).get_url()

    def get_url(self):
        return self.http_url
