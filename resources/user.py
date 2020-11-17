import traceback
from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    fresh_jwt_required,
)
from schemas.user import UserSchema
from models.user import UserModel
from blacklist import BLACKLIST
from libs.mailgun import MailGunException

from libs.test_flask_lib import function_accessing_global

# from models.confirmation import ConfirmationModel
from libs.strings import gettext


user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {"message": gettext("user_username_exists")}, 400

        # if UserModel.find_by_email(user.email):
        #     return {"message": gettext("user_email_exists")}, 400

        try:
            user.save_to_db()
            # confirmation = ConfirmationModel(user.id)
            # confirmation.save_to_db()
            # user.send_confirmation_email()
            return {"message": gettext("user_registratered")}, 201
        # except MailGunException as mge:
        #     user.delete_from_db()
        #     return {"message": str(mge)}, 500
        except:
            traceback.print_exc()
            user.delete_from_db()
            return {"message": gettext("user_error_creating")}, 500


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        user.delete_from_db()
        return {"message": gettext("user_deleted")}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):

        user_json = request.get_json()
        # user_data = user_schema.load(user_json, partial=("email",))
        user_data = user_schema.load(user_json)

        user = UserModel.find_by_username(user_data.username)

        # this is what the `authenticate()` function did in security.py
        if user and user.password and safe_str_cmp(user.password, user_data.password):
            # confirmation = user.most_recent_confirmation
            # if confirmation and confirmation.confirmed:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200
            # return {"message": gettext("user_not_confirmed").format(user.username)}, 400

        return {"message": gettext("user_invalid_credentials")}, 401


# class UserLogout(Resource):
#     @classmethod
#     @jwt_required
#     def post(cls):
#         jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
#         user_id = get_jwt_identity()
#         BLACKLIST.add(jti)
#         return {"message": gettext("user_logged_out").format(user_id)}, 200


# class TokenRefresh(Resource):
#     @classmethod
#     @jwt_refresh_token_required
#     def post(cls):
#         current_user = get_jwt_identity()
#         new_token = create_access_token(identity=current_user, fresh=False)
#         return {"access_token": new_token}, 200


class SetPassword(Resource):
    @classmethod
    @fresh_jwt_required
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)
        user = UserModel.find_by_username(user_data.username)

        if not user:
            return {"message": gettext("user_not_found")}, 404

        user.password = user_data.password
        return {"message": gettext("user_password_updated")}, 201