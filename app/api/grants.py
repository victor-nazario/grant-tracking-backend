from flask import Blueprint, jsonify
from app.scheduled.layers import models
from app.session_generator.create_session import get_session
from app.scheduled.layers.models import GrantEntrySchema
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin

grants_bp = Blueprint('api', __name__)
grant_schema = GrantEntrySchema()

spec = APISpec(
    title='Grant-Tracking-Platform-Swagger-Documentation',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)


@grants_bp.route('/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())


@grants_bp.route('/grants', methods=['GET'])
def available_grants():
    db_session = get_session()
    with db_session as session:
        query_result = session.query(models.GrantEntry).all()
        grant_list = []

    for grant in query_result:
        grant_list.append(grant_schema.dump(grant))

    return jsonify(grant_list)



