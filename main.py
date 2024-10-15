from flask import Flask,url_for
from backend.models import *

#app=None
'''
def init_appr():
    household_app=Flask(__name__, template_folder='../templates') #object of flask
    household_app.debug=True
    household_app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///household.sqlite3"
    #household_app.app_context().push() #Direct access app by other modules (db, authentication)
    db.init_app(household_app) #object.method(<parameter>
    household_app.app_context().push()
    print("Household app started...")
    return household_app

app=init_appr()
'''
app=Flask(__name__, template_folder='../templates')
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///household.sqlite3"
db.init_app(app) #object.method(<parameter>
app.app_context().push()

from backend.controllers import *


if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)



