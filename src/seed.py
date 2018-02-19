import os, sys
sys.path.insert(0, os.getcwd()) # This makes the app, db import work
from sqlalchemy import exc
from src import app, db
from src.models import PayRange, Perk, EmploymentType, Role, Education, Tech

def seed_db(database):
    try:
        # Add pay ranges
        for i in range(0, 145000 + 1, 5000):
            database.session.add(PayRange(lower=i, upper=i + 4999.99))

        # Add perks
        database.session.add(Perk('Yearly Bonus', listed=True))
        database.session.add(Perk('Quarterly Bonuses', description='Use the total value paid out per year', listed=True))
        database.session.add(Perk('RRSP Matching / Profit Sharing', description='Use the value when the benefit is maxxed out', listed=True))
        database.session.add(Perk('Professional Development Expense Reimbursement', listed=True))
        database.session.add(Perk('Fitness Expense Reimbursement', listed=True))
        database.session.add(Perk('Food / Drinks', listed=True))
        database.session.add(Perk('Employee Discount Program', listed=True))

        # Add employment type
        database.session.add(EmploymentType('Full-Time', listed=True))
        database.session.add(EmploymentType('Part-Time', listed=True))
        database.session.add(EmploymentType('Independent Contractor', listed=True))

        # Add roles
        database.session.add(Role('Software Developer', listed=True))
        database.session.add(Role('Web: Backend', listed=True))
        database.session.add(Role('Web: Frontend', listed=True))
        database.session.add(Role('Web: Full-Stack', listed=True))
        database.session.add(Role('Web: Design', listed=True))
        database.session.add(Role('Graphic Designer', listed=True))
        database.session.add(Role('System Administrator', listed=True))
        database.session.add(Role('DevOps', listed=True))
        database.session.add(Role('Embedded Software Developer', listed=True))
        database.session.add(Role('Hardware Developer', listed=True))

        # Add education
        database.session.add(Education('Some Secondary School'))
        database.session.add(Education('Completed Secondary School'))
        database.session.add(Education('Some College / University'))
        database.session.add(Education('Completed Associate\'s Degree'))
        database.session.add(Education('Completed Bachelor\'s Degree'))
        database.session.add(Education('Completed Master\'s / Graduate Degree'))
        database.session.add(Education('Completed Doctorate Degree'))

        # Add tech
        database.session.add(Tech('Python', listed=True))
        database.session.add(Tech('PHP', listed=True))
        database.session.add(Tech('Ruby', listed=True))
        database.session.add(Tech('Java', listed=True))
        database.session.add(Tech('C', listed=True))
        database.session.add(Tech('C++', listed=True))
        database.session.add(Tech('C#', listed=True))
        database.session.add(Tech('Javascript', listed=True))
        database.session.add(Tech('SQL', listed=True))
        database.session.add(Tech('HTML', listed=True))
        database.session.add(Tech('CSS', listed=True))
        database.session.add(Tech('Bash / Shell', listed=True))
        database.session.add(Tech('Linux', listed=True))
        database.session.add(Tech('GoLang', listed=True))
        database.session.add(Tech('Git', listed=True))
        database.session.add(Tech('Perforce', listed=True))

        database.sesssion.commit()

    except exc.SQLAlchemyError:
        database.session.rollback()

if __name__ == '__main__':
    seed_db(db)