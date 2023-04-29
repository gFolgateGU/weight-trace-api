import bcrypt

from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    _id: Optional[str] = Field(alias="_id")
    username: str
    hashed_password: str
    salt: str

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def create(cls, username: str, password: str):
        salt = bcrypt.gensalt().decode('utf-8')
        salted_password = (password + salt).encode('utf-8')
        hashed_password = bcrypt.hashpw(salted_password, bcrypt.gensalt()).decode('utf-8')
        return cls(username=username, hashed_password=hashed_password, salt=salt)
    
    def to_json(self):
        return self.json()

    def to_bson(self):
        return self.dict(by_alias=True, exclude_unset=True)

    def verify_password(self, password: str):
        salted_password = (password + self.salt).encode('utf-8')
        hashed_password = bcrypt.hashpw(salted_password, self.hashed_password.encode('utf-8'))
        return hashed_password == self.hashed_password.encode('utf-8')

    