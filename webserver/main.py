# --- import required libraries and modules:
from flask import Flask, render_template, make_response

from modules.database.engine import session
from modules.database.models import Reading

import pandas as pd


# --- Instantiate a new flask app (which will be called main):
app = Flask(__name__)


# --- Define the routes that the server will have:
@app.route("/")
def home() -> render_template:
    # --- Get the last 10 readings:
    results = session.query(Reading).order_by(Reading.id.desc()).limit(10)
    
    return render_template(template_name_or_list = "index.html", 
                           readings = results)
    

@app.route("/download-all")
def download_all() -> make_response:
    query = session.query(Reading)
    
    df = pd.read_sql_query(sql = session.query(Reading).statement,
        #sql = query.statement, # This is SELECT * FROM readings;
                           con = session.bind, 
                           index_col="id")
    
    response = make_response(df.to_csv())
    response.headers["Content-Disposition"] = "attachment; filename=all-data.csv"
    response.headers["Content-Type"] = "text/csv"
    
    return response