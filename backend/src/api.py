import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
database = "database.db"
setup_db(app, database)
CORS(app)

TOTAL_ITEMS_PER_PAGE = 10


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES


@app.route('/')
@requires_auth(permission="post:drinks")
def test(payload):
    return f"hey"


'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks", methods=["GET"])
def get_drinks():
    # try:
    page = request.args.get("page", 1)
    all_drinks = Drink.query.paginate(
                    page=page,
                    max_per_page=TOTAL_ITEMS_PER_PAGE)
    drinks = [drink.short() for drink in all_drinks.items]

    return jsonify({
        "success": True,
        "drinks": drinks
    })

    # except Exception as e:
    #     abort(500, "an error occured on the server")


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks-detail")
@requires_auth(permission="get:drinks-detail")
def get_drinks_details(payload):
    try:
        page = request.args.get("page", 1)
        all_drinks = Drink.query.paginate(
                        page=page,
                        max_per_page=TOTAL_ITEMS_PER_PAGE)
        drinks = [drink.long() for drink in all_drinks.items]

        return jsonify({
            "success": True,
            "drinks": drinks
        })

    except Exception as e:
        abort(500, "an error occured on the server")


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks", methods=["POST"])
@requires_auth(permission="post:drinks")
def create_drink(payload):
    data = request.get_json()
    required_fields = ["title", "recipe"]
    required_recipe = ["color", "name", "parts"]

    for field in required_fields:
        if field not in data:
            abort(400, f"required field missing: {field}")

    for recipe in required_recipe:
        if recipe not in data["recipe"].keys():
            abort(400, f"required recipe attribute missing: {recipe}")

    print(json.dumps(data["recipe"]))
    drink = Drink(title=data["title"],
                  recipe=f'[{json.dumps(data["recipe"])}]')
    drink.insert()

    return jsonify({"hello": "hello"})


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": f"{error}",
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": f"{error}"
    }), 400


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_errors(error):
    return jsonify({
        "error": error.status_code,
        "message": error.error
    }), error.status_code
