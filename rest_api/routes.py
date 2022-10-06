from flask import current_app as app
from .models import Dress, Category, Banner,Partner, User, Gallery, db
from .schemas import DressSchema, BannerSchema, PartnerSchema, CategoryDressSchema, GallerySchema
from flask import Flask, request, jsonify, send_from_directory, make_response
from sqlalchemy import asc
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import datetime
from .jwt import token_required
import jwt

dress_schema = DressSchema()
category_dress_schema = CategoryDressSchema()

category_dress_schemas = CategoryDressSchema(many=True)
dress_schemas = DressSchema(many = True)

banner_schema = BannerSchema(many = True)
partner_schema = PartnerSchema(many = True)

gallery_schema = GallerySchema(many = True)


@app.route("/check", methods = ['GET'])
@token_required
def check(current_user):
    return jsonify(
        status  = 'success'
    )

@app.route('/login', methods=['POST'])
def login_user():

  body = request.get_json()

  if not body['name'] or not body['password']:
     return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

  user = User.query.filter_by(name=body['name']).first()

  if user and check_password_hash(user.password, body['password']):
     token = jwt.encode({'id': user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=1)}, app.config['SECRET_KEY'],"HS256")
     return jsonify({'token' : token})

  return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

@app.route('/register', methods=['POST'])
def signup_user():
 data = request.get_json()

 hashed_password = generate_password_hash(data['password'], method='sha256')

 new_user = User(name=data['name'], password=hashed_password)
 db.session.add(new_user)
 db.session.commit()

 return jsonify({'message': 'registered successfully'})

#filename
@app.route('/filename/<string:filename>',methods = ['GET'])
def downloads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#Category routes
@app.route("/getCategories", methods = ['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify(category_dress_schemas.dump(categories))

@app.route("/getCategory/<int:id>", methods = ['GET'])
def get_category(id):
    category = Category.query.get(id)
    return jsonify(category_dress_schema.dump(category))

@app.route("/deleteCategory/<int:id>", methods = ['DELETE'])
@token_required
def delete_category(current_user,id):
    delete = Category.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    return jsonify(
        status  = 'success',
        message = 'category deleted'
    )

@app.route("/updateCategoryTitle/<int:id>", methods = ['PUT'])
@token_required
def update_category_title(current_user,id):
    body = request.get_json()
    category = Category.query.get(id)
    category.title = body['title']
    db.session.commit()
    return jsonify(
        status  = 'success',
        message = 'category title changed'
    )

@app.route("/addCategory", methods = ['POST'])
@token_required
def insert_category(current_user):
    body = request.get_json()
    category = Category(body['title'],body['title_uz'])
    db.session.add(category)
    db.session.commit()
    return jsonify(
    status = 'success',
    message = 'category created'
    )

#Partner routes
@app.route('/getPartners', methods=['GET'])
def get_partners():
    partners = Partner.query.all()
    return jsonify(partner_schema.dump(partners))


@app.route("/deletePartner/<int:id>", methods = ['DELETE'])
@token_required
def delete_partner(current_user,id):
    partner = Partner.query.filter_by(id = id).one()
    os.remove(app.config['UPLOAD_FOLDER']+"/"+partner.photo)
    db.session.delete(partner)
    db.session.commit()
    return jsonify(
    status = 'success',
    message = 'partner deleted'
    )

@app.route("/addPartner", methods = ['POST'])
@token_required
def insert_partner(current_user):
    body = json.loads(request.form['data'])
    files = request.files.getlist('file')
    files[0].save(os.path.join(app.config['UPLOAD_FOLDER'], files[0].filename))
    photo = request.host_url+"filename/"+files[0].filename
    db.session.add(Partner(photo,body['title'], body['isActive']))
    db.session.commit()
    return jsonify(
    status = 'success',
    message = 'partner created'
    )

#Banner routes
@app.route('/getBanners', methods=['GET'])
def get_banners():
    banners = Banner.query.order_by(Banner.id.asc()).all()
    return jsonify(banner_schema.dump(banners))

@app.route('/getBannersTrue', methods=['GET'])
def get_bannersTrue():
    banners = Banner.query.filter_by(isActive = True)
    return jsonify(banner_schema.dump(banners))

@app.route("/deleteBanner/<int:id>", methods = ['DELETE'])
@token_required
def delete_banner(current_user,id):
    banner = Banner.query.filter_by(id = id).one()
    db.session.delete(banner)
    db.session.commit()
    return jsonify(
    status = 'success',
    message = 'banner deleted'
    )

@app.route("/updateBanner", methods = ['PUT'])
@token_required
def update_banner(current_user):
    body = request.get_json()
    banners_id = body['banners_id']
    banners = Banner.query.all()
    Banner.query.update({Banner.isActive: False})
    db.session.commit()
    for id in banners_id:
        banner = Banner.query.get(id)
        banner.isActive = True
        db.session.commit()
    return jsonify(
    status = 'success',
    message = 'banner updated'
    )

@app.route("/addBanner", methods = ['POST'])
@token_required
def insert_banner(current_user):
    try:
        body = json.loads(request.form['data'])
        files = request.files.getlist('file')
        files[0].save(os.path.join(app.config['UPLOAD_FOLDER'], files[0].filename))
        photo = request.host_url+"filename/"+files[0].filename
        db.session.add(Banner(photo,body['title'], body['isActive']))
        db.session.commit()
        return jsonify(
        status = 'success',
        message = 'banner created'
        )
    except Exception as e:
        return jsonify(
        error  = str(e)
        )


#Gallerry routes
@app.route('/getGallery', methods=['GET'])
def get_gallery():
    galleries = Gallery.query.order_by(Gallery.id.asc()).all()
    return jsonify(gallery_schema.dump(galleries))

@app.route('/getGalleryTrue', methods=['GET'])
def get_galleriesTrue():
    galleries = Gallery.query.filter_by(isActive = True)
    return jsonify(gallery_schema.dump(galleries))

@app.route("/deleteGallery/<int:id>", methods = ['DELETE'])
@token_required
def delete_Gallery(current_user,id):
    gallery = Gallery.query.filter_by(id = id).one()
    db.session.delete(gallery)
    db.session.commit()
    return jsonify(
    status = 'success',
    message = 'gallery deleted'
    )

@app.route("/updateGallery", methods = ['PUT'])
@token_required
def update_gallery(current_user):
    body = request.get_json()
    galleries_id = body['galleries_id']
    galleries = Gallery.query.all()
    Gallery.query.update({Gallery.isActive: False})
    db.session.commit()
    for id in galleries_id:
        gallery = Gallery.query.get(id)
        gallery.isActive = True
        db.session.commit()
    return jsonify(
    status = 'success',
    message = 'gallery updated'
    )

@app.route("/addGallery", methods = ['POST'])
@token_required
def insert_gallery(current_user):
    body = json.loads(request.form['data'])
    files = request.files.getlist('file')
    photos = []

    for file in files:
        photo = request.host_url+"filename/"+file.filename
        photos.append(photo)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    gallery = Gallery(
        photos,
        body['title'],
        body['isActive']
        )
    db.session.add(gallery)
    db.session.commit()
    return jsonify(
    status = 'success',
    message = 'gallery created'
    )

#Dress routes
@app.route('/getDressesBestSeller', methods=['GET'])
def get_dresses_bestseller_true():
    dresses = Dress.query.filter_by(isBestSeller = True)
    return jsonify(dress_schemas.dump(dresses))

@app.route('/getDressesCollection', methods=['GET'])
def get_dresses_collection_true():
    dresses = Dress.query.filter_by(isCollection = True)
    return jsonify(dress_schemas.dump(dresses))

@app.route("/getDresses", methods = ['GET'])
def get_dresses():
    dresses = Dress.query.all()
    return jsonify(dress_schemas.dump(dresses))


@app.route("/getDress/<int:id>", methods = ['GET'])
def get_dress(id):
    dress = Dress.query.get(id)
    return jsonify(dress_schema.dump(dress))

@app.route("/deleteDress/<int:id>", methods = ['DELETE'])
@token_required
def delete_dress(current_user,id):
    dress = Dress.query.filter_by(id = id).one()
    db.session.delete(dress)
    db.session.commit()
    return jsonify(
    status = 'success',
    message = 'dress deleted'
    )

@app.route("/deleteDressCategories/<int:id>", methods = ['DELETE'])
@token_required
def delete_dress_categories(current_user,id):
    body = request.get_json()
    dress = Dress.query.get(id)
    categories_id = body['categories_id']
    for category_id in categories_id:
        category = Category.query.get(category_id)
        dress.categories.remove(category)
    db.session.commit()
    return jsonify(
    status = 'success',
    message = 'categories of dress deleted'
    )

@app.route("/extendDressCategories/<int:id>", methods = ['PUT'])
@token_required
def extend_dress_categories(current_user,id):
    body = request.get_json()
    dress = Dress.query.get(id)
    categories_id = body['categories_id']
    for category_id in categories_id:
        category = Category.query.get(category_id)
        dress.categories.append(category)
    db.session.commit()
    return jsonify(
    status = 'success',
    message = 'categories of dress extended'
    )

@app.route("/updateDressCollection", methods = ['PUT'])
@token_required
def update_dress_collection(current_user):
    body = request.get_json()
    dresses_ids = body['dresses_id']
    dresses = Dress.query.all()
    Dress.query.update({Dress.isCollection: False})
    db.session.commit()
    for id in dresses_ids:
        dress = Dress.query.get(id)
        dress.isCollection = True
        db.session.commit()
    return jsonify(
    status = 'success',
    message = 'dress updated'
    )

@app.route("/updateDressBestSeller", methods = ['PUT'])
@token_required
def update_dress_best_seller(current_user):
    body = request.get_json()
    dresses_ids = body['dresses_id']
    dresses = Dress.query.all()
    Dress.query.update({Dress.isBestSeller: False})
    db.session.commit()
    for id in dresses_ids:
        dress = Dress.query.get(id)
        dress.isBestSeller = True
        db.session.commit()
    return jsonify(
    status = 'success',
    message = 'dress updated'
    )

@app.route("/addDress", methods = ['POST'])
@token_required
def insert_dress(current_user):
    body = json.loads(request.form['data'])
    files = request.files.getlist('file')
    photos = []

    for file in files:
        photo = request.host_url+"filename/"+file.filename
        photos.append(photo)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    dress = Dress(
        photos,
        body['title'],body['title_uz'], body['description'],body['description_uz'],
        body['brand'],body['country'],
        body['size'],body['color'],body['color_uz'],
        body['price'],body['available'],
        body['isBestSeller'],body['isCollection']
        )
    categories_id = body['categories_id']
    for category_id in categories_id:
        category = Category.query.get(category_id)
        dress.categories.append(category)
    db.session.add(dress)
    db.session.commit()
    return jsonify(
    status = 'success',
    message = 'dress created'
    )