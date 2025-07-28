from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'  # You should create this file with your OpenAPI spec

swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Plastic Surgery EMR API"
    }
)

bp = Blueprint('swagger', __name__)
bp.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)
from flask import Blueprint, jsonify

bp = Blueprint('swagger', __name__, url_prefix='/api/docs')

@bp.route('/', methods=['GET'])
def docs():
    return jsonify({
        'info': {
            'title': 'BPRS UNTH EMR API',
            'version': '1.0',
            'description': 'API documentation for the BPRS UNTH EMR system.'
        },
        'paths': {
            '/api/auth/login': {'post': {'summary': 'User login'}},
            '/api/auth/register': {'post': {'summary': 'User registration'}},
            '/api/patients/': {'get': {'summary': 'List patients'}, 'post': {'summary': 'Create patient'}},
            '/api/patients/{id}': {'get': {'summary': 'Get patient'}, 'put': {'summary': 'Update patient'}, 'delete': {'summary': 'Delete patient'}},
            '/api/clinical/evaluations': {'post': {'summary': 'Create clinical evaluation'}},
            '/api/clinical/evaluations/{id}': {'get': {'summary': 'Get clinical evaluation'}},
            '/api/clinical/diagnoses': {'post': {'summary': 'Create diagnosis'}},
            '/api/clinical/diagnoses/{id}': {'get': {'summary': 'Get diagnosis'}},
            '/api/clinical/treatmentplans': {'post': {'summary': 'Create treatment plan'}},
            '/api/clinical/treatmentplans/{id}': {'get': {'summary': 'Get treatment plan'}},
            '/api/clinical/labinvestigations': {'post': {'summary': 'Create lab investigation'}},
            '/api/clinical/labinvestigations/{id}': {'get': {'summary': 'Get lab investigation'}},
            '/api/clinical/imaginginvestigations': {'post': {'summary': 'Create imaging investigation'}},
            '/api/clinical/imaginginvestigations/{id}': {'get': {'summary': 'Get imaging investigation'}},
            '/api/clinical/woundcareplans': {'post': {'summary': 'Create wound care plan'}},
            '/api/clinical/woundcareplans/{id}': {'get': {'summary': 'Get wound care plan'}},
            '/api/clinical/surgerybookings': {'post': {'summary': 'Create surgery booking'}},
            '/api/clinical/surgerybookings/{id}': {'get': {'summary': 'Get surgery booking'}},
            '/api/clinical/appointments': {'post': {'summary': 'Create appointment'}},
            '/api/clinical/appointments/{id}': {'get': {'summary': 'Get appointment'}},
            '/api/notifications/': {'get': {'summary': 'List notifications'}},
            '/api/notifications/{id}/read': {'post': {'summary': 'Mark notification as read'}},
            '/api/assessments/': {'get': {'summary': 'List assessments'}},
            '/api/assessments/cbt': {'get': {'summary': 'Get CBT questions'}},
            '/api/assessments/score': {'post': {'summary': 'Submit assessment score'}},
        }
    })
