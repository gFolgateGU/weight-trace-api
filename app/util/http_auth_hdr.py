class HttpAuthHdr:
    def __init__(self, auth_hdr):
        self.auth_hdr = auth_hdr
    
    @classmethod
    def create(cls, access_token):
        bearer = f'Bearer {access_token}'
        auth_hdr = dict()
        auth_hdr['Authorization'] = bearer
        return cls(auth_hdr).get_auth_hdr()

    def get_auth_hdr(self):
        return self.auth_hdr
        