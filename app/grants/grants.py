from flask import Blueprint, jsonify
from app.scheduled import models
from app.session_generator.create_session import get_session

grants_bp = Blueprint('grants', __name__)


@grants_bp.route('/grants', methods=['GET'])
def available_grants():
    db_session = get_session()
    with db_session as session:
        query_result = session.query(models.GrantEntry).all()
        grant_list = []
    for grant in query_result:
        grant_dict = grant.__dict__
        to_be_deleted = ('_sa_instance_state', 'etag', 'id', 'content')
        for k in to_be_deleted:
            grant_dict.pop(k, None)
        grant_list.append(grant_dict)
    return jsonify(grant_list)


