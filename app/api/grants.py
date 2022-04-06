from flask import Blueprint, jsonify
from app.scheduled.layers import models
from app.session_generator.create_session import get_session
from app.scheduled.layers.models import GrantEntrySchema

grants_bp = Blueprint('api', __name__)
grant_schema = GrantEntrySchema()


@grants_bp.route('/grants', methods=['GET'])
def available_grants():
    db_session = get_session()
    with db_session as session:
        query_result = session.query(models.GrantEntry).all()
        grant_list = []

    for grant in query_result:
        grant_list.append(grant_schema.dump(grant))

    return jsonify(grant_list)

