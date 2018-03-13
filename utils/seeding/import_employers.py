import os, sys
from sqlalchemy import exc
from src import app, db
from src.models import Employer
import argparse
import json

def import_employers(employers_dict):
    for employer in employers_dict:
        employer_model = Employer.query.filter(Employer.name == employer['name']).first()
        if not employer_model:
            employer_model = Employer(employer['name'], employer['email_domain'], employer['url'])

        else:
            employer_model.name = employer['name']
            employer_model.email_domain = employer['email_domain']
            employer_model.url = employer['url']

        db.session.add(employer_model)

    db.session.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Imports a JSON-encoded list of emlpoyers into the database.')
    parser.add_argument('json_file', metavar='F', help='The JSON file.')
    args = parser.parse_args()

    with open(args.json_file, 'r') as json_data:
        import_employers(json.load(json_data))