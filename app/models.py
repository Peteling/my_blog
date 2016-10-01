from . import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role', lazy='dynamic')

	def __repr__(self):
		return '<Role %r>' % self.name


class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	
	email = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	
	#check the password is right or not
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
	
	#use password to create the password_lists
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
		
	#check the password is pair the database_password or not
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))