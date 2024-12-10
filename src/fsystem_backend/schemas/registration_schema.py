from flask import Blueprint, request, jsonify
from fsystem_backend.database import db
from datetime import datetime
from fsystem_backend.model import RegisteredObject
from http import HTTPStatus
from marshmallow import Schema, fields, validate, ValidationError

# Schema definition
class RegistrationSchema(Schema):
    """Schema for validating registration request"""
    registered_objectno = fields.Str(
        required=True, 
        validate=validate.Length(equal=6, error="Must be exactly 6 digits"),
        error_messages={"required": "registered_objectno is required"}
    )
    registered_objectnam = fields.Str(
        required=True,
        validate=validate.Length(max=6, error="Must not exceed 6 characters"),
        error_messages={"required": "registered_objectnam is required"}
    )
    object_full_name = fields.Str(validate=validate.Length(max=30))
    object_eng_full_name = fields.Str(validate=validate.Length(max=30))
    object_typeno = fields.Str(validate=validate.Length(max=6))
    unit_currencyno = fields.Str(validate=validate.Length(max=6))
    in_cityno = fields.Str(validate=validate.Length(max=6))
    applicant = fields.Integer()
    want_login_date = fields.Date()
    administratora_nam = fields.Str(validate=validate.Length(max=20))
    administratora_mobile = fields.Str(validate=validate.Length(max=16))