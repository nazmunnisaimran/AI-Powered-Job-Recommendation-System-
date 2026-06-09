from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to user profile
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    skills = db.Column(db.Text, default='')  # Comma-separated list of skills, e.g., "Python, SQL, HTML"
    resume_filename = db.Column(db.String(255), nullable=True)
    extracted_text = db.Column(db.Text, nullable=True)  # Raw text extracted from PDF for TF-IDF similarity
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100), default='Remote')
    salary = db.Column(db.String(100), default='Not Specified')
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, default='')  # Comma-separated skills required, e.g., "Python, SQL, Docker"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class LearningResource(db.Model):
    __tablename__ = 'learning_resources'
    
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(80), nullable=False)  # Skill tag associated with this resource
    title = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(100), default='Online Course')
    url = db.Column(db.String(500), nullable=False)
