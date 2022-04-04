from flask import Blueprint
from app.session_generator.create_session import get_session

grants_bp = Blueprint('grants', __name__)


@grants_bp.route('/grants', methods=['GET'])
def available_grants():
    return 'Some grant info...'


