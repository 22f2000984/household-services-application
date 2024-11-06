import os
from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import date

app=Flask(__name__)
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
    reviews=db.Column(db.String,nullable=False)
    phone_number=db.Column(db.Integer,nullable=False)
    #customer_service_req=db.relation("Customer_Service_Request",cascade="all,delete",backref="user_info",lazy=True)

class Service_Info(db.Model):
    __tablename__="service_info"
    id=db.Column(db.Integer,primary_key=True)
    servicename=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    baseprice=db.Column(db.Integer,nullable=False)
    time_required=db.Column(db.String,nullable=False)
    service_type=db.Column(db.String,nullable=False)
    city=db.Column(db.String,nullable=False)
    #customer_service_req=db.relation("Customer_Service_Request",cascade="all,delete",backref="service_info",lazy=True)
    
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
    location=db.Column(db.String,nullable=False)
    ratings=db.Column(db.String,nullable=False)
    
    
    

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
                return redirect(url_for(".professional_dashboard",professional_name=usr.full_name,professional_id=usr.id))
            else:
                return render_template('login.html',msg='"Invalid credentials, try again"')
        elif usr and usr.status=="rejected":
            return render_template('login.html',msg="You can't login, admin rejected your account")
        elif usr and usr.status=="pending":
            return render_template('login.html',msg="Admin approval for your account is pending.")
        elif not usr:
            return render_template('login.html',msg='"Invalid credentials, try again"')
    return render_template('login.html',msg="")

# Customer signup 
@app.route("/customersignup", methods=['GET', 'POST'])
def customer_signup():
    usr=db.session.query(User_Info).with_entities(User_Info.location).filter().distinct().all()
    if request.method=='POST':
        email=request.form.get("c_email")
        pwd=request.form.get("c_password")
        fname=request.form.get("c_fullname")
        uname=request.form.get("c_email")
        add=request.form.get("c_address")
        pin=request.form.get("c_pincode")
        cphone=request.form.get("c_phone")
        location=request.form.get("customer_location")
        usr=User_Info.query.filter_by(email=email).first()
        if not usr:
            new_user=User_Info(email=email,full_name=fname,user_name=uname,service_name="Customer",experience=0,pwd=pwd,add=add,pincode=pin,role=1,status="approved",location=location,reviews="None",phone_number=cphone)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        elif usr:
            return render_template('customer_signup.html',msg='"Customer exists"')
    return render_template("customer_signup.html",msg="",usr=usr)

# Service professional signup 
@app.route("/professionalsignup", methods=["GET","POST"])
def serviceprofessional_signup():
    pservicename=Service_Info.query.all()
    servname=db.session.query(User_Info).with_entities(User_Info.location).filter().distinct().all()
    if request.method=='POST':
        f = request.files['file'] 
        f.save(f.filename)
        email=request.form.get("s_email")
        pwd=request.form.get("s_password")
        fname=request.form.get("s_fullname")
        uname=request.form.get("s_email")
        sname=request.form.get("ps_name")
        add=request.form.get("s_address")
        pin=request.form.get("s_pincode")
        sexp=request.form.get("s_exp")
        sphone=request.form.get("s_phone")
        location=request.form.get("customer_location")
        usr=User_Info.query.filter_by(email=email).first()
        if not usr:
            new_professional=User_Info(email=email,full_name=fname,user_name=uname,service_name=sname,experience=sexp,pwd=pwd,add=add,pincode=pin,role=2,status="requested",location=location,reviews="None",phone_number=sphone)
            db.session.add(new_professional)
            db.session.commit()
            return render_template('professional_signup.html',msg='"Service Professional registered successfully"')
        elif usr:
            return render_template('professional_signup.html',msg='"Service Professional exists"',servicename=servname,pservicename=pservicename)
    return render_template("professional_signup.html",msg="",servicename=servname,pservicename=pservicename)


'''--------------------------Admin section---------------------------------------------------'''

#Admin dashboard
@app.route("/admindashboard")
def admin_dashboard():
    crole=1
    prole=2
    status="requested"
    servname=Service_Info.query.all()
    professional=User_Info.query.filter_by(role=prole,status=status)
    user=User_Info.query.all()
    customerservicerequests=Customer_Service_Request.query.all()
    return render_template("admin_dashboard.html",servicename=servname,professional=professional,cservice=customerservicerequests,user=user)

#Admin search page
@app.route("/adminsearch",methods=["GET","POST"])
def admin_search():
    servname=Service_Info.query.all()
    crequests=Customer_Service_Request.query.all()
    if request.method=="POST":
        searchby=request.form.get("s_name")
        searchtext=request.form.get("s_text")
        servname=Service_Info.query.all()
        role1=0
        role2=1
        role3=2
        status="approved"
        if searchby=="option1":
            servname=Service_Info.query.all()
            username=User_Info.query.all()
            crequests=Customer_Service_Request.query.all()
            return render_template("admin_search.html",crequests=crequests,searchby=searchby,searchtext=searchtext,username=username,servname=servname)
        elif searchby=="option2":
            name="customers"
            customers=User_Info.query.all()
            return render_template("admin_search.html",customers=customers,searchby=searchby)
        elif searchby=="option3":
            name="professionals"
            professionals=User_Info.query.all()
            return render_template("admin_search.html",professionals=professionals,searchby=searchby)
        else:
            servname=Service_Info.query.all()
            return render_template("admin_search.html",servicename=servname)
        
    return render_template("admin_search.html",crequests=crequests)

#Add new home service from admindashboard
@app.route("/newservice")
def new_service():
    return render_template("new_service.html")


#Edit home services
@app.route("/viewservice/<int:id>/edit", methods=["GET", "POST"])
def edit_service(id):
    service = Service_Info.query.filter_by(id=id).first()
    return redirect(url_for(".update_service",id=id))
# Continuation... 
@app.route("/updateservice/<id>",methods=["GET","POST"])
def update_service(id):
    service = Service_Info.query.filter_by(id=id).first()
    return render_template("update_service.html",id=id,servicename=service.servicename)

#testing route
@app.route("/hello/<id>")
def update_service1(id):
    age=id
    return f'<b>Welcome to this site {age}</b>'

######################
@app.route("/editservice",methods=["GET","POST"])
def ed_service():
    if request.method =="POST":
        ids=request.form.get("service_id")
        servicename1=request.form.get("service_name")
        description=request.form.get("description")
        baseprice=request.form.get("base_price")
        timerequired=request.form.get("time_required")
        servicetype=request.form.get("service_type")
        city=request.form.get("city")
        prfser=Service_Info.query.filter_by(id=ids).first()
        prfser.servicename=servicename1
        prfser.description=description
        prfser.baseprice=baseprice
        prfser.time_required=timerequired
        prfser.service_type=servicetype
        prfser.city=city
        
        db.session.commit()
        return redirect("/admindashboard")

################################


#View home service details from admin dashborad
@app.route("/viewservice/<int:id>", methods=["GET"])
def view_service(id):
    service = Service_Info.query.filter_by(id=id).first()
    return render_template("view_service.html",service=service)

#Delete home service from admin dashboard
@app.route("/viewservice/<int:id>/delete", methods=["GET", "POST"])
def delete_service(id):
  service = Service_Info.query.filter_by(id=id).first()
  db.session.delete(service)
  db.session.commit()
  return redirect("/admindashboard")


#Delete service professional's registration from admin dashboard
@app.route("/viewprofessional/<int:id>/delete", methods=["GET", "POST"])
def delete_professional(id):
  service = User_Info.query.filter_by(id=id).first()
  db.session.delete(service)
  db.session.commit()
  return redirect("/admindashboard")

#View service professional's registration request from admin dashboard
@app.route("/viewprofessional/<int:id>", methods=["GET", "POST"])
def view_professional(id):
  service = User_Info.query.filter_by(id=id).first()
  return render_template ("view_professional.html",service=service)

#Approve service professional's registration request from admin dashboard
@app.route("/viewprofessional/<int:id>/approve", methods=["GET", "POST"])
def approve_professional(id):
  service = User_Info.query.filter_by(id=id).first()
  service.status="approved"
  db.session.commit()
  return redirect("/admindashboard")

#Reject service professional's registration request from admin dashboard
@app.route("/viewprofessional/<int:id>/reject", methods=["GET", "POST"])
def reject_professional(id):
  service = User_Info.query.filter_by(id=id).first()
  service.status="rejected"
  service.remarks="Admin rejected"
  db.session.commit()
  return redirect("/admindashboard")

# Summary report (pie/bar charts) from admin dashboard 
@app.route("/adminsummary", methods=["GET","POST"])
def admin_summary():
    path=os.path.join('static', 'images', 'plot_pie.png')
    if os.path.exists("path"):
        os.remove(path)
    plot_graph('pie')
    plot_graph('bar')
    return render_template("admin_summary.html")

def plot_graph(abc):
    cservice=Customer_Service_Request.query.all()
    barlabels = ["Requested","Accepted","Closed","Rejected"]
    pielabels=["Poor","Average","Excellent"]
    
    D={'Requested': 0,'Accepted': 0,'Closed': 0,'Rejected': 0}
    D1={"Poor":0,"Average":0,"Excellent":0}
    if abc=="bar":
        for entry in cservice:
            if entry.service_status=="requested":
                D['Requested']+=1
            elif entry.service_status=="accepted":
                D['Accepted']+=1
            elif entry.service_status=="closed":
                D['Closed']+=1
            else:
                D['Rejected']+=1
        data=list(D.values())
        color = ['blue','green', 'purple', 'red']
        plt.bar(barlabels,data,color=color)
        plt.xlabel("STATUS FOR THE SERVICE REQUESTS",color="red")
        plt.ylabel("COUNTS",color="red")
        plt.savefig('static/images/plot_bar.png')
        return plt.show()
    elif abc=="pie":
        for entry in cservice:
            if entry.ratings=="poor":
                D1['Poor']+=1
            elif entry.ratings=="average":
                D1['Average']+=1
            else:
                D1['Excellent']+=1
                
        data1=list(D1.values())
        explode=(0.02,0.02,0.02)
        plt.pie(data1,labels=pielabels,autopct='%1.1f%%',explode=explode)
        plt.legend(loc='lower right')
        plt.savefig('static/images/plot_pie.png')
        return plt.show()

    
#View customer's home service requests from admin dashboard
@app.route("/viewcustomerservicerequests/<int:id>", methods=["GET"])
def customer_service_requests(id):
    service = Customer_Service_Request.query.filter_by(id=id).first()
    servname=Service_Info.query.all()
    user=User_Info.query.all()
    return render_template("view_customerservicerequests.html",servname=servname,service=service,customer_id=service.customer_id,professional_id=service.professional_id,user=user)

#Approve customer's home service request from admin dashboard
@app.route("/viewcustomerservicerequests/<int:id>/accept", methods=["GET", "POST"])
def accept_customer_service_requests(id):
  service = Customer_Service_Request.query.filter_by(id=id).first()
  service.service_status="accepted"
  db.session.commit()
  return redirect("/admindashboard")

#Reject customer's home service request from admin dashboard
@app.route("/viewcustomerservicerequests/<int:id>/reject", methods=["GET", "POST"])
def reject_customer_service_requests(id):
  service = Customer_Service_Request.query.filter_by(id=id).first()
  service.service_status="rejected"
  db.session.commit()
  return redirect("/admindashboard")

#Close customer's home service request from admin dashboard
@app.route("/viewcustomerservicerequests/<int:id>/close", methods=["GET", "POST"])
def close_customer_service_requests(id):
  service = Customer_Service_Request.query.filter_by(id=id).first()
  service.service_status="closed"
  db.session.commit()
  return redirect("/admindashboard")

# Add new home service from admin dashboard 
@app.route("/addservice", methods=["GET","POST"])
def add_service():
    if request.method=='POST':
        servicename=request.form.get("service_name")
        description=request.form.get("description")
        baseprice=request.form.get("base_price")
        timerequired=request.form.get("time_required")
        servicetype=request.form.get("service_type")
        city=request.form.get("city")
        service=Service_Info.query.filter_by(servicename=servicename).first()
        location=Service_Info.query.filter_by(city=city).first()
        new_service=Service_Info(servicename=servicename,description=description,baseprice=baseprice,time_required=timerequired,service_type=servicetype,city=city)
        db.session.add(new_service)
        db.session.commit()
        return redirect("/admindashboard")
    return render_template("new_service.html",msg="")

 #Approve(unblock) professional from admin dashboard search
@app.route("/blockprofessional/<int:id>/approve", methods=["GET", "POST"])
def block_professional(id):
  service = User_Info.query.filter_by(id=id).first()
  service.status="approved"
  db.session.commit()
  return redirect("/adminsearch")

# Unblock service professional from admin dashboard search
@app.route("/blockprofessional/<int:id>/reject", methods=["GET", "POST"])
def unblock_professional(id):
  service = User_Info.query.filter_by(id=id).first()
  service.status="rejected"
  db.session.commit()
  return redirect("/adminsearch")

'''------------------------Customer section----------------------------------'''

#Customer dashboard
@app.route("/customerdashboard")
def customer_dashboard():
    #name = request.args['customer_name']
    id = request.args['customer_id']
    service=db.session.query(Service_Info).with_entities(Service_Info.service_type).filter().distinct().all()
    servname=Service_Info.query.all()
    customer_service_request=Customer_Service_Request.query.all()
    user=User_Info.query.filter_by(id=id).first()
    customer_location=user.location
    return render_template("customer_dashboard.html",service=service,servname=servname,customer_id=id,customer_service_request=customer_service_request,name=user.full_name,customer_location=customer_location,customer_name=user.full_name)

#Go back to customer dashboard 
@app.route("/customerdashboard/<int:id>")
def customer_dashboard1(id):
    service=db.session.query(Service_Info).with_entities(Service_Info.service_type).filter().distinct().all()
    servname=Service_Info.query.all()
    customer_service_request=Customer_Service_Request.query.all()
    user=User_Info.query.filter_by(id=id).first()
    customer_location=user.location
    return render_template("customer_dashboard.html",service=service,servname=servname,customer_id=id,customer_service_request=customer_service_request,name=user.full_name,customer_location=customer_location,customer_name=user.full_name)

#View customer's prfile from customer dashboard
@app.route("/viewcustomerprofile/<int:id>", methods=["GET", "POST"])
def view_customer_profile(id):
  professional_id=id
  service = User_Info.query.filter_by(id=id).first()
  return render_template ("view_customer_profile.html",service=service,customer_id_id=id)


# Edit customer's profile from customer dashboard
@app.route("/viewcustomerprofile/<int:id>/edit", methods=["GET", "POST"])
def view_customer_profile_edit(id):
  customer_id=id
  pservicename=Service_Info.query.all()
  servname=db.session.query(User_Info).with_entities(User_Info.location).filter().distinct().all()
  service = User_Info.query.filter_by(id=id).first()
  user=User_Info.query.all()
  return render_template ("customer_profileedit.html",service=service,customer_id=id,user=user,pservicename=pservicename,servname=servname)

@app.route("/customerprofileupdate/<int:customer_id>", methods=["GET","POST"])
def customer_profile_update(customer_id):
    if request.method =="POST":
        ids=customer_id
        email=request.form.get("c_email")
        pwd=request.form.get("c_password")
        full_name=request.form.get("c_fullname")
        phone_number=request.form.get("c_phone")
        add=request.form.get("c_address")
        location=request.form.get("customer_location")
        pincode=request.form.get("c_pincode")
        prfser=User_Info.query.filter_by(id=ids).first()
        prfser.email=email
        prfser.pwd=pwd
        prfser.full_name=full_name
        prfser.user_name=email
        prfser.add=add
        prfser.pincode=pincode
        prfser.location=location
        prfser.phone_number=phone_number
        
        db.session.commit()
        return redirect(url_for(".customer_dashboard1",id=customer_id))
    
    

#Links to book different services from customer dashboard
@app.route("/cleaning/<customer_id>",methods=["GET","POST"])
def home_cleaning(customer_id):
    customer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    stype="cleaning"
    servicename=Service_Info.query.all()
    return render_template("service_cleaning.html",servicename=servicename,customer_name=customer_name.full_name,customer_id=customer_id,customer_location=customer_name.location)

@app.route("/carpainter/<customer_id>",methods=["GET","POST"])
def home_carpainter(customer_id):
    customer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    stype="carpainter"
    servicename=Service_Info.query.all()
    return render_template("service_carpainter.html",servicename=servicename,customer_name=customer_name.full_name,customer_id=customer_id,customer_location=customer_name.location)

@app.route("/plumbing/<customer_id>",methods=["GET","POST"])
def home_plumbing(customer_id):
    customer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    stype="plumbing"
    servicename=Service_Info.query.all()
    return render_template("service_plumbing.html",servicename=servicename,customer_name=customer_name.full_name,customer_id=customer_id,customer_location=customer_name.location)

@app.route("/acservicing/<customer_id>",methods=["GET","POST"])
def home_acservicing(customer_id):
    customer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    servicename=Service_Info.query.all()
    return render_template("service_acservicing.html",servicename=servicename,customer_name=customer_name.full_name,customer_id=customer_id,customer_location=customer_name.location)

@app.route("/painting/<customer_id>",methods=["GET","POST"])
def home_painting(customer_id):   
    customer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    stype="plumbing"
    servicename=Service_Info.query.all()
    return render_template("service_painting.html",servicename=servicename,customer_name=customer_name.full_name,customer_id=customer_id,customer_location=customer_name.location)

@app.route("/gardening/<customer_id>",methods=["GET","POST"])
def home_gardening(customer_id):
    customer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    servicename=Service_Info.query.all()
    return render_template("service_gardening.html",servicename=servicename,customer_name=customer_name.full_name,customer_id=customer_id,customer_location=customer_name.location)

@app.route("/saloning/<customer_id>",methods=["GET","POST"])
def home_saloning(customer_id):
    customer_id=customer_id
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    servicename=Service_Info.query.all()
    return render_template("service_saloning.html",servicename=servicename,customer_name=customer_name.full_name,customer_id=customer_id,customer_location=customer_name.location)
 
#  Location based servicing 

@app.route("/location/<int:customer_id>/searchtext",methods=["GET","POST"])
def location_servicing(customer_id,searchtext):
    customer_id=customer_id
    searchtext=searchtext
    customer_name=User_Info.query.filter_by(id=customer_id).first()
    servicename=Service_Info.query.all()
    return render_template("location_servicing.html",servicename=servicename,customer_name=customer_name.full_name,customer_id=customer_id,searchtext=searchtext)

#Book home service from customer dashboard
@app.route("/bookservice/<int:id>/<int:customer_id>")
def book_service(id,customer_id):
    serviceid=id
    customerid=customer_id
    professionalid=9
    customer_name="ABC"
    usr=User_Info.query.filter_by(id=customerid).first()
    dateofrequested=date.today()
    dateofcompletion=date.today()
    servicestatus="requested"
    remarks=None
    new_service=Customer_Service_Request(service_id=serviceid,customer_id=customerid,professional_id=professionalid,date_of_request=dateofrequested,date_of_completion=dateofcompletion,service_status=servicestatus,remarks=remarks,location=usr.location,ratings=remarks)
    db.session.add(new_service)
    db.session.commit()
    return redirect(url_for(".customer_dashboard1",id=customer_id))

#close home service from customer dashboard
@app.route("/customercloseservice/<int:id>/<int:customer_id>")
def customer_close_service(id,customer_id):
    #service = Customer_Service_Request.query.filter_by(id=id).first()
    #service.service_status="closed"
    #db.session.commit()
    #return redirect(url_for(".customer_dashboard1",id=customer_id))
    return render_template("customer_update_servicerequest.html",id=id,customer_id=customer_id)

# In continution to close ther service..
@app.route("/customerupdateservice/<int:id>/<int:customer_id>", methods=["GET","POST"])
def customer_update_service(id,customer_id):
    if request.method =="POST":
        id=id
        ids=customer_id
        customer_id=customer_id
        servicestatus=request.form.get("service_status")
        servicerating=request.form.get("service_rating")
        serviceremark=request.form.get("service_remark")
        service = Customer_Service_Request.query.filter_by(id=id).first()
        service.service_status=servicestatus
        service.remarks=serviceremark
        service.ratings=servicerating
        db.session.commit()
        return redirect(url_for(".customer_dashboard1",id=customer_id))

# Edit home service from customer dashboard 
@app.route("/customereditservice/<int:id>/<int:customer_id>")
def customer_edit_service(id,customer_id):
    return render_template("customer_edit_servicerequest.html",id=id,customer_id=customer_id)

# In continution to edit home service..
@app.route("/customerupdateeditservice/<int:id>/<int:customer_id>", methods=["GET","POST"])
def customer_update_edit_service(id,customer_id):
    if request.method =="POST":
        id=id
        ids=customer_id
        customer_id=customer_id
        servicestatus=request.form.get("service_status")
        servicedor=request.form.get("service_dor")
        serviceremark=request.form.get("service_remark")
        service = Customer_Service_Request.query.filter_by(id=id).first()
        service.service_status=servicestatus
        service.remarks=serviceremark
        service.date_of_completion=servicedor
        db.session.commit()
        return redirect(url_for(".customer_dashboard1",id=customer_id))
    
#Customer's summary reports (pie/bar charts) customer dashboard   
@app.route("/customersummary/<int:customer_id>", methods=["GET","POST"])
def customer_summary(customer_id):
    usr=User_Info.query.filter_by(id=customer_id).first()
    path=os.path.join('static', 'images', 'customer_plot_pie.png')
    if os.path.exists("path"):
        os.remove(path)
    #customer_plot_graph('pie',customer_id)
    customer_plot_graph('bar',customer_id)
    return render_template("customer_summary.html",customer_name=usr.full_name,customer_id=customer_id)

def customer_plot_graph(abc,customer_id):
    cservice=Customer_Service_Request.query.filter_by(customer_id=customer_id).all()
    barlabels = ["Requested","Accepted","Closed","Rejected"]
    #pielabels=["Poor","Average","Excellent"]
    D={'Requested': 0,'Accepted':0,'Closed': 0,'Rejected': 0}
    D1={"Poor":0,"Average":0,"Excellent":0}
    if abc=="bar":
        for entry in cservice:
                if entry.service_status =="requested":
                    D['Requested']+=1
                elif entry.service_status=="accepted":
                    D['Accepted']+=1
                elif entry.service_status=="closed":
                    D['Closed']+=1
                else:
                    D['Rejected']+=1
        data=list(D.values())
        color = ['blue','green', 'purple','red']
        plt.bar(barlabels,data,color=color)
        plt.xlabel("STATUS FOR THE SERVICE REQUESTS",color="red")
        plt.ylabel("COUNTS",color="red")
        plt.savefig('static/images/customer_plot_bar.png')
        return plt.show()
    elif abc=="pie":
        for entry in cservice:
                if entry.ratings=="poor":
                    D1['Poor']+=1
                elif entry.ratings=="average":
                    D1['Average']+=1
                else:
                    D1['Excellent']+=1
                        
        data1=list(D1.values())
        explode=(0.02,0.02,0.02)
        plt.pie(data1,labels=pielabels,autopct='%1.1f%%',explode=explode)
        plt.legend(loc='lower right')
        plt.savefig('static/images/customer_plot_pie.png')
        return plt.show()

#Searching from customer dashboard
@app.route("/customersearch/<int:customer_id>",methods=["GET","POST"])
def customer_search(customer_id):
    servname=Service_Info.query.all()
    crequests=Customer_Service_Request.query.all()
    if request.method=="POST":
        searchby=request.form.get("c_name")
        searchtext=request.form.get("c_text")
        servname=Service_Info.query.all()
        if searchby=="option1" and searchtext=="cleaning":
            servname=Service_Info.query.all()
            username=User_Info.query.all()
            crequests=Customer_Service_Request.query.all()
            #return render_template("service_cleaning.html",crequests=crequests,searchby=searchby,searchtext=searchtext,username=username,servname=servname,customer_id=customer_id)
            return redirect(url_for(".home_cleaning",customer_id=customer_id,crequests=crequests,username=username))
        elif searchby=="option1" and searchtext=="carpainter":
            servname=Service_Info.query.all()
            username=User_Info.query.all()
            crequests=Customer_Service_Request.query.all()
            return redirect(url_for(".home_carpainter",customer_id=customer_id))
        elif searchby=="option1" and searchtext=="plumbing":
            servname=Service_Info.query.all()
            username=User_Info.query.all()
            crequests=Customer_Service_Request.query.all()
            return redirect(url_for(".home_plumbing",customer_id=customer_id))
        elif searchby=="option1" and searchtext=="acservicing":
            servname=Service_Info.query.all()
            username=User_Info.query.all()
            crequests=Customer_Service_Request.query.all()
            return redirect(url_for(".home_acservicing",customer_id=customer_id))
        elif searchby=="option1" and searchtext=="painting":
            servname=Service_Info.query.all()
            username=User_Info.query.all()
            crequests=Customer_Service_Request.query.all()
            return redirect(url_for(".home_painting",customer_id=customer_id))
        elif searchby=="option1" and searchtext=="gardening":
            servname=Service_Info.query.all()
            username=User_Info.query.all()
            crequests=Customer_Service_Request.query.all()
            return redirect(url_for(".home_gardening",customer_id=customer_id))
        elif searchby=="option1" and searchtext=="saloning":
            servname=Service_Info.query.all()
            username=User_Info.query.all()
            crequests=Customer_Service_Request.query.all()
            return redirect(url_for(".home_saloning",customer_id=customer_id))
        elif searchby=="option2":
            searchtext=searchtext
            servicename=Service_Info.query.all()
            username=User_Info.query.all()
            crequests=Customer_Service_Request.query.all()
            #return redirect(url_for(".location_servicing",customer_id=customer_id,srchtxt=searchtext)) 
            return render_template("location_servicing.html",servicename=servicename,customer_id=customer_id,searchtext=searchtext)
        elif searchby=="option3":
            searchtext=searchtext
            servicename=Service_Info.query.all()
            username=User_Info.query.all()
            un=User_Info.query.filter_by(pincode=searchtext).first()
            location=un.location
            crequests=Customer_Service_Request.query.all()
            #return redirect(url_for(".location_servicing",customer_id=customer_id,srchtxt=searchtext)) 
            return render_template("pincode_servicing.html",servicename=servicename,customer_id=customer_id,searchtext=searchtext,location=location)
    return render_template("customer_search.html",crequests=crequests,customer_id=customer_id)

    
'''---------------------Professional section---------------------------'''

#Professional dashboard
@app.route("/professionaldashboard/")
def professional_dashboard():
    name = request.args['professional_name']
    id=request.args['professional_id']
    cservice=Customer_Service_Request.query.all()
    usr=User_Info.query.filter_by(id=id).first()
    user=User_Info.query.all()
    return render_template("professional_dashboard.html",professional_name=name,professional_id=id,cservice=cservice,professional_location=usr.location,user=user)

#Go back to professional dashboard
@app.route("/professionaldashboard/<int:professional_id>")
def professional_dashboard1(professional_id):
    cservice=Customer_Service_Request.query.all()
    usr=User_Info.query.filter_by(id=professional_id).first()
    user=User_Info.query.all()
    name=usr.full_name
    return render_template("professional_dashboard.html",professional_name=name,professional_id=professional_id,cservice=cservice,professional_location=usr.location,user=user)

#close home service from professional dashboard
@app.route("/professionalcloseservice/<int:id>/<int:professional_id>")
def professional_close_service(id,professional_id):
    #service = Customer_Service_Request.query.filter_by(id=id).first()
    #service.service_status="closed"
    #db.session.commit()
    #return redirect(url_for(".customer_dashboard1",id=customer_id))
    return render_template("professional_update_servicerequest.html",id=id,professional_id=professional_id)

# In continution to close the service..
@app.route("/professionalupdateservice/<int:id>/<int:professional_id>", methods=["GET","POST"])
def professional_update_service(id,professional_id):
    if request.method =="POST":
        id=id
        ids=professional_id
        professional_id=professional_id
        servicestatus=request.form.get("service_status")
        servicerating=request.form.get("service_rating")
        serviceremark=request.form.get("service_remark")
        service = Customer_Service_Request.query.filter_by(id=id).first()
        service.service_status=servicestatus
        service.remarks=serviceremark
        service.ratings=servicerating
        db.session.commit()
        return redirect(url_for(".professional_dashboard1",professional_id=professional_id))

#View service professional's profile from professional dashboard
@app.route("/viewprofessionalprofile/<int:id>", methods=["GET", "POST"])
def view_professional_profile(id):
  professional_id=id
  service = User_Info.query.filter_by(id=id).first()
  return render_template ("view_professional_profile.html",service=service,professional_id=id)
  
# Edit professional's profile from professional dashboard
@app.route("/viewprofessionalprofile/<int:id>/edit", methods=["GET", "POST"])
def view_professional_profile_edit(id):
  professional_id=id
  pservicename=Service_Info.query.all()
  servname=db.session.query(User_Info).with_entities(User_Info.location).filter().distinct().all()
  service = User_Info.query.filter_by(id=id).first()
  user=User_Info.query.all()
  return render_template ("professional_profileedit.html",service=service,professional_id=id,user=user,pservicename=pservicename,servname=servname)

# Professionals' profile update in continuation of above from professional dashboard
@app.route("/professionalprofileupdate/<int:professional_id>", methods=["GET","POST"])
def professional_profile_update(professional_id):
    if request.method =="POST":
        ids=professional_id
        email=request.form.get("s_email")
        pwd=request.form.get("s_password")
        full_name=request.form.get("s_fullname")
        service_name=request.form.get("ps_name")
        experience=request.form.get("s_exp")
        add=request.form.get("s_address")
        location=request.form.get("customer_location")
        pincode=request.form.get("s_pincode")
        prfser=User_Info.query.filter_by(id=ids).first()
        prfser.email=email
        prfser.pwd=pwd
        prfser.full_name=full_name
        prfser.user_name=email
        prfser.service_name=service_name
        prfser.exp=experience
        prfser.add=add
        prfser.pincode=pincode
        prfser.location=location
        
        db.session.commit()
        return redirect(url_for(".professional_dashboard1",professional_id=professional_id))
    
    
# Accept customer's home service request by a professional from professional dahboard
@app.route("/acceptcustomerservicerequests/<int:professional_id>/<int:id>/accept", methods=["GET", "POST"])
def accept_customer_service_requests_by_professional(professional_id,id):
  service = Customer_Service_Request.query.filter_by(id=id).first()
  service.service_status="accepted"
  service.professional_id=professional_id
  db.session.commit()
  return redirect(url_for(".professional_dashboard1",professional_id=professional_id))

#Reject customer's home service request by a professional from professional dahboard
@app.route("/rejectcustomerservicerequests/<int:professional_id>/<int:id>/reject", methods=["GET", "POST"])
def reject_customer_service_requests_by_professional(professional_id,id):
  service = Customer_Service_Request.query.filter_by(id=id).first()
  service.service_status="rejected"
  db.session.commit()
  return redirect(url_for(".professional_dashboard1",professional_id=professional_id,id=id))
  
#Professional's summary reports (pie/bar charts) professional dashboard   
@app.route("/professionalsummary/<int:professional_id>", methods=["GET","POST"])
def professional_summary(professional_id):
    usr=User_Info.query.filter_by(id=professional_id).first()
    path=os.path.join('static', 'images', 'prof_plot_pie.png')
    if os.path.exists("path"):
        os.remove(path)
    prof_plot_graph('pie',professional_id)
    prof_plot_graph('bar',professional_id)
    return render_template("professional_summary.html",professional_name=usr.full_name,professional_id=usr.id)

def prof_plot_graph(abc,professional_id):
    cservice=Customer_Service_Request.query.filter_by(professional_id=professional_id).all()
    barlabels = ["Received","Accepted","Closed","Rejected"]
    pielabels=["Poor","Average","Excellent"]
    D={'Received': 0,'Accepted':0,'Closed': 0,'Rejected': 0}
    D1={"Poor":0,"Average":0,"Excellent":0}
    if abc=="bar":
        for entry in cservice:
                if entry.service_status =="requested":
                    D['Received']+=1
                elif entry.service_status=="accepted":
                    D['Accepted']+=1
                elif entry.service_status=="closed":
                    D['Closed']+=1
                else:
                    D['Rejected']+=1
        data=list(D.values())
        color = ['blue','green', 'purple','red']
        plt.bar(barlabels,data,color=color)
        plt.xlabel("STATUS FOR THE SERVICE REQUESTS",color="red")
        plt.ylabel("COUNTS",color="red")
        plt.savefig('static/images/prof_plot_bar.png')
        return plt.show()
    elif abc=="pie":
        for entry in cservice:
                if entry.ratings=="poor":
                    D1['Poor']+=1
                elif entry.ratings=="average":
                    D1['Average']+=1
                else:
                    D1['Excellent']+=1
                        
        data1=list(D1.values())
        explode=(0.02,0.02,0.02)
        plt.pie(data1,labels=pielabels,autopct='%1.1f%%',explode=explode)
        plt.legend(loc='lower right')
        plt.savefig('static/images/prof_plot_pie.png')
        return plt.show()

import json
#Searching from professional's dashboard
@app.route("/professionalsearch/<int:professional_id>",methods=["GET","POST"])
def professional_search(professional_id):
    servname=Service_Info.query.all()
    crequests=Customer_Service_Request.query.all()
    if request.method=="POST":
        searchby=request.form.get("p_name")
        searchtext=request.form.get("p_text")
        servname=Service_Info.query.all()
        if searchby=="option1":
            servname=Service_Info.query.all()
            username=User_Info.query.all()
            crequests=Customer_Service_Request.query.all()
            cr=Customer_Service_Request.query.filter_by(professional_id=professional_id).first()
            dtlist=db.session.query(Customer_Service_Request).with_entities(Customer_Service_Request.date_of_request).filter().distinct().all()
            #loclist=db.session.query(Service_Info).with_entities(Service_Info.city).filter().distinct().all()
            #pinlist=db.session.query(User_Info).with_entities(User_Info.pincode).filter().distinct().all()
            customer_id=cr.customer_id
            datelist=[]
            for dt in dtlist:
                datelist.append(dt[0])
            #locationlist=[]
            #for dt in loclist:
            #    locationlist.append(dt[0]) 
            #pincodelist=[]
            #for dt in pinlist:
            #    pincodelist.append(dt[0]) 
            #return render_template("professional_search.html",crequests=crequests,searchby=searchby,searchtext=searchtext,username=username,servname=servname,professional_id=professional_id,customer_id=customer_id,datelist=datelist,pincodelist=pincodelist,locationlist=locationlist)
            return render_template("professional_search.html",crequests=crequests,searchby=searchby,searchtext=searchtext,username=username,servname=servname,professional_id=professional_id,customer_id=customer_id,datelist=datelist)
        elif searchby=="option2":
            servname=Service_Info.query.all()
            username=User_Info.query.all()
            crequests=Customer_Service_Request.query.all()
            un=User_Info.query.filter_by(id=professional_id).first()
            prof_name=un.full_name
            return render_template("professional_search.html",crequests=crequests,searchby=searchby,searchtext=searchtext,username=username,servname=servname,professional_id=professional_id,prof_name=prof_name)
        elif searchby=="option3":
            servname=Service_Info.query.all()
            username=User_Info.query.all()
            un=User_Info.query.filter_by(id=professional_id).first()
            prof_name=un.full_name
            crequests=Customer_Service_Request.query.all()
            cr=Customer_Service_Request.query.filter_by(professional_id=professional_id).first()
            customer_id=cr.customer_id
            return render_template("professional_search.html",crequests=crequests,searchby=searchby,searchtext=searchtext,username=username,servname=servname,professional_id=professional_id,customer_id=customer_id,prof_name=prof_name)   
    return render_template("professional_search.html",crequests=crequests,professional_id=professional_id)
    #return render_template("professional_search.html",crequests=crequests,username=username,servname=servname,professional_id=professional_id,customer_id=customer_id,datelist=datelist,pincodelist=pincodelist,locationlist=locationlist)


    
    
    
    '''------------ Plotting graphs for admin dashboardd--------------------------------'''

#plotting graph for admin dashbaord

        
    

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True, port=8080)