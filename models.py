from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

from passlib.apps import custom_app_context as pwd_context
import random
import string
from itsdangerous import (TimedJSONWebSignatureSerializer as
                          Serializer,
                          BadSignature,
                          SignatureExpired)


Base = declarative_base()


# Generate a secret key to create and verify tokens
secret_key = ''.join(
    random.choice(string.ascii_uppercase + string.digits)
    for x in xrange(32))


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(250), nullable=False)
    user_email = Column(String(250), nullable=False, unique=True)
    user_picture = Column(String(250))
    password_hash = Column(String)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_email': self.user_email
        }

    # Methods to generate and verify password_hash
    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # Method to generate auth tokens
    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({"user_id": self.user_id})

    # Method to verify auth tokens
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid token, but expired
            return None
        except BadSignature:
            # Invalid token
            return None
        user_id = data['user_id']
        return user_id


class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    user = relationship('User', backref=backref(
        'categories', cascade='all, delete-orphan'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'user_id': self.user_id
        }


class Item(Base):
    __tablename__ = 'item'

    item_id = Column(Integer, primary_key=True)
    item_name = Column(String(80), nullable=False)
    item_description = Column(String)
    item_price = Column(String(20))
    item_date = Column(DateTime, default=func.now())
    category_id = Column(Integer, ForeignKey('category.category_id'))
    category = relationship('Category', backref=backref(
        'items', cascade='all, delete-orphan'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'item_name': self.item_name,
           'item_description': self.item_description,
           'item_id': self.item_id,
           'item_price': self.item_price,
           'item_date': self.item_date,
           'category_id': self.category_id
        }


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
