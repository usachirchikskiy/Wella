from . import db
from sqlalchemy import ARRAY, DateTime
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(250))

    def __init__(self, name,password):
        self.name = name
        self.password = password


class CategoryDress(db.Model):
    __tablename__ = 'category_dress'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
    dress_id = db.Column('dress_id', db.Integer, db.ForeignKey('dress.id'))


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    title_uz = db.Column(db.String(250))
    created_at = db.Column(db.String(250),default = datetime.now().strftime("%Y-%m-%d").split(" ")[0])

    def __init__(self, title,title_uz):
        self.title = title
        self.title_uz = title_uz

class Dress(db.Model):
    __tablename__ = 'dress'

    id = db.Column(db.Integer, primary_key=True)
    photos = db.Column(ARRAY(db.String(250)))
    title = db.Column(db.String(250))
    title_uz = db.Column(db.String(250))
    description = db.Column(db.Text())
    description_uz = db.Column(db.Text())
    brand = db.Column(db.String(50))
    country = db.Column(db.String(50))
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    color_uz = db.Column(db.String(50))
    price = db.Column(db.String(50))
    available = db.Column(db.Boolean)
    isBestSeller = db.Column(db.Boolean)
    isCollection = db.Column(db.Boolean)
    created_at = db.Column(db.String(250),default = datetime.now().strftime("%Y-%m-%d").split(" ")[0])
    categories = db.relationship(Category, secondary="category_dress", backref='dresses')

    def __init__(self, photos,title,title_uz, description,description_uz, brand, country, size, color,color_uz, price, available,isBestSeller,isCollection):
        self.photos = photos
        self.title = title
        self.title_uz = title_uz
        self.description = description
        self.description_uz = description_uz
        self.brand = brand
        self.country = country
        self.size = size
        self.color = color
        self.color_uz = color_uz
        self.price = price
        self.available = available
        self.isBestSeller = isBestSeller
        self.isCollection = isCollection


class Banner(db.Model):
    __tablename__ = 'banner'

    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(250))
    title = db.Column(db.String(250))
    isActive = db.Column(db.Boolean)
    created_at = db.Column(db.String(250),default = datetime.now().strftime("%Y-%m-%d").split(" ")[0])

    def __init__(self, photo, title,isActive):
        self.title = title
        self.photo = photo
        self.isActive = isActive

class Gallery(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(ARRAY(db.String(250)))
    title = db.Column(db.String(250))
    isActive = db.Column(db.Boolean)
    created_at = db.Column(db.String(250),default = datetime.now().strftime("%Y-%m-%d").split(" ")[0])


    def __init__(self, photo, title,isActive):
        self.title = title
        self.photo = photo
        self.isActive = isActive


class Partner(db.Model):
    __tablename__ = 'partner'

    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(250))
    title = db.Column(db.String(250))
    isActive = db.Column(db.Boolean)
    created_at = db.Column(db.String(250),default = datetime.now().strftime("%Y-%m-%d").split(" ")[0])

    def __init__(self, photo, title,isActive):
        self.title = title
        self.photo = photo
        self.isActive = isActive
