from flask import Flask, request, session, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, User

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super-secret-key"

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


# -------------------------
# CLEAR SESSION (TEST HELPER)
# -------------------------
@app.route("/clear", methods=["GET"])
def clear():
    session.clear()
    return {}, 204


# -------------------------
# LOGIN
# -------------------------
class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")

        user = User.query.filter(User.username == username).first()

        if user:
            session["user_id"] = user.id
            return make_response(user.to_dict(), 200)

        return make_response({"error": "User not found"}, 404)


# -------------------------
# LOGOUT
# -------------------------
class Logout(Resource):
    def delete(self):
        session.pop("user_id", None)
        return make_response({}, 204)


# -------------------------
# CHECK SESSION
# -------------------------
class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")

        if user_id:
            user = User.query.get(user_id)
            return make_response(user.to_dict(), 200)

        return make_response({}, 401)


# -------------------------
# ROUTES
# -------------------------
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
