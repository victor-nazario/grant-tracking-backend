import datetime

from flask import Blueprint

grants_bp = Blueprint('grants', __name__)


@grants_bp.route('/grants', methods=['GET'])
def available_grants():
    return 'Some grant info...'


