import os
import sys
import json

from app import application

from app.services.strava_service import StravaService

from app.util.http_request import HttpRequest

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def parse_app_config(app, config_file):
    """
    Load and parse the input JSON file for app specific data

    Args:
        config_file (str): The name of the JSON file to parse.

    Returns:
        A dictionary containing the parsed app config data.

    """
    # Load the JSON file into a dictionary
    with open(config_file) as f:
        cfg_data = json.load(f)

    return cfg_data
    
def bind_cfg_deps(app, cfg_data):
    """
    Add config specific attributes to the application class
    for other services to reference within the project

    Args:
        app (obj): The encompassing flask application object
        cfg_data (dict): A dictionary containing the parsed app
        config data.

    Returns:
        None

    """
    if "host_info" in cfg_data:
        if "host" in cfg_data["host_info"]:
            setattr(app, "host_name", cfg_data["host_info"]["host"])
        if "port" in cfg_data["host_info"]:
            setattr(app, "host_port", cfg_data["host_info"]["port"])

    if "db_info" in cfg_data:
        if "db_name" in cfg_data["db_info"]:
            setattr(app, "db_name", cfg_data["db_info"]["db_name"])
        if "conn_str" in cfg_data["db_info"]:
            setattr(app, "db_conn_str", cfg_data["db_info"]["conn_str"])      
            # Create a new client and connect to the server
            client = MongoClient(app.db_conn_str, server_api=ServerApi('1'))
            setattr(app, "mongo_client", client)

    if "app_secrets" in cfg_data:
        if "secret_key" in cfg_data["app_secrets"]:
            setattr(app, "secret_key", cfg_data["app_secrets"]["secret_key"])

    if "strava_api_info" in cfg_data:
        if "client_id" in cfg_data["strava_api_info"]:
            setattr(app, "strava_client_id", cfg_data["strava_api_info"]["client_id"])
        if "client_secret" in cfg_data["strava_api_info"]:
            setattr(app, "strava_client_secret", cfg_data["strava_api_info"]["client_secret"])
        if "auth_url" in cfg_data["strava_api_info"]:
            setattr(app, "strava_auth_url", cfg_data["strava_api_info"]["auth_url"])
        if "base_url" in cfg_data["strava_api_info"]:
            setattr(app, "strava_base_url", cfg_data["strava_api_info"]["base_url"])
        if "redirect_url" in cfg_data["strava_api_info"]:
            setattr(app, "strava_redirect_url", cfg_data["strava_api_info"]["redirect_url"])
        if "redirect_app_url" in cfg_data["strava_api_info"]:
            setattr(app, "strava_redirect_app_url", cfg_data["strava_api_info"]["redirect_app_url"])
        if "token_url" in cfg_data["strava_api_info"]:
            setattr(app, "strava_token_url", cfg_data["strava_api_info"]["token_url"])

def bind_deps(app):
    """
    Apply dependency injection and add class dependencies to the application

    Args:
        app (obj): The encompassing flask application object

    Returns:
        None

    """
    # Create utlity services
    http_rqstr = HttpRequest()

    # Create Services
    strava_service = StravaService(base_url=app.strava_base_url, http_rqster=http_rqstr)
    setattr(app, "strava_service", strava_service)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Please enter an input configuration file')
        sys.exit()
    
    config_file = sys.argv[1]

    cfg_data = parse_app_config(application, config_file)
    bind_cfg_deps(application, cfg_data)
    bind_deps(application)
    
    host_name = getattr(application, 'host_name')
    host_port = getattr(application, 'host_port')

    if host_name and host_port:
        port = int(os.environ.get("PORT", host_port))
        application.run(host_name, port=port)
    else:
        print('Please specify a host port and host name in the cfg file')