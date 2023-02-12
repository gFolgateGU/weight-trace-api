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

@application.route("/api/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]

    print('------')
    print(f'Your email: {email}')
    print(f'Your password: {password}')

    return jsonify({
        "id": email
    })

@application.route("/api/login", methods=["POST"])
def login_user():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return {"msg": "Wrong email or password"}, 401

    print('------')
    print(f'Your login email: {email}')
    print(f'Your login password: {password}')

    access_token = create_access_token(identity=email)
    response = { "access_token": access_token }
    return response

@application.route("/api/logout", methods=["POST"])
def logout_user():
    response = jsonify( {"msg": "logout successful"} )
    unset_jwt_cookies(response)
    return response