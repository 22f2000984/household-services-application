from flask import Flask,url_for,render_template
from backend.models import db

#app=None

def setup_app():
    #app=Flask(__name__)
    app=Flask(__name__, template_folder='../templates')
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///household.sqlite3"
    db.init_app(app) #object.method(<parameter>
    app.app_context().push()
    #app.debug=True
    print("Household application started")
    return app

app=setup_app()
from backend.controllers import *
#from backend.models import *


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)
    #app.run()



