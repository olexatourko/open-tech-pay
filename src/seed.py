import os, sys
sys.path.insert(0, os.getcwd()) # This makes the app, db import work
from sqlalchemy import exc
from src import app, db
from src.models import *

def seed_db(database):
    try:
        pay_ranges = [PayRange(lower=i, upper=i + 4999.99) for i in range(0, 145000 + 1, 5000)]
        perks = [
            Perk('Yearly Bonus', listed=True),
            Perk('Quarterly Bonuses', description='Use the total value paid out per year', listed=True),
            Perk('RRSP Matching / Profit Sharing', description='Use the value when the benefit is maxxed out', listed=True),
            Perk('Professional Development Expense Reimbursement', listed=True),
            Perk('Fitness Expense Reimbursement', listed=True),
            Perk('Food / Drinks', listed=True),
            Perk('Employee Discount Program', listed=True),
            Perk('Transit Pass', listed=False)
        ]
        employment_types = [
            EmploymentType('Full-Time'),
            EmploymentType('Part-Time'),
            EmploymentType('Independent Contractor'),
            EmploymentType('Paid Internship'),
            EmploymentType('Unpaid Internship')
        ]
        roles = [
            Role('Software Developer', listed=True),
            Role('Web: Backend', listed=True),
            Role('Web: Frontend', listed=True),
            Role('Web: Full-Stack', listed=True),
            Role('Web: Design', listed=True),
            Role('Graphic Designer', listed=True),
            Role('System Administrator', listed=True),
            Role('DevOps', listed=True),
            Role('Embedded Software Developer', listed=True),
            Role('Hardware Developer', listed=True),
            Role('Project Manager', listed=True),
            Role('Mobile Developer', listed=False),
        ]
        educations = [
            Education('Some Secondary School'),
            Education('Completed Secondary School'),
            Education('Some College / University'),
            Education('Completed Associate\'s Degree'),
            Education('Completed Bachelor\'s Degree'),
            Education('Completed Master\'s / Graduate Degree'),
            Education('Completed Doctorate Degree')
        ]
        techs = [
            Tech('Python', listed=True),
            Tech('PHP', listed=True),
            Tech('Ruby', listed=True),
            Tech('Java', listed=True),
            Tech('C', listed=True),
            Tech('C++', listed=True),
            Tech('C#', listed=True),
            Tech('Javascript', listed=True),
            Tech('SQL', listed=True),
            Tech('HTML', listed=True),
            Tech('CSS', listed=True),
            Tech('Bash / Shell', listed=True),
            Tech('Linux', listed=True),
            Tech('Golang', listed=True),
            Tech('Git', listed=True),
            Tech('Perforce', listed=True),
            Tech('Laravel', listed=False),
            Tech('Spring', listed=False),
            Tech('Rails', listed=False)
        ]
        for v in pay_ranges: db.session.add(v)
        for v in perks: db.session.add(v)
        for v in employment_types: db.session.add(v)
        for v in roles: db.session.add(v)
        for v in educations: db.session.add(v)
        for v in techs: db.session.add(v)
        database.session.commit()

        from random import randint
        for i in range(0, 10):
            submission = Submission()
            submission.years_experience = randint(0, 15)
            submission.years_with_current_employer = randint(0, 5)
            submission.number_of_employers = randint(1, 3)
            submission.pay_range = pay_ranges[randint(6, 16)]
            db.session.add(submission)

            for j in range(0, 3):
                submission.associate_perk(perks[randint(0, len(perks) - 1)])
                # submission.append(perks[randint(0, len(perks) - 1)])

            submission.employment_type = employment_types[randint(0, len(employment_types) - 1)]
            for j in range(0, 2):
                submission.associate_role(roles[randint(0, len(roles) - 1)])

            for j in range(0, 5):
                submission.associate_tech(techs[randint(0, len(techs) - 1)])

            submission.education = educations[randint(0, len(educations) - 1)]

        database.session.commit()

    except exc.SQLAlchemyError:
        import traceback
        print(traceback.format_exc())
        database.session.rollback()

if __name__ == '__main__':
    seed_db(db)