from flask import Blueprint, jsonify, request, Flask
from flask_sqlalchemy import Pagination
from marshmallow import Schema, fields
from app.scheduled.layers import models
from app.session_generator.create_session import get_session
from app.scheduled.layers.models import GrantEntrySchema
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_swagger_ui import get_swaggerui_blueprint

grants_bp = Blueprint('api', __name__)
grant_schema = GrantEntrySchema()

# Swagger configs
spec = APISpec(
    title='Grant-Tracking-Platform-Swagger-Documentation',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Grant Tracking Platform'
    }
)


app = Flask(__name__)


class GistParameter(Schema):
    gist_id = fields.Int()


class GistSchema(Schema):
    id = fields.Int()
    content = fields.Str()


@grants_bp.route('/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())


DAFAULT_ROWS_PER_PAGE = 5
# export FLASK_APP=__init__.py
# FLASK_DEBUG=1
# flask run
# http://127.0.0.1:5000/api/grants?page=1


@grants_bp.route('/grants', methods=['GET'])
def available_grants():
    """Test view
        ---
        get:
            tags:
                - Users
            summary: searches grants
            operationId: searchGrants
            description:  |
                By passing in the appropriate options, you can search for
                available grants in the system.
            parameters:
            -   in: query
                name: skip
                description: number of records to skip for pagination
                schema:
                    type: integer
                    format: int32
                    minimum: 0

            -   in: query
                name: rows
                description: maximum number of records to return
                schema:
                    type: integer
                    format: int32
                    minimum: 0
                    maximum: 50
            responses:
                200:
                    description: search results matching criteria
                    content:
                        application/json:
                            schema: GrantEntrySchema
                400:
                    description: bad input parameter
    """
    number_of_rows = request.args.get('rows', DAFAULT_ROWS_PER_PAGE, type=int)
    db_session = get_session()
    page = request.args.get("page", 1, type=int)
    with db_session as session:
        query_result = session.query(models.GrantEntry).all()
        grant_list = []

    for grant in query_result:
        grant_list.append(grant_schema.dump(grant))

    start = (page - 1) * number_of_rows
    print(start + 1)
    end = start + number_of_rows
    print(end)
    items = grant_list[start:end]
    grants_paginate = Pagination(query=None, page=None, per_page=None,
                                 total=len(items),
                                 items=items)
    # total_pages = float(len(grant_list) / ROWS_PER_PAGE)
    # if page == ceil(total_pages) + 1:
    #     print("ERROR" + str(page))
    return jsonify(grants_paginate.items)


@grants_bp.route('/test', methods=['GET'])
def test():
    """Test view
        ---
        get:
            tags:
                - Users
            summary: searches grants
            operationId: testSearch
            description:  |
                By passing in the appropriate options, you can search for
                available grants in the system.
            parameters:
            -   in: query
                name: searchString
                description: pass an optional search string for looking up inventory
                required: false
                schema:
                    type: string

            -   in: query
                name: skip
                description: number of records to skip for pagination
                schema:
                    type: integer
                    format: int32
                    minimum: 0

            -   in: query
                name: limit
                description: maximum number of records to return
                schema:
                    type: integer
                    format: int32
                    minimum: 0
                    maximum: 50
            responses:
                200:
                    description: search results matching criteria
                    content:
                        application/json:
                            schema: GrantEntrySchema
                400:
                    description: bad input parameter
    """
    return 'Hello World'


app.register_blueprint(grants_bp)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

spec.components.schema("GrantEntry", schema=GrantEntrySchema)
with app.test_request_context():
    spec.path(view=test)
    spec.path(view=available_grants)





