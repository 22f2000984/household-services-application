from flask_sqlalchemy import SQLAlchemy
#from flask import Flask

#app=Flask(__name__, template_folder='../templates') 
db = SQLAlchemy()

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
    #customer_service_request=db.relation("Customer_Service_Request",cascade="all,delete",backref="user_info",lazy=True)

class Service_Info(db.Model):
    __tablename__="service_info"
    id=db.Column(db.Integer,primary_key=True)
    servicename=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    baseprice=db.Column(db.Integer,nullable=False)
    time_required=db.Column(db.String,nullable=False)
    service_type=db.Column(db.String,nullable=False)
    #customer_service_request=db.relation("Customer_Service_Request",cascade="all,delete",backref="service_info",lazy=True)

    
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
