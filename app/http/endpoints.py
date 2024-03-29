from flask import Flask, jsonify, request
from app import application
from app.services.example import Example
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

application.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
jwt = JWTManager(application)

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