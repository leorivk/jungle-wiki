from flask import Blueprint, request, make_response, redirect
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(fresh=False)
def refresh():
    try:
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)

        previous = request.referrer
        if previous is None:
            previous = "/"

        response = make_response(redirect(previous))
        response.set_cookie('access_token', new_token, max_age=60*60*24, httponly=True)  # 쿠키의 이름과 max_age 설정

        return response
    except Exception as e:
        return redirect("/logout")


