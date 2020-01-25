from matplotlib import pyplot as plt, ticker
from matplotlib import rcParams
from src import db # Configures the db (look at src/_init_.py)
from src.models import Submission, Location, SubmissionToLocation
import datetime
import pandas

if __name__ == '__main__':
    q= db.session.query(Submission.id, Submission.salary, Submission.years_experience, Location.name)\
        .join(SubmissionToLocation, SubmissionToLocation.submission_id == Submission.id)\
        .join(Location, SubmissionToLocation.location_id == Location.id)\
        .filter(Submission.confirmed == True)

    raw_query = str(q.statement.compile(compile_kwargs={"literal_binds": True})) # https://docs.sqlalchemy.org/en/13/faq/sqlexpressions.html
    dataframe = pandas.read_sql_query(raw_query, db.engine)
    local_dataframe = dataframe.where(dataframe.name.isin(('London, Ontario', 'Near London, Ontario')))
    remote_dataframe = dataframe.where(dataframe.name.isin(('Remote Work', )))

    rcParams['font.family'] = 'monospace'
    fig, ax = plt.subplots()
    ax.set(xlabel='Years Experience', ylabel='Base Salary', title='Generated {}'.format(datetime.datetime.today().strftime('%Y-%m-%d %H:%M')))
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax.xaxis.set_ticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, min(20, dataframe['years_experience'].max())])

    ax.plot(local_dataframe['years_experience'], local_dataframe['salary'], color='#27b1d4', marker='o', linestyle='none', label='Working in or near London, Ontario')
    ax.plot(remote_dataframe['years_experience'], remote_dataframe['salary'], color='#f0822d', marker='o', linestyle='none', label='Working remotely')
    ax.legend() # Auto-configures based on .plot() labels
    plt.tight_layout() # Makes sure it all fits into the figure (ylabel was being cut off)
    plt.savefig('./src/static/graphs/basic_salary_to_exp_graph.png')
    # plt.show()
