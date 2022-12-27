from flask import Flask, jsonify, request
from app import application
from app.services.example import Example

@application.route("/api/data", methods=["GET"])
def index():
    ex = Example()
    data = ex.example_json()
    return jsonify(data)