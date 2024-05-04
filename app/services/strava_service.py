from app.models.strava_profile import StravaProfile

from app.util.http_auth_hdr import HttpAuthHdr
from app.util.http_endpoint_builder import HttpEndpointBuilder

class StravaService:
    def __init__(self, base_url, http_rqster):
        self.base_url = base_url
        self.http_rqstr = http_rqster


    def get_athlete_summary(self, strava_token):
        # 1) Create the authentication header
        auth_hdr = HttpAuthHdr.create(strava_token)

        # 2) Create the HTTP request URL
        http_url = HttpEndpointBuilder.create(self.base_url, 'athlete')

        # 3) Get athlete JSON data
        athlete_json = self.http_rqstr.get_data(http_url, auth_hdr)
        if len(athlete_json) == 0:
            return None

        # 4) Create the Strava Profile Model
        model = StravaProfile.create(athlete_json)
        return model

        