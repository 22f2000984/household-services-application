import os
from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
#import datetime

from datetime import date

app=Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join( current_dir, "database.sqlite3")
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///household.sqlite3"

db = SQLAlchemy(app)

#Define db classes
class User_Info(db.Model):
    __tablename__="user_info"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,nullable=False)
    full_name=db.Column(db.String,nullable=False)
    user_name=db.Column(db.String,unique=True,nullable=False)
    service_name=db.Column(db.String,nullable=False)
    experience=db.Column(db.Integer,nullable=False)
    pwd=db.Column(db.String,nullable=False)
    add=db.Column(db.String,nullable=True)
    pincode=db.Column(db.String,nullable=False)
    role=db.Column(db.Integer,nullable=False,default=1)
    status=db.Column(db.String,unique=True)
    location=db.Column(db.String,nullable=False)

class Service_Info(db.Model):
    __tablename__="service_info"
    id=db.Column(db.Integer,primary_key=True)
    servicename=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    baseprice=db.Column(db.Integer,nullable=False)
    time_required=db.Column(db.String,nullable=False)
    service_type=db.Column(db.String,nullable=False)
    
class Customer_Service_Request(db.Model):
    __tablename__="customer_service_request"
    id=db.Column(db.Integer,primary_key=True)
    service_id=db.Column(db.Integer,db.ForeignKey(Service_Info.id),nullable=False)
    customer_id=db.Column(db.Integer,db.ForeignKey(User_Info.id),nullable=False)
    professional_id=db.Column(db.Integer,db.ForeignKey(User_Info.id),nullable=False)
    date_of_request=db.Column(db.String,nullable=False)
    date_of_completion=db.Column(db.String,nullable=False)
    service_status=db.Column(db.String,nullable=False)
    remarks=db.Column(db.String)
    
    
    

'''-----------------------------Login and signup section-----------------------------------------'''

@app.route('/')
def index():
    return render_template('index.html')
    #return "<h2> Welcome to our Page </h2>"
    
#Route to login
@app.route("/login",methods=['GET','POST'])
def user_login():
    if request.method=='POST':
        uname=request.form.get("user_email")
        pwd=request.form.get("user_password")
        usr=User_Info.query.filter_by(email=uname,pwd=pwd).first()
        if usr and usr.status=="approved":
            if usr and usr.role==0:
                return redirect(url_for(".admin_dashboard",admin_name=usr.full_name))
            elif usr and usr.role==1:
                #return redirect("/customerdashboard",customer_name=usr.full_name)
                return redirect(url_for(".customer_dashboard",customer_name=usr.full_name,customer_id=usr.id))
            elif usr and usr.role==2:
                #return redirect("/customerdashboard",customer_name=usr.full_name)
                return redirect(url_for(".professional_dashboard",professional_name=usr.full_name))
            else:
                return render_template('login.html',msg='"Invalid credentials, try again"')
        elif usr and usr.status=="rejected":
            return render_template('login.html',msg="You can't login, admin rejected your account")
        elif usr and usr.status=="pending":
            return render_template('login.html',msg="Admin approval for your account is pending.")
        elif not usr:
            return render_template('login.html',msg='"Invalid credentials, try again"')
    return render_template('login.html',msg="")

# Route and function for cutomer signup 
@app.route("/customersignup", methods=['GET', 'POST'])
def customer_signup():
    usr=db.session.query(User_Info).with_entities(User_Info.location).filter().distinct().all()
    #usr=User_Info.query.all()
    #customerrequest=Customer_Service_Request.query.filter_by(customer_id=id).first()
    if request.method=='POST':
        email=request.form.get("c_email")
        pwd=request.form.get("c_password")
        fname=request.form.get("c_fullname")
        uname=request.form.get("c_email")
        add=request.form.get("c_address")
        pin=request.form.get("c_pincode")
        location=request.form.get("customer_location")
        usr=User_Info.query.filter_by(email=email).first()
        if not usr:
            new_user=User_Info(email=email,full_name=fname,user_name=uname,service_name="Customer",experience=0,pwd=pwd,add=add,pincode=pin,role=1,status="approved",location=location)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
            #render_template("/login.html",msg="Successfully account created")
        elif usr:
            return render_template('customer_signup.html',msg='"Customer exists"')
    return render_template("customer_signup.html",msg="",usr=usr)

# Route for service professional signup 
@app.route("/professionalsignup", methods=["GET","POST"])
def serviceprofessional_signup():
    #servname=Service_Info.query.all()
    pservicename=Service_Info.query.all()
    servname=db.session.query(User_Info).with_entities(User_Info.location).filter().distinct().all()
    #pservicename=db.session.query(Service_Info).with_entities(Service_Info.service_type).filter().distinct().all()
    if request.method=='POST':
        email=request.form.get("s_email")
        pwd=request.form.get("s_password")
        fname=request.form.get("s_fullname")
        uname=request.form.get("s_email")
        sname=request.form.get("ps_name")
        add=request.form.get("s_address")
        pin=request.form.get("s_pincode")
        sexp=request.form.get("s_exp")
        location=request.form.get("customer_location")
        usr=User_Info.query.filter_by(email=email).first()
        if not usr:
            new_professional=User_Info(email=email,full_name=fname,user_name=uname,service_name=sname,experience=sexp,pwd=pwd,add=add,pincode=pin,role=2,status="pending",location=location)
            db.session.add(new_professional)
            db.session.commit()
            return redirect("/login")
        elif usr:
            return render_template('professional_signup.html',msg='"Service Professional exists"',servicename=servname,pservicename=pservicename)
    return render_template("professional_signup.html",msg="",servicename=servname,pservicename=pservicename)


'''--------------------------Admin section---------------------------------------------------'''

#Route for admin dashboard
@app.route("/admindashboard")
def admin_dashboard():
    #name = request.args['admin_name']
    crole=1
    prole=2
    status="pending"
    servname=Service_Info.query.all()
    professional=User_Info.query.filter_by(role=prole,status=status)
    #return render_template("admin_dashboard.html", name=name,servicename=servname,professional=professional)
    return render_template("admin_dashboard.html",servicename=servname,professional=professional)

#Route to admin search
@app.route("/adminsearch",methods=["GET","POST"])
def admin_search():
    servname=Service_Info.query.all()
    if request.method=="POST":
        #name = request.args['admin_name']
        searchby=request.form.get("s_name")
        searchtext=request.form.get("s_text")
        servname=Service_Info.query.all()
        role1=0
        role2=1
        role3=2
        status="approved"
        if searchby=="services":
            servname=Service_Info.query.all()
            return render_template("admin_search.html",servicename=servname,searchby=searchby)
        elif searchby=="customers":
            name="customers"
            #customers=User_Info.query.filter_by().first()
            customers=User_Info.query.all()
            return render_template("admin_search.html",customers=customers,searchby=searchby)
        elif searchby=="professionals":
            name="professionals"
            #ole=2
            #professionals=User_Info.query.filter_by(role=int(role)).first()
            professionals=User_Info.query.all()
            return render_template("admin_search.html",professionals=professionals,searchby=searchby)
        else:
            servname=Service_Info.query.all()
            return render_template("admin_search.html",servicename=servname)
        #return render_template("admin_dashboard.html", name=name,servicename=servname,professional=professional)
        
    return render_template("admin_search.html",servicename=servname)

#Route for new service
@app.route("/newservice")
def new_service():
    #msg = request.args['msg']
    return render_template("new_service.html")


#-----------------
@app.route("/viewservice/<int:id>/edit", methods=["GET", "POST"])
def edit_service(id):
    service = Service_Info.query.filter_by(id=id).first()
    #print(service.id)
    #return redirect(url_for(".update_service",id=service.id))
    return redirect(url_for(".update_service",id=id))
    #return redirect("editservice")
#testing route
@app.route("/hello/<id>")
def update_service1(id):
    age=id
    return f'<b>Welcome to this site {age}</b>'

######################
@app.route("/editservice",methods=["GET","POST"])
def ed_service():
    #ids = request.args.get('identity')
    #prfser=Service_Info.query.filter_by(id=14).first()
    if request.method =="POST":
        #age=int(id)
        ids=request.form.get("service_id")
        servicename1=request.form.get("service_name")
        description=request.form.get("description")
        baseprice=request.form.get("base_price")
        timerequired=request.form.get("time_required")
        servicetype=request.form.get("service_type")
        prfser=Service_Info.query.filter_by(id=ids).first()
        prfser.servicename=servicename1
        prfser.description=description
        prfser.baseprice=baseprice
        prfser.time_required=timerequired
        prfser.service_type=servicetype
        
        db.session.commit()
        #return f'<b>Updated successfully {ids}</b>'
        return redirect("/admindashboard")

################################
#Route for new service
@app.route("/updateservice/<id>",methods=["GET","POST"])
def update_service(id):
    return render_template("update_service.html",id=id)

#Route to view service details
@app.route("/viewservice/<int:id>", methods=["GET"])
def view_service(id):
    service = Service_Info.query.filter_by(id=id).first()
    return render_template("view_service.html",service=service)

#Route to delete service from admin dashboard
@app.route("/viewservice/<int:id>/delete", methods=["GET", "POST"])
def delete_service(id):
  service = Service_Info.query.filter_by(id=id).first()
  db.session.delete(service)
  db.session.commit()
  return redirect("/admindashboard")


#Route to delete professional's registration

@app.route("/viewprofessional/<int:id>/delete", methods=["GET", "POST"])
def delete_professional(id):
  service = User_Info.query.filter_by(id=id).first()
  db.session.delete(service)
  db.session.commit()
  return redirect("/admindashboard")

# Route to view professional's details

#Route to approve service professional's registration request from admin dashboard
@app.route("/viewprofessional/<int:id>", methods=["GET", "POST"])
def view_professional(id):
  service = User_Info.query.filter_by(id=id).first()
  return render_template ("view_professional.html", id=service.id)
  #return redirect("/admindashboard")

#Route to approve service professional's registration request from admin dashboard
@app.route("/viewprofessional/<int:id>/approve", methods=["GET", "POST"])
def approve_professional(id):
  service = User_Info.query.filter_by(id=id).first()
  service.status="approved"
  #db.session.delete(service)
  db.session.commit()
  return redirect("/admindashboard")

#Route to reject service professional's registration request from admin dashboard
@app.route("/viewprofessional/<int:id>/reject", methods=["GET", "POST"])
def reject_professional(id):
  service = User_Info.query.filter_by(id=id).first()
  service.status="rejected"
  #db.session.delete(service)
  db.session.commit()
  return redirect("/admindashboard")

# Admin summary 
@app.route("/adminsummary", methods=["GET","POST"])
def admin_summary():
    return render_template("admin_summary.html")

# Add service name 

@app.route("/addservice", methods=["GET","POST"])
def add_service():
    if request.method=='POST':
        servicename=request.form.get("service_name")
        description=request.form.get("description")
        baseprice=request.form.get("base_price")
        timerequired=request.form.get("time_required")
        servicetype=request.form.get("service_type")
        service=Service_Info.query.filter_by(servicename=servicename).first()
        if not service:
            new_service=Service_Info(servicename=servicename,description=description,baseprice=baseprice,time_required=timerequired,service_type=servicetype)
            db.session.add(new_service)
            db.session.commit()
            return redirect("/admindashboard")
        elif service:
            return render_template('/new_service.html',msg='"Service exists"')
    return render_template("new_service.html",msg="")


'''------------------------Customer section----------------------------------'''

#Route for customer dashboard
@app.route("/customerdashboard")
def customer_dashboard():
    name = request.args['customer_name']
    id = request.args['customer_id']
    
    service=db.session.query(Service_Info).with_entities(Service_Info.service_type).filter().distinct().all()
    #customerrequest=Customer_Service_Request.query.filter_by(customer_id=id).first()
    customer_service_request=Customer_Service_Request.query.all()
    #service=Service_Info.query.all()
    return render_template("customer_dashboard.html",service=service,customer_id=id,customer_service_request=customer_service_request)

#Different services
@app.route("/cleaning/<customer_id>",methods=["GET","POST"])
def home_cleaning(customer_id):
    customer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    stype="cleaning"
    #servicename=db.session.query(Service_Info).filter(service_type="cleaning").all()
    servicename=Service_Info.query.all()
    return render_template("service_cleaning.html",servicename=servicename,customer_name=customer_name.full_name,customer_id=customer_id)

@app.route("/carpainter/<customer_id>",methods=["GET","POST"])
def home_carpainter(customer_id):
    customer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    stype="carpainter"
    #servicename=db.session.query(Service_Info).filter(service_type="cleaning").all()
    servicename=Service_Info.query.all()
    return render_template("service_carpainter.html",servicename=servicename,customer_name=customer_name.full_name)

@app.route("/plumbing/<customer_id>",methods=["GET","POST"])
def home_plumbing(customer_id):
    customer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    stype="plumbing"
    servicename=Service_Info.query.all()
    return render_template("service_plumbing.html",servicename=servicename,customer_name=customer_name.full_name)

@app.route("/acservicing/<customer_id>",methods=["GET","POST"])
def home_acservicing(customer_id):
    ustomer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    servicename=Service_Info.query.all()
    return render_template("service_acservicing.html",servicename=servicename,customer_name=customer_name.full_name)

@app.route("/painting/<customer_id>",methods=["GET","POST"])
def home_painting(customer_id):
    #return render_template("service_painting.html")    
    customer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    stype="plumbing"
    servicename=Service_Info.query.all()
    return render_template("service_painting.html",servicename=servicename,customer_name=customer_name.full_name)

@app.route("/gardening/<customer_id>",methods=["GET","POST"])
def home_gardening(customer_id):
    customer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    servicename=Service_Info.query.all()
    return render_template("service_gardening.html",servicename=servicename,customer_name=customer_name.full_name)

@app.route("/salooning/<customer_id>",methods=["GET","POST"])
def home_saloon(customer_id):
    customer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    servicename=Service_Info.query.all()
    return render_template("service_salooning.html",servicename=servicename,customer_name=customer_name.full_name)
 
 #Route to approve service professional's registration request from admin dashboard
@app.route("/blockprofessional/<int:id>/approve", methods=["GET", "POST"])
def block_professional(id):
  service = User_Info.query.filter_by(id=id).first()
  service.status="approved"
  #db.session.delete(service)
  db.session.commit()
  return redirect("/adminsearch")

# Unblock service professional
@app.route("/blockprofessional/<int:id>/reject", methods=["GET", "POST"])
def unblock_professional(id):
  service = User_Info.query.filter_by(id=id).first()
  service.status="reject"
  #db.session.delete(service)
  db.session.commit()
  return redirect("/adminsearch")

#Book service
@app.route("/bookservice/<int:id>/<int:customer_id>")
def book_service(id,customer_id):
    #now=datetime.now()
    #timestamp = datetime.timestamp(now)
    serviceid=id
    customerid=customer_id
    professionalid=9
    customer_name="ABC"
    #dateofrequested=date.today()
    #dateofcompletion=date.today()
    dateofrequested=date.today()
    dateofcompletion=date.today()
    servicestatus="pending"
    remarks=None
    new_service=Customer_Service_Request(service_id=serviceid,customer_id=customerid,professional_id=professionalid,date_of_request=dateofrequested,date_of_completion=dateofcompletion,service_status=servicestatus,remarks=remarks)
    db.session.add(new_service)
    db.session.commit()
    return redirect("/login")
    
'''---------------------Professional section---------------------------'''

#Route for professional dashboard
@app.route("/professionaldashboard")
def professional_dashboard():
    name = request.args['professional_name']
    return render_template("professional_dashboard.html",professional_name=name)
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True, port=8080)