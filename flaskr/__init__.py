import json
import datetime
import jwt
from my_functions import code_gen, random_char
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, setup_db, User, Code, Station, Consume, Connexion
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta

# global variables
HASH_METHOD = 'pbkdf2:sha256:260000'
SECRET_KEY = "mySECRET_KEY"
JWT_ALGO = "HS256"


# response style
def make_json_response(code, message, success, detail="", data=None):
    return jsonify({
        "code": code,
        "message": message,
        "detail": detail,
        "success": success,
        "data": data
    }), code


# jwt token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", None)
        if not auth:
            return make_json_response(code=401, message="authorization_header_missing", success=False, detail="Authorization header is expected")

        parts = auth.split()
        if parts[0].lower() != "bearer":
            return make_json_response(code=401, message="invalid_header", success=False, detail="Authorization header must start with Bearer")
        if len(parts) == 1:
            return make_json_response(code=401, message="invalid_header", success=False, detail="Token not found")
        if len(parts) > 2:
            return make_json_response(code=401, message="invalid_header", success=False, detail="Authorization header must be Bearer token")

        token = parts[1]
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGO)
            user = User.query.filter(
                User.user_id.like(data['user_id'])).first()
            current_user = user.format_without_password()
        except:
            return make_json_response(code=401, message="invalid_token", success=False, detail="Token is invalid !!")

        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)

    """ Set up CORS. Allow '*' for origins."""
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """ Use the after_request decorator to set Access-Control-Allow"""
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

#####################################################################################

    # This route generates ticket for a phone number and the amount paid
    @app.route("/generate", methods=['POST'])
    @token_required
    def get_code(current_user):

        # GETTING REQUEST BODY
        body = request.get_json()
        post_body = json.loads(json.dumps(body))

        if all(key in post_body for key in ("telephone", "montant")):
            telephone = body.get("telephone", None)
            montant = body.get("montant", None)

            codeGen = code_gen(6, '0123456789ABCDEF')
            # codeGen = "F6E735" # test : trying to generate an existing code

            # does this code exists already ?
            same_code = Code.query.filter(
                Code.hashcode.ilike('%'+codeGen+'%')).filter(Code.statut == 1).first()
            if same_code:
                get_code()  # restart the function to get a new unique code

            else:
                date_time = datetime.now()  # current timestamp

                code = Code(hashcode=codeGen,
                            statut=True, user_id=current_user["id"], telephone=telephone, montant=montant, date_time=date_time)
                code.insert()

                data = {
                    'username': current_user["name"],
                    # 'code': codeGen,
                    'telephone': telephone,
                    'montant': montant,
                    'datetime': date_time
                }

                return make_json_response(code=200, message="code_created", success=True, detail="It worked !!", data=data)

            return abort(422)

        else:
            return abort(400)

#####################################################################################

    # This route consumes a specific ticket by guessing the code
    @app.route("/moozle", methods=['POST'])
    def consume_code():

        # GETTING REQUEST BODY
        body = request.get_json()
        post_body = json.loads(json.dumps(body))

        if all(key in post_body for key in ("station_id", "code")):
            station_id = body.get("station_id", None)
            verify_code = body.get("code", None)

            # if station doesn't exist or have done many tries
            station_exists = Station.query.filter(
                Station.station_id.like(station_id)).first()
            if not station_exists:
                abort(401)
            elif station_exists.error >= 5:
                abort(403)

            # does this code exist ?
            code = Code.query.filter(
                Code.hashcode.like(verify_code)).filter(Code.statut == 1).first()
            if code:

                # changes the validity of the code to "used"
                code_update = Code.query.get(code.id)
                code_update.statut = False
                code_update.update()

                # creates a log for the event
                date_time = datetime.now()
                log = Consume(success=True, code_used=verify_code, consumed_by=station_id,
                              generated_by=code.user_id, date_time=date_time)
                log.insert()

                # reinitializes the margin of error
                station_exists.error = 0
                station_exists.update()

                data = {
                    "station": station_exists.name,
                    "montant": code.montant
                }

                return make_json_response(code=200, message="code_verified", detail="Valid code!", success=True, data=data)
            else:
                # increments error
                station_exists.error += 1
                station_exists.update()

                false_but_the_code_exists_query = Code.query.filter(
                    Code.hashcode.like(verify_code))
                false_but_the_code_exists = false_but_the_code_exists_query.first()

                if false_but_the_code_exists:
                    date_time = datetime.now()
                    log = Consume(success=False, code_used=verify_code, consumed_by=station_id,
                                  generated_by=false_but_the_code_exists.user_id, date_time=date_time)
                    log.insert()
                else:
                    date_time = datetime.now()
                    log = Consume(success=False, code_used=verify_code, consumed_by=station_id,
                                  generated_by=None, date_time=date_time)
                    log.insert()

                return abort(404)
        else:
            abort(400)

#####################################################################################

    # This route creates a user
    @app.route("/users", methods=['POST'])
    def create_user():

        # GETTING REQUEST BODY
        body = request.get_json()
        post_body = json.loads(json.dumps(body))

        if all(key in post_body for key in ("name", "password")):
            name = body.get("name", None)
            password = body.get("password", None)
            if (name and password):

                # is there an user with that name
                query = User.query.filter(User.name.ilike('%'+name+'%'))
                user_with_that_name = query.first()
                if user_with_that_name:
                    return make_json_response(code=301, message="username_duplicated", detail="Ce nom d'utilisateur existe déjà. Veuillez vous connectez!", success=True)

                else:
                    # hash
                    hash_pass = generate_password_hash(
                        password, method=HASH_METHOD)
                    # store hashpass without method
                    hash_pass_without_method = hash_pass.replace(
                        HASH_METHOD, '')

                    user = User(user_id=random_char(),
                                name=name, password=hash_pass_without_method)
                    user.insert()

                    return make_json_response(code=200, message="user_inserted", detail="User created successfully", success=True, data=user.format_without_password())

            else:
                abort(422)
        else:
            abort(400)

#####################################################################################

    # This route modifies a user
    @app.route("/users", methods=['PATCH'])
    @token_required
    def update_user(current_user):

        # GETTING REQUEST BODY
        body = request.get_json()
        post_body = json.loads(json.dumps(body))

        # UPDATE USER
        if all(key in post_body for key in ("name", "password")):
            new_name = body.get("name", None)
            new_password = body.get("password", None)

            if (new_name or new_password):
                user_with_that_id = User.query.get(current_user["id"])
                if user_with_that_id:
                    # hash
                    hash_pass = generate_password_hash(
                        new_password, method=HASH_METHOD)
                    # store hashpass without method
                    hash_pass_without_method = hash_pass.replace(
                        HASH_METHOD, '')

                    user_with_that_id.user_id = random_char()
                    if new_name:
                        user_with_that_id.name = new_name
                    if new_password:
                        user_with_that_id.password = hash_pass_without_method

                    user_with_that_id.update()

                    if new_name or new_password:
                        return make_json_response(code=200, message="user_updated", detail="user modified", success=True, data=user_with_that_id.format_without_password())
                    else:
                        return abort(400)
                else:
                    abort(404)
            else:
                abort(400)
        else:
            abort(400)

#####################################################################################

    # This route logs a user in
    @app.route("/login", methods=['POST'])
    def connect_user():

        # GETTING REQUEST BODY
        body = request.get_json()
        post_body = json.loads(json.dumps(body))

        # CONNECT USER
        if all(key in post_body for key in ("name", "password")):
            user_name = body.get("name", None)
            user_pass = body.get("password", None)

            if (user_name and user_pass):

                query = User.query.filter(User.name.ilike('%'+user_name+'%'))
                user_with_that_name = query.first()

                if user_with_that_name:
                    if check_password_hash(HASH_METHOD+user_with_that_name.password, user_pass):
                        new_user_id = random_char()
                        user_with_that_name.user_id = new_user_id
                        user_with_that_name.update()

                        # inserts a connexion log for the event
                        date_time = datetime.now()
                        con = Connexion(
                            id_user=user_with_that_name.id, date_time=date_time)
                        con.insert()

                        # generates the JWT Token
                        token = jwt.encode({
                            'user_id': str(user_with_that_name.user_id),
                            'exp': datetime.utcnow() + timedelta(minutes=30)
                        }, SECRET_KEY, algorithm=JWT_ALGO)

                        return make_json_response(code=200, message="user_verified", detail=user_name, success=True, data={"token": token})
                    else:
                        abort(401)
                else:
                    abort(401)
            else:
                abort(422)
        else:
            abort(400)

#####################################################################################

    # This route returns all users
    @app.route("/users", methods=['GET'])
    def get_users():
        query = User.query.all()
        users = [users.format_without_password() for users in query]
        data = {
            "users": users,
            "total_users": len(users)
        }
        return make_json_response(code=200, message="get_all_users", detail="List of all users", success=True, data=data)

#####################################################################################

    # This route creates stations
    @app.route("/stations", methods=['POST'])
    def create_station():

        # GETTING REQUEST BODY
        body = request.get_json()
        post_body = json.loads(json.dumps(body))

        # CREATE STATION
        if all(key in post_body for key in ("station_id", "name")):
            station_id = body.get("station_id", None)
            name = body.get("name", None)
            gps_code = body.get("gps_code", None)

            if (station_id):
                # is there a station with that id
                query = Station.query.filter(
                    Station.station_id.ilike('%'+station_id+'%'))
                station_with_that_id = query.first()
                if station_with_that_id:
                    abort(422)

                else:
                    station = Station(station_id=station_id,
                                      name=name, gps_code=gps_code, error=None)
                    station.insert()

                    return make_json_response(code=200, message="station_inserted", detail="Station created successfully", success=True, data=station.format())
            else:
                abort(422)

#####################################################################################

# This route connexion logs
    @app.route("/connexions", methods=['GET'])
    def get_con_logs():
        query = Connexion.query.all()
        con_logs = [con_logs.format() for con_logs in query]
        data = {
            "logs": con_logs
        }
        return make_json_response(code=200, message="get_con_logs", detail="Connexion logs", success=True, data=data)

#####################################################################################

    # ERROR HANDLER

    @app.errorhandler(404)
    def not_found(error):
        return make_json_response(code=404, message="not_found", success=False, detail="resource not found")

    @app.errorhandler(422)
    def unprocessable(error):
        return make_json_response(code=422, message="unprocessable", success=False, detail="Something went wrong!")

    @app.errorhandler(401)
    def unauthorized(error):
        return make_json_response(code=401, message="unauthorized", success=False, detail="Authentication failed!")

    @app.errorhandler(403)
    def forbidden(error):
        return make_json_response(code=403, message="forbidden", success=False, detail="We cannot give you this access!")

    @app.errorhandler(400)
    def bad_request(error):
        return make_json_response(code=400, message="bad_request", success=False, detail="You should review your request.")

    return app
