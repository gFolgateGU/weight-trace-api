from flask import Flask, jsonify, request, redirect, session
import requests
from app import application
from app.services.user_service import UserService
from app.util.token_gen import generate_session_token
from app.models.models import User

@application.route("/api/auth", methods=["GET"])
def auth():
    try:
        # Build the authorization URL
        strava_auth_url = application.strava_auth_url
        strava_client_id = application.strava_client_id
        redirect_url = application.strava_redirect_url
        auth_url = f"{strava_auth_url}?client_id={strava_client_id}&redirect_uri={redirect_url}&response_type=code&scope=read_all"

        # Return the authorization URL embedded within a JSON object
        return jsonify({"auth_url": auth_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@application.route("/api/authcallback")
def authcallback():
    try:
        code = request.args.get('code')
        data = {
            "client_id": application.strava_client_id,
            "client_secret": application.strava_client_secret,
            "code": code,
            "grant_type": "authorization_code"
        }
        token_url = application.strava_token_url
        response = requests.post(token_url, data=data)
        token = response.json().get("access_token")
        athlete = response.json().get("athlete")

        if token is None:
            return redirect(application.strava_redirect_app_url)

        user_service = application.user_service
        auth_user = user_service.create_user(strava_id=athlete["id"],
                                             username=athlete["username"])

        session_token = generate_session_token(auth_user.strava_id)

        session["strava_access_token"] = token
        session["session_token"] = session_token
        return redirect(application.strava_redirect_app_url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@application.route("/api/isauth", methods=["GET"])
def is_auth():
    if "strava_access_token" in session:
        # User is logged in, return the profile data
        client_token = dict()
        client_token['token'] = 'logged_in'
        return jsonify(client_token), 200
    else:
        # User is not logged in
        return jsonify({"error": 'user must be logged in!'})

@application.route("/api/logout", methods=["GET"])
def logout_user():
    session.clear()
    response = jsonify( {"msg": "logout successful"} )
    return response