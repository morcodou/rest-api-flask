import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

# from flask_migrate import Migrate
# from flask_uploads import configure_uploads, patch_request_class
# from libs.image_helper import IMAGES_SET

from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

from db import db

from ma import ma
from marshmallow import ValidationError


from oa import oauth

# from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, User, SetPassword
from resources.github_login import GithubLogin, GithubAuthorize

# , TokenRefresh, UserLogout
# from resources.confirmation import Confirmation, ConfirmationByUser
# from resources.item import Item, ItemList
# from resources.store import Store, StoreList
# from resources.image import ImageUpload, Image, AvatarUpload, Avatar


app = Flask(__name__)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")

# patch_request_class(app, 32 * 1024 * 1024)
# configure_uploads(app, IMAGES_SET)

api = Api(app)
jwt = JWTManager(app)
# migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


# # This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
# @jwt.token_in_blacklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     return (
#         decrypted_token["jti"] in BLACKLIST
#     )  # Here we blacklist particular JWTs that have been created in the past.


# api.add_resource(Store, "/store/<string:name>")
# api.add_resource(StoreList, "/stores")
# api.add_resource(Item, "/item/<string:name>")
# api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(GithubLogin, "/login/github")
api.add_resource(GithubAuthorize, "/login/github/authorized")
api.add_resource(SetPassword, "/user/password")
# api.add_resource(TokenRefresh, "/refresh")
# api.add_resource(UserLogout, "/logout")
# api.add_resource(Confirmation, "/confirmation/<string:confirmation_id>")
# api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")
# api.add_resource(ImageUpload, "/upload/image")
# api.add_resource(Image, "/image/<string:filename>")
# api.add_resource(AvatarUpload, "/upload/avatar")
# api.add_resource(Avatar, "/avatar/<int:user_id>")


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    oauth.init_app(app)
    app.run(port=5000)
