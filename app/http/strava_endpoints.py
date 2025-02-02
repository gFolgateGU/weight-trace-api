from flask import Flask, jsonify, request, redirect, session
import requests
from app.util.token_gen import decode_session_token
from app import application
from app.util.http_auth_hdr import HttpAuthHdr

@application.route("/api/athlete", methods=["GET"])
def get_athlete_overview():
    if "strava_access_token" in session and "session_token" in session:
        # Extract the authenticated user from the session token
        payload = decode_session_token(session["session_token"])
        auth_user_id = payload["user_id"]
        
        # Get the athlete summary model
        strava_service = application.strava_service
        athlete = strava_service.get_athlete_summary(session["strava_access_token"],
                                                     auth_user_id)
                                                     
        if athlete is None:
            return jsonify({"error": "Unable to get athlete information"})
        return athlete.to_json()
    else:
        # User is not logged in
        return jsonify({"error": 'user must be logged in!'})
