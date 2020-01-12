import os, sys
from sqlalchemy import exc
from src import app, db
from src.models import *
import datetime

def seed_preset_submisssions(database):
    employment_types = EmploymentType.query.all()
    locations = Location.query.all()
    roles = Role.query.all()
    perks = Perk.query.all()
    techs = Tech.query.all()
    educations = Education.query.all()

    try:
        ''' Seed 1 '''
        submission = Submission()
        submission.salary = 50000
        submission.email = 'submission_1@company1.com'
        submission.confirmed = True
        submission.years_experience = 3
        submission.years_with_current_employer = 3
        submission.number_of_employers = 1
        db.session.add(submission)
        submission.employment_type = employment_types[0]
        submission.location = locations[0]
        submission.associate_perk(perks[0])
        submission.associate_role(roles[0])
        submission.associate_tech(techs[0])
        submission.education = educations[0]
        submission.created_at = datetime.date(2017, 1, 1)

        ''' Seed 2 '''
        submission = Submission()
        submission.salary = 40000
        submission.email = 'submission_2@company1.com'
        submission.confirmed = True
        submission.years_experience = 3
        submission.years_with_current_employer = 3
        submission.number_of_employers = 1
        db.session.add(submission)
        submission.employment_type = employment_types[0]
        submission.location = locations[0]
        submission.associate_perk(perks[0])
        submission.associate_role(roles[0])
        submission.associate_tech(techs[0])
        submission.education = educations[0]
        submission.created_at = datetime.date(2017, 1, 1)

        ''' Seed 3 '''
        submission = Submission()
        submission.salary = 60000
        submission.email = 'submission_3@unlisted.com'
        submission.confirmed = True
        submission.years_experience = 3
        submission.years_with_current_employer = 3
        submission.number_of_employers = 1
        db.session.add(submission)
        submission.employment_type = employment_types[0]
        submission.location = locations[0]
        submission.associate_perk(perks[0])
        submission.associate_role(roles[0])
        submission.associate_tech(techs[0])
        submission.education = educations[0]
        submission.created_at = datetime.date(2017, 1, 1)

        db.session.commit()


    except exc.SQLAlchemyError:
        import traceback
        print(traceback.format_exc())
        database.session.rollback()

if __name__ == '__main__':
    seed_preset_submisssions(db)