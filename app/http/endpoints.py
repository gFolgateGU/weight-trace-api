from flask import Flask, jsonify, request, redirect, session
import requests
from app import application
from app.services.example import Example
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

application.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
jwt = JWTManager(application)

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
    #session["access_token"] = access_token
    return redirect(application.strava_redirect_app_url)


@application.route("/api/data", methods=["GET"])
@jwt_required()
def index():
    ex = Example()
    data = ex.example_json()
    return jsonify(data)

@application.route("/api/test", methods=["GET"])
def test():
    user_service = getattr(application, 'user_service')
    if user_service is not None:
        users = user_service.get_all_users()
        ex = Example()
        data = ex.example_json()
        return jsonify(data)

@application.route("/api/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]

    user_service = getattr(application, 'user_service')

    user_ok = user_service.register_user(email, password)

    if user_ok:
        return jsonify({
            "id": email
        })
    else:
        return {"msg": "Unable to register user"}, 401

@application.route("/api/login", methods=["POST"])
def login_user():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    user_service = getattr(application, 'user_service')

    user_ok = user_service.verify_user(email, password)
    
    if not user_ok:
        return {"msg": "Wrong email or password"}, 401
    
    access_token = create_access_token(identity=email)
    response = { "access_token": access_token }
    return response

@application.route("/api/logout", methods=["POST"])
def logout_user():
    response = jsonify( {"msg": "logout successful"} )
    unset_jwt_cookies(response)
    return response