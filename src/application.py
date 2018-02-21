from flask import jsonify
from flask_migrate import Migrate
from src import app, db
from src.models import *
from src.model_mappings import *

migrate = Migrate(app, db)

@app.route('/fetch_pay_ranges')
def fetch_pay_ranges():
    pay_ranges = PayRange.query.all()
    schema = PayRangeSchema()
    result = [schema.dump(pay_range).data for pay_range in pay_ranges]
    return jsonify(result)

@app.route('/fetch_perks')
def fetch_perk():
    perks = Perk.query.all()
    schema = PerkSchema()
    result = [schema.dump(perk).data for perk in perks]
    return jsonify(result)

@app.route('/fetch_employment_types')
def fetch_employment_type():
    employment_types = EmploymentType.query.all()
    schema = EmploymentTypeSchema()
    result = [schema.dump(employment_type).data for employment_type in employment_types]
    return jsonify(result)

@app.route('/fetch_roles')
def fetch_roles():
    roles = Role.query.all()
    schema = RoleSchema()
    result = [schema.dump(role).data for role in roles]
    return jsonify(result)

@app.route('/fetch_educations')
def fetch_educations():
    educations = Education.query.all()
    schema = EducationSchema()
    result = [schema.dump(education).data for education in educations]
    return jsonify(result)

@app.route('/fetch_techs')
def fetch_techs():
    techs = Tech.query.all()
    schema = TechSchema()
    result = [schema.dump(tech).data for tech in techs]
    return jsonify(result)