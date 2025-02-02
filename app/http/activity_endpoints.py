from flask import Flask, jsonify, request, redirect, session
import requests
from app import application
from app.util.http_auth_hdr import HttpAuthHdr

@application.route("/api/activities", methods=["GET"])
def get_activities():
    if "session_token" in session:
        return jsonify({"testdata": "test description"})
    else:
        # User is not logged in
        return jsonify({"error": 'user must be logged in!'})
