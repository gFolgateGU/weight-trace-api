from operator import truediv
from flask import Flask

application = Flask(__name__)
application.debug = True

from app.http.activity_endpoints import *
from app.http.auth_endpoints import *
from app.http.strava_endpoints import *
from app.util.token_gen import *