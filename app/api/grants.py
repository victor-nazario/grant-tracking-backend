from flask import Blueprint, jsonify, request
from flask_sqlalchemy import Pagination

from app.scheduled.layers import models
from app.session_generator.create_session import get_session
from app.scheduled.layers.models import GrantEntrySchema

grants_bp = Blueprint('api', __name__)
grant_schema = GrantEntrySchema()

ROWS_PER_PAGE = 5


# export FLASK_APP=__init__.py
# FLASK_DEBUG=1
# flask run
# http://127.0.0.1:5000/api/grants?page=1
@grants_bp.route('/grants', methods=['GET'])
def available_grants():
    db_session = get_session()
    page = request.args.get("page", 1, type=int)
    with db_session as session:
        query_result = session.query(models.GrantEntry).all()
        grant_list = []

    for grant in query_result:
        grant_list.append(grant_schema.dump(grant))

    start = (page - 1) * ROWS_PER_PAGE
    print(start + 1)
    end = start + ROWS_PER_PAGE
    print(end)
    items = grant_list[start:end]
    grants_paginate = Pagination(query=None, page=None, per_page=None,
                                 total=len(items),
                                 items=items)
    # total_pages = float(len(grant_list) / ROWS_PER_PAGE)
    # if page == ceil(total_pages) + 1:
    #     print("ERROR" + str(page))
    return jsonify(grants_paginate.items)

