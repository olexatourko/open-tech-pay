from flask import render_template, jsonify, request, url_for
from flask_migrate import Migrate
from sqlalchemy import and_, asc
from marshmallow import ValidationError, EXCLUDE
from src import app, db
from src.model_schemas import *
from src.request_schemas import *
import src.high_level_methods as hlm
import datetime
import json
import click

migrate = Migrate(app, db)

'''
Contains all endpoints and CLI commands
'''

@app.route('/')
def index():
    preview_submissions = Submission.query.filter(Submission.confirmed)\
        .order_by(Submission.created_at.desc())\
        .limit(app.config['MARKET_DATA_MIN_DISPLAY'])\
        .all()
    aggregate_data = hlm.get_aggregate_data()

    schema = SubmissionSchema(only={
        'salary',
        'employment_type',
        'perks',
        'roles',
        'education',
        'location',
        'techs',
        'years_experience',
        'years_with_current_employer',
        'number_of_employers',
        'verified',
        'created_at'
    })
    preview_submissions = [schema.dump(submission) for submission in preview_submissions]

    return render_template('app.html',
                           preview_submissions=preview_submissions,
                           aggregate_data=aggregate_data,
                           asset_date=(datetime.datetime.today() - datetime.timedelta(hours=1)).strftime('%Y-%m-%d'))

@app.route('/fetch_fields')
def fetch_fields():
    perks = Perk.query.filter(Perk.listed).all()
    employment_types = EmploymentType.query.all()
    locations = Location.query.all()
    roles = Role.query.filter(Role.listed).order_by(Role.name).all()
    educations = Education.query.order_by().all()
    techs = Tech.query.filter(Tech.listed).order_by(Tech.name).all()

    return jsonify({
        'perks': [PerkSchema(exclude=['listed']).dump(model) for model in perks],
        'employment_types': [EmploymentTypeSchema().dump(model) for model in employment_types],
        'locations': [LocationSchema().dump(model) for model in locations],
        'roles': [RoleSchema(exclude=['listed']).dump(model) for model in roles],
        'educations': [EducationSchema().dump(model) for model in educations],
        'techs': [TechSchema(exclude=['listed']).dump(model) for model in techs],
    })


@app.route('/fetch_submissions')
def fetch_submissions():
    submissions = Submission.query.filter(Submission.confirmed).order_by(Submission.created_at.desc()).all()
    schema = SubmissionSchema(only={
        'salary',
        'employment_type',
        'submission_to_perks',
        'roles',
        'education',
        'location',
        'techs',
        'years_experience',
        'years_with_current_employer',
        'number_of_employers',
        'verified',
        'created_at'
    })
    result = [schema.dump(submission) for submission in submissions]
    return jsonify(result)


@app.route('/check_email')
def check_email():
    try:
        request_schema = CheckEmailRequestSchema().load(request.args)
    except ValidationError as err:
        return jsonify({
            'status': 'error'
        })

    result = {
        'in_use': hlm.is_email_recently_used(request_schema['email']),
        'whitelisted': hlm.is_email_whitelisted(request_schema['email'])
    }

    result.pop('in_use', None) # Otherwise, it would be very easy to check if an employee/coworker has submitted.
    result['status'] = 'ok'
    return jsonify(result)


@app.route('/submit')
def submit():
    return render_template('submit.html', title='Submit')


@app.route('/submit', methods=['POST'])
def submit_post():
    payload = json.loads(request.form['payload'])

    """ Perform basic validation on the request params """
    try:
        request_schema = SubmissionRequestSchema().load(payload)
    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'errors': err.messages
        })

    """ Overwriting existing unconfirmed submission, otherwise create a new one """
    submission = Submission.query.filter(
        and_(
            Submission.email == payload['email'],
            Submission.confirmed == False
        )
    ).first()

    if submission:
        db.session.delete(submission)

    submission = SubmissionSchema(only=(
        'salary',
        'email',
        'years_experience',
        'years_with_current_employer',
        'number_of_employers'
    )).load(request_schema, unknown=EXCLUDE)

    """ Load EmploymentType, Education, Location """
    employment_type = EmploymentType.query.filter(EmploymentType.id == payload['employment_type']).first()
    education = Education.query.filter(Education.id == payload['education']).first()
    location = Location.query.filter(Location.id == payload['location']).first()

    submission.perks = []
    submission.roles = []
    submission.techs = []

    """ Get Perk models """
    for perk_dict in payload['perks']:
        if 'id' in perk_dict:
            perk = Perk.query.filter(Perk.id == perk_dict['id']).first()

        elif 'name' in perk_dict:
            perk = Perk.query.filter(Perk.name == perk_dict['name']).first()
            if not perk:
                try:
                    perk_schema = PerkSchema(only=['name']).load(perk_dict)
                except ValidationError as err:
                    return jsonify({
                        'status': 'error',
                        'errors': err.messages
                    })
                perk = perk_schema

        if perk:
            if 'value' in perk_dict:
                # Add perk with value
                submission.submission_to_perks.append(SubmissionToPerk(perk, value=perk_dict['value']))

            else:
                # Add perk without value
                submission.perks.append(perk)

    """ Get Role models """
    for role_dict in payload['roles']:
        if 'id' in role_dict:
            role = Role.query.filter(Role.id == role_dict['id']).first()

        elif 'name' in role_dict:
            role = Role.query.filter(Role.name == role_dict['name']).first()
            if not role:
                try:
                    role_schema = RoleSchema(only=['name']).load(role_dict)
                except ValidationError as err:
                    return jsonify({
                        'status': 'error',
                        'errors': err.messages
                    })
                role = role_schema

        if role:
            submission.roles.append(role)

    """ Get Tech models """
    for tech_dict in payload['techs']:
        if 'id' in tech_dict:
            tech = Tech.query.filter(Tech.id == tech_dict['id']).first()

        elif 'name' in tech_dict:
            tech = Tech.query.filter(Tech.name == tech_dict['name']).first()
            if not tech:
                try:
                    tech_schema = TechSchema(only=['name']).load(tech_dict)
                except ValidationError as err:
                    return jsonify({
                        'status': 'error',
                        'errors': err.messages
                    })
                tech = tech_schema

        if tech:
            submission.techs.append(tech)

    if len(submission.roles) == 0:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'errors': ['No roles selected']
        })

    submission.employment_type = employment_type
    submission.education = education
    submission.location = location
    submission.confirmed = False
    submission.confirmation_code = hlm.get_confirmation_code()
    submission.verified = hlm.is_email_whitelisted(request_schema['email'])

    db.session.add(submission)
    db.session.commit()

    """ Send confirmation email """
    if app.config['MAILJET_API_KEY'] and app.config['MAILJET_API_SECRET']:
        from mailjet_rest import Client
        mailjet = Client(auth=(app.config['MAILJET_API_KEY'], app.config['MAILJET_API_SECRET']))
        data = {
            'FromEmail': 'noreply@londontechpay.ca',
            'FromName': app.config['DEPLOYMENT_NAME'],
            'Subject': 'Confirm your submission',
            'Text-part': 'Thank you for your submission! To confirm your submission, please follow this link:\n\n {}\n\n' \
                   ''.format(url_for('confirm', _external=True, code=submission.confirmation_code)),
            'Recipients': [{'Email': submission.email}]
        }
        result = mailjet.send.create(data=data)
        if result.status_code != 200:
            return jsonify({
                'status': 'error',
                'errors': 'Error sending email, please try again later.'
            })

    return jsonify({
        'status': 'ok'
    })


@app.route('/confirm')
def confirm():
    """
    This is split up into a GET and POST route because some email virus scanners will
    inspect the link, triggering a confirmation before the user opens the email.
    To fix this, the GET confirm route uses an AJAX call to the POST confirm route to confirm.
    """
    code = 'undefined'
    try:
        request_schema = ConfirmRequestSchema().load(request.args)
        code = request_schema['code']
    except ValidationError as err:
        pass

    return render_template('confirm.html', code=code)

@app.route('/confirm', methods=['POST'])
def confirm_post():
    try:
        request_schema = ConfirmRequestSchema().load(request.form)
    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'error': err.messages
        })

    return jsonify({
        'status': 'ok',
        'succeeded': hlm.confirm_submission(request_schema['code']) is not None
    })


@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy-policy.html', title='Privacy Policy')

@app.route('/resources')
def resources():
    employers = Employer.query.distinct(Employer.name).order_by(asc(Employer.name)).all()
    return render_template('resources.html', title='Resources', employers=employers)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

"""
Custom CLI Commands
"""
@app.cli.command()
def list_submissions():
    submissions = Submission.query.all()
    for submission in submissions:
        click.echo(submission)


@app.cli.command()
@click.argument('email')
def remove_submission(email):
    submission = Submission.query.filter(Submission.email == email).first()
    if submission:
        click.echo('Submission found and deleted')
        db.session.delete(submission)
        db.session.commit()
    else:
        click.echo('Submission not found')
