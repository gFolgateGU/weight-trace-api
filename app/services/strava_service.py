from app.models.strava_profile import StravaProfile

from app.util.http_auth_hdr import HttpAuthHdr
from app.util.http_endpoint_builder import HttpEndpointBuilder

class StravaService:
    def __init__(self, base_url, http_rqster, lru_cache):
        self.base_url = base_url
        self.http_rqstr = http_rqster
        self.lru_cache = lru_cache

    def get_athlete_stats(self, auth_hdr, user_id):
        http_url = HttpEndpointBuilder.create(self.base_url, f'athletes/{user_id}/stats')

        stats_json = self.http_rqstr.get_data(http_url, auth_hdr)
        if (len(stats_json) == 0):
            return None
        
        return stats_json
    
    def get_athlete_summary(self, strava_token, user_id):
        # 0) Check the LRU Cache for an existing athlete summary
        ath_summary_key = f'{user_id}_athlete_summary'
        ath_summary = self.lru_cache.get(ath_summary_key)
        if ath_summary is not None:
            print(f'retrieving {ath_summary_key} from cache')
            return ath_summary
        
        # 1) Create the authentication header
        auth_hdr = HttpAuthHdr.create(strava_token)

        # 2) Create the HTTP request URL
        http_url = HttpEndpointBuilder.create(self.base_url, 'athlete')

        # 3) Get athlete JSON data
        athlete_json = self.http_rqstr.get_data(http_url, auth_hdr)
        if len(athlete_json) == 0:
            return None

        stats_json = self.get_athlete_stats(auth_hdr, user_id)
        if stats_json is not None:
            athlete_json["activity_stats"] = stats_json

        # 4) Create and cache Strava Profile Model
        model = StravaProfile.create(athlete_json)
        self.lru_cache.put(ath_summary_key, model)
        print(f'storing {ath_summary_key} in cache')
        return model

        