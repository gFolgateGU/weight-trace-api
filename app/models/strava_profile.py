from dataclasses import dataclass, asdict

@dataclass
class ActivityTotal:
    count: int
    distance: float
    moving_time: int
    elapsed_time: int
    elevation_gain: float
    achievement_count: int = 0  # default value since not all totals include it

@dataclass
class ActivityStats:
    recent_ride_totals: ActivityTotal
    recent_run_totals: ActivityTotal
    recent_swim_totals: ActivityTotal
    ytd_ride_totals: ActivityTotal
    ytd_run_totals: ActivityTotal
    ytd_swim_totals: ActivityTotal
    all_ride_totals: ActivityTotal
    all_run_totals: ActivityTotal
    all_swim_totals: ActivityTotal

@dataclass
class StravaProfile:
    firstname: str
    lastname: str
    bio: str
    city: str
    state: str
    profile: str
    created_at: str
    activity_stats: ActivityStats

    @classmethod
    def create(cls, json_data):
        # Extracting model keys
        model_keys = ["firstname", "lastname", "bio", "city", "state", "profile", "created_at"]
        model_data = {key: json_data.get(key, "") for key in model_keys}

        # Extracting and creating ActivityStats
        activity_stats_data = json_data.get("activity_stats", {})
        activity_stats = ActivityStats(
            recent_ride_totals=ActivityTotal(**activity_stats_data.get("recent_ride_totals", {})),
            recent_run_totals=ActivityTotal(**activity_stats_data.get("recent_run_totals", {})),
            recent_swim_totals=ActivityTotal(**activity_stats_data.get("recent_swim_totals", {})),
            ytd_ride_totals=ActivityTotal(**activity_stats_data.get("ytd_ride_totals", {})),
            ytd_run_totals=ActivityTotal(**activity_stats_data.get("ytd_run_totals", {})),
            ytd_swim_totals=ActivityTotal(**activity_stats_data.get("ytd_swim_totals", {})),
            all_ride_totals=ActivityTotal(**activity_stats_data.get("all_ride_totals", {})),
            all_run_totals=ActivityTotal(**activity_stats_data.get("all_run_totals", {})),
            all_swim_totals=ActivityTotal(**activity_stats_data.get("all_swim_totals", {}))
        )

        return cls(
            firstname=model_data["firstname"],
            lastname=model_data["lastname"],
            bio=model_data["bio"],
            city=model_data["city"],
            state=model_data["state"],
            profile=model_data["profile"],
            created_at=model_data["created_at"],
            activity_stats=activity_stats
        )

    def to_json(self):
        return asdict(self)
