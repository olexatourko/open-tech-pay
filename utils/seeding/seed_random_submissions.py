import os, sys
from sqlalchemy import exc
from src import app, db
from src.models import *

def seed_random_submisssions(database, n=10):
    employment_types = EmploymentType.query.all()
    locations = Location.query.all()
    roles = Role.query.all()
    perks = Perk.query.all()
    techs = Tech.query.all()
    educations = Education.query.all()

    try:
        from random import randint
        for i in range(0, n):
            submission = Submission()
            submission.salary = randint(25, 100) * 1000
            submission.email = 'submission_{}@company1.com'.format(i)
            submission.confirmed = True
            submission.years_experience = randint(0, 15)
            submission.years_with_current_employer = randint(0, 5)
            submission.number_of_employers = randint(1, 3)
            db.session.add(submission)

            for j in range(0, 3):
                perk = perks[randint(0, len(perks) - 1)]
                if perk not in submission.perks:
                    value = randint(1, 50) * 100
                    submission.submission_to_perks.append(SubmissionToPerk(perk, value))


            submission.employment_type = employment_types[randint(0, len(employment_types) - 1)]
            submission.location = locations[randint(0, len(locations) - 1)]
            for j in range(0, 2):
                submission.associate_role(roles[randint(0, len(roles) - 1)])

            for j in range(0, 5):
                submission.associate_tech(techs[randint(0, len(techs) - 1)])

            submission.education = educations[randint(0, len(educations) - 1)]
            db.session.commit()


    except exc.SQLAlchemyError:
        import traceback
        print(traceback.format_exc())
        database.session.rollback()

if __name__ == '__main__':
    seed_random_submisssions(db)