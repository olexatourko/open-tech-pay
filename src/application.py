from flask import render_template, jsonify, request
from flask_migrate import Migrate
from src import app, db
from src.models import *
from src.model_mappings import *
import json

migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/fetch_pay_ranges')
def fetch_pay_ranges():
    pay_ranges = PayRange.query.all()
    schema = PayRangeSchema()
    result = [schema.dump(pay_range).data for pay_range in pay_ranges]
    return jsonify(result)

@app.route('/fetch_perks')
def fetch_perk():
    perks = Perk.query.filter(Perk.listed).all()
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
    roles = Role.query.filter(Role.listed).all()
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
    techs = Tech.query.filter(Tech.listed).all()
    schema = TechSchema()
    result = [schema.dump(tech).data for tech in techs]
    return jsonify(result)

@app.route('/fetch_submissions')
def fetch_submissions():
    submisions = Submission.query.all()
    schema = SubmissionSchema()
    result = [schema.dump(submission).data for submission in submisions]
    return jsonify(result)


@app.route('/submit', methods=['POST'])
def submit():
    print(request.form.keys())

    return jsonify({
        'status': 'ok'
    })