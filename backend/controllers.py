from flask import Flask,render_template,request
from flask import current_app as app
from .models import *
#from app import app

app=Flask(__name__, template_folder='../templates')
@app.route('/')
def index():
    return render_template('index.html')
    #return "<h2> Welcome to our Page </h2>"

@app.route("/login",methods=['GET','POST'])
def user_login():
    if request.method=='POST':
        uname=request.form.get("user_email")
        pwd=request.form.get("user_password")
        usr=User_Info.query.filter_by(user_name=uname,pwd=pwd).first()
        if usr and usr.role==0:
            #return "<h2>Welcome</h2>"
            return render_template("admin_dashboard.html",name=usr.full_name)
        elif usr and usr.role==1:
            return render_template("customer_dashboard.html")
        else:
            return render_template('login.html',msg="Invalid Credentials")
    return render_template('login.html',msg="")

@app.route("/customersignup")
def customer_signup():
    if request.method=='POST':
        email=request.form.get("c_email")
        uname=request.form.get("c_fullname")
        fname=request.form.get("c_fullname")
        pwd=request.form.get("c_password")
        add=request.form.get("c_address")
        pin=request.form.get("c_pincode")
        usr=User_Info.query.filter_by(email=email).first()
        if not usr:
            new_user=User_Info(email=email,full_name=fname,user_name=uname,pwd=pwd,service_name="none",experience=0,add=add,pincode=pin,role=1)
            db.session.add(new_user)
            db.session.commit()
        if usr and usr.role==0:
            #return "<h2>Welcome</h2>"
            return render_template("admin_dashboard.html")
        elif usr and usr.rol==1:
            return render_template("customer_dashboard.html")
        else:
            return render_template('csignup.html',msg="Invalid Credentials")
    return render_template("csignup.html")

@app.route("/professionalsignup")
def serviceprofessional_signup():
    return render_template("sp_signup.html")


if __name__=='__main__':
    app.debug=True
    app.run()




