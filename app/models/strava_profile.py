from dataclasses import dataclass, asdict

@dataclass
class StravaProfile:
    firstname: str
    lastname: str
    bio: str
    city: str
    state: str
    profile: str
    created_at: str

    @classmethod
    def create(cls, json_data):
        model_keys = ["firstname", "lastname", "bio", "city", "state", "profile", "created_at"]
        model_data = dict()
        for key in model_keys:
            if key in json_data:
                model_data[key] = json_data[key]
            else:
                model_data[key] = ""
        return cls(firstname=model_data["firstname"],
                   lastname=model_data["lastname"],
                   bio=model_data["bio"],
                   city=model_data["city"],
                   state=model_data["state"],
                   profile=model_data["profile"],
                   created_at=model_data["created_at"])

    def to_json(self):
        return asdict(self)