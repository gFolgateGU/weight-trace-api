from flask import Flask, jsonify, request, redirect, session
import requests
from app import application
from app.services.example import Example
from app.util.http_auth_hdr import HttpAuthHdr

@application.route("/api/athlete", methods=["GET"])
def get_athlete_overview():
    if "strava_access_token" in session:
        # User is logged in, return the profile data
        url = application.strava_base_url + "/athlete"
        hdr = HttpAuthHdr(session["strava_access_token"]).build()
        response = requests.get(url, headers=hdr)
        if response.status_code == 200:
            data = response.json()
            return data
        ex = Example()
        data = ex.example_json()
        return jsonify(data)
    else:
        # User is not logged in
        return jsonify({"error": 'user must be logged in!'})
