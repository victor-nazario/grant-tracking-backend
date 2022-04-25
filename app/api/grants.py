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
    # sorting from the least recent date to most recent date
    # sorted_grant_list = sorted(grant_list, key=lambda x: x['close_date'])

    # sorting from most recent date to the least recent date
    sorted_grant_list = sorted(grant_list, key=lambda date: date['close_date'], reverse=True)

    start = (page - 1) * number_of_rows
    print(start + 1)
    end = start + number_of_rows
    print(end)
    items = sorted_grant_list[start:end]
    grants_paginate = Pagination(query=None, page=None, per_page=None,
                                 total=len(items),
                                 items=items)

    return jsonify(grants_paginate.items)


@app.route('/table')
def index():
    return render_template('table.html', title='Grant Tracking Platform')


@app.route('/api/data')
def data():
    db_session = get_session()
    query = db_session.query(models.GrantEntry)

    total_filtered = query.count()

    query_result = query.all()

    grant_list = []
    for grant in query_result:
        grant_list.append(grant_schema.dump(grant))

    # sorting
    # order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        # col_name = request.args.get(f'columns[{col_index}][data]')
        # if col_name not in ['close_date']:
        #     col_name = 'close_date'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        # col = grant_list[0].get(col_name, None)
        # print(col)

        # sorting from most recent date to the least recent date
        if descending:
            grant_list = sorted(grant_list, key=lambda date: date['close_date'], reverse=True)

        # sorting from the least recent date to most recent date
        else:
            grant_list = sorted(grant_list, key=lambda date: date['close_date'])
        # order.append(col)
        i += 1
    # if order:
    #     grant_list = sorted(grant_list, key=lambda date: date['close_date'], reverse=True)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    # print(start)
    # print(length + start)
    items = grant_list[start:length + start]

    # response
    return {
        'data': [item for item in items],
        # Todo: change recordsFiltered and recordsTotal
        'recordsFiltered': total_filtered,
        'recordsTotal': total_filtered,
        'draw': request.args.get('draw', type=int),
    }


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

if __name__ == '__main__':
    app.run(debug=True)
