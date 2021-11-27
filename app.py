from matplotlib import style
style.use('fivethirtyeight')

import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template
from sqlalchemy import (Column, Float, Integer, MetaData, String, Table,
                        create_engine, func)
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from password import password

#################################################
# Database Setup
connect_str = f"postgres:{password}@localhost:5432/Formula1" 
engine = create_engine(f"postgresql://{connect_str}")

# check if we can connect
# result = engine.execute("select * from f1")
# for r in result:
#     print(r)


def init():

    # we can then produce a set of mappings from this MetaData.
    Base = automap_base()

    # calling prepare() just sets up mapped classes and relationships.
    Base.prepare(engine, reflect=True)
    Formulat1Data = Base.classes.f1
    return Formulat1Data
    

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route('/')
def db_ping():
    init()
    df = pd.read_sql_table('f1', engine)

    df.reset_index(inplace=True)
    year = df['year']
    years = list(set(year))
    years.sort()

    return render_template('index.html', yearlist=years)



# calling this function when changing the state
# @app.route('/<year>')
# def calc_metadata(year):
#     Formulat1Data = init()
#     session = Session(engine)

#     points = session.execute("SELECT points from f1").fetchall()
#     names = session.execute("SELECT name form f1").fetchall()
#     # # if year == 2019:
#     # temps = session.query(func.sum(Formulat1Data.points)).\
#     #     filter(Formulat1Data.year == year).all()
#     # temps = list(np.ravel(temps))
#     # session.close()
#     # print(temps)
#     # # names = "${:,.0f}".format(temps[0])
#     # points = "${:,.0f}".format(temps[1])
#     # # avg = "${:,.0f}".format(temps[2])
#     temp_dict = {"Names": names, "Points": points}
#     # #display(temp_dict)
#     return jsonify(temp_dict)


# calling this function to show all data per year
@app.route('/data/<year>')
def get_data(year):
    # HouseData = init()
    session = Session(engine)
    data = session.execute("SELECT * from f1").fetchall()
    # take all the rows that contain this state
    names_list = []
    points_list = []
    year = int(year)
    for i in data:
        print(i[2])
        if i[1] == year:
            print('---------- IT IS-------------- ')
            names_list.append(i[2])
            points_list.append(float(i[5]))

    temp_dict = { 
                 "year": [year],
                 "names": names_list,
                 "points": points_list
                 }
    # ret_data = [list(x) for x in names_list]
    session.close()
    print(temp_dict)
    return temp_dict
    #return jsonify(temp_dict)

if __name__ == '__main__':
    app.run(debug=True)
    # calc_metadata(2010)
    get_data(2010)