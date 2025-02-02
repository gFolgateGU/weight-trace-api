from app.models.strava_profile import StravaProfile

from app.util.http_auth_hdr import HttpAuthHdr
from app.util.http_endpoint_builder import HttpEndpointBuilder

class StravaService:
    def __init__(self, base_url, http_rqster):
        self.base_url = base_url
        self.http_rqstr = http_rqster

    def get_athlete_stats(self, auth_hdr, user_id):
        http_url = HttpEndpointBuilder.create(self.base_url, f'athletes/{user_id}/stats')

        stats_json = self.http_rqstr.get_data(http_url, auth_hdr)
        if (len(stats_json) == 0):
            return None
        
        return stats_json
    
    def get_athlete_summary(self, strava_token, user_id):
        # 1) Create the authentication header
        auth_hdr = HttpAuthHdr.create(strava_token)

        # 2) Create the HTTP request URL
        http_url = HttpEndpointBuilder.create(self.base_url, 'athlete')

        # 3) Get athlete JSON data
        athlete_json = self.http_rqstr.get_data(http_url, auth_hdr)
        if len(athlete_json) == 0:
            print('here')
            return None

        stats_json = self.get_athlete_stats(auth_hdr, user_id)
        if stats_json is not None:
            athlete_json["activity_stats"] = stats_json

        # 4) Create the Strava Profile Model
        model = StravaProfile.create(athlete_json)
        return model
        #return None

        