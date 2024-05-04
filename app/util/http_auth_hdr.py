class HttpAuthHdr:
    def __init__(self, access_token):
        self.access_token = access_token
        self.auth_hdr = dict()
    
    def build(self):
        bearer = f'Bearer {self.access_token}'
        self.auth_hdr["Authorization"] = bearer
        return self.auth_hdr
        