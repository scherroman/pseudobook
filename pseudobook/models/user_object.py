'''
model for a user
'''

import uuid

from hexlistserver.app import app, db

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class UserObject(db.Model):
    __tablename__ = 'user_objects'

    userID = db.Column(db.String(), primary_key=True)
    firstName = db.Column(db.String(20))
    lastName = db.Column(db.String(20))
    email = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))

    address = db.Column(db.String(40))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zipCode = db.Column(db.String(5))
    telephone = db.Column(db.String(10))
    firstName = db.Column(db.String(20))
    firstName = db.Column(db.String(20))

    is_active = True
    is_authenticated = True
    is_anonymous = False
    
    # accountCreationDate DATETIME,
    # rating INTEGER,

    def __init__(self, username):
        self.userID = uuid.uuid4().urn[9:] # make a uuid, convert to urn/string, uuid starts after 9th char
        self.username = username

    def __repr__(self):
        return ('{{id: {},'
                + 'name: {} {}}}').format(
                self.userID,
                self.firstName,
                self.lastName
            )

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.userID})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired) as e:
            return None
        user = UserObject.query.get(data['id'])
        return user
    
    def get_id(self):
        return self.userID
        
'''
author @roman
'''