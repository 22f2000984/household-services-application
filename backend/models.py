from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

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
    
    