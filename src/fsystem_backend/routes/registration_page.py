from flask_smorest import Blueprint
from flask import request, jsonify
from marshmallow import  ValidationError
from fsystem_backend.database import db
from fsystem_backend.model import RegisteredObject
from fsystem_backend.schemas.registration_schema import RegistrationSchema

from datetime import datetime
from http import HTTPStatus

# Create blueprint
registration_bp = Blueprint('registration', __name__, url_prefix='/api/registration')

@registration_bp.route('/', methods=['POST'])
def create_registration():
    """Create a new registered object"""
    try:
        data = request.get_json()
        
         # Validate schema
        schema = RegistrationSchema()
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation error',
                'errors': err.messages
            }), HTTPStatus.BAD_REQUEST

        # Validate required fields
        if not data.get('registered_objectno') or not data.get('registered_objectnam'):
            return jsonify({
                'success': False,
                'message': 'Missing required fields: registered_objectno and registered_objectnam'
            }), HTTPStatus.BAD_REQUEST
        
        # Check if object already exists
        existing_object = RegisteredObject.query.get(data['registered_objectno'])
        if existing_object:
            return jsonify({
                'success': False,
                'message': 'Registration object already exists'
            }), HTTPStatus.CONFLICT
        
        # Create new object
        new_object = RegisteredObject.from_dict(data)
        new_object.created_date = datetime.utcnow()
        new_object.last_update = datetime.utcnow()
        
        db.session.add(new_object)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Registration created successfully',
            'data': new_object.to_dict()
        }), HTTPStatus.CREATED
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating registration: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@registration_bp.route('/<registered_objectno>', methods=['GET'])
def get_registration(registered_objectno):
    """Get a registered object by its number"""
    try:
        reg_object = RegisteredObject.query.get_or_404(registered_objectno)
        return jsonify({
            'success': True,
            'data': reg_object.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving registration: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@registration_bp.route('/<registered_objectno>', methods=['PUT'])
def update_registration(registered_objectno):
    """Update an existing registered object"""
    try:
        reg_object = RegisteredObject.query.get_or_404(registered_objectno)
        data = request.get_json()
        
        # Update fields
        for key, value in data.items():
            if hasattr(reg_object, key):
                setattr(reg_object, key, value)
        
        reg_object.last_update = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Registration updated successfully',
            'data': reg_object.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating registration: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@registration_bp.route('/<registered_objectno>', methods=['DELETE'])
def delete_registration(registered_objectno):
    """Delete a registered object"""
    try:
        reg_object = RegisteredObject.query.get_or_404(registered_objectno)
        db.session.delete(reg_object)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Registration deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting registration: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@registration_bp.route('/list', methods=['GET'])
def list_registrations():
    """List all registered objects with optional filtering"""
    try:
        # Get query parameters for filtering
        status = request.args.get('status', type=int)
        object_type = request.args.get('object_typeno')
        
        query = RegisteredObject.query
        
        # Apply filters if provided
        if status is not None:
            query = query.filter_by(status=status)
        if object_type:
            query = query.filter_by(object_typeno=object_type)
            
        registrations = query.all()
        return jsonify({
            'success': True,
            'data': [reg.to_dict() for reg in registrations]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error listing registrations: {str(e)}'
        }), HTTPStatus.INTERNAL_SERVER_ERROR