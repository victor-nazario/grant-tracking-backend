from flask import Blueprint, jsonify, request, Flask, render_template
from flask_sqlalchemy import Pagination
from marshmallow import Schema, fields
from app.scheduled.layers import models
from app.session_generator.create_session import get_session
from app.scheduled.layers.models import GrantEntrySchema
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_swagger_ui import get_swaggerui_blueprint
import yaml

grants_bp = Blueprint('api', __name__)
grant_schema = GrantEntrySchema()


OPENAPI_SPEC = """
servers:
- url: http://localhost:8085/api/
  description: The development API server
"""

settings = yaml.safe_load(OPENAPI_SPEC)
# Swagger configs
spec = APISpec(
    title='Grant-Tracking-Platform-Swagger-Documentation',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    **settings
)


SWAGGER_URL = '/swagger'
API_URL = 'swagger.json'
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


@SWAGGER_BLUEPRINT.route('/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())


DEFAULT_ROWS_PER_PAGE = 5


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
                name: rows
                description: maximum number of records to return
                schema:
                    type: integer
                    format: int32
                    minimum: 5
                    maximum: 100

            -   in: query
                name: page
                description: current page number
                schema:
                    type: integer
                    format: int32
                    minimum: 1
            responses:
                200:
                    description: search results matching criteria
                    content:
                        application/json:
                            schema: GrantEntrySchema
                400:
                    description: bad input parameter
    """
    number_of_rows = request.args.get('rows', DEFAULT_ROWS_PER_PAGE, type=int)
    db_session = get_session()
    page = request.args.get("page", 1, type=int)
    with db_session as session:
        query_result = session.query(models.GrantEntry).all()
        grant_list = []

    for grant in query_result:
        grant_list.append(grant_schema.dump(grant))
    # sorting from the least recent date to most recent date
    # sorting from most recent date to the least recent date
    sorted_grant_list = sorted(grant_list, key=lambda date: date['close_date'], reverse=True)

    start = (page - 1) * number_of_rows
    end = start + number_of_rows
    items = sorted_grant_list[start:end]
    grants_paginate = Pagination(query=None, page=None, per_page=None,
                                 total=len(items),
                                 items=items)

    return jsonify(grants_paginate.items)


@grants_bp.route('/table')
def index():
    return render_template('table.html', title='Grant Tracking Platform')


@grants_bp.route('/data')
def data():
    db_session = get_session()
    query = db_session.query(models.GrantEntry)

    total_filtered = query.count()

    query_result = query.all()

    grant_list = []
    for grant in query_result:
        grant_list.append(grant_schema.dump(grant))

    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        descending = request.args.get(f'order[{i}][dir]') == 'desc'

        # sorting from most recent date to the least recent date
        if descending:
            grant_list = sorted(grant_list, key=lambda date: date['close_date'], reverse=True)

        # sorting from the least recent date to most recent date
        else:
            grant_list = sorted(grant_list, key=lambda date: date['close_date'])
        i += 1

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    items = grant_list[start:length + start]

    # response
    return {
        'data': [item for item in items],
        'recordsFiltered': total_filtered,
        'recordsTotal': total_filtered,
        'draw': request.args.get('draw', type=int),
    }


app.register_blueprint(grants_bp)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

spec.components.schema("GrantEntry", schema=GrantEntrySchema)
with app.test_request_context():
    spec.path(view=available_grants)

if __name__ == '__main__':
    app.run(debug=True)
