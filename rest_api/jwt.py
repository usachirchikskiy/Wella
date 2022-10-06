import jwt
from flask import request, jsonify, current_app as app
from .models import User
from functools import wraps

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      token = None

      if 'x-access-tokens' in request.headers:
         token = request.headers['x-access-tokens']

      if not token:
         return jsonify({'message': 'a valid token is missing'})

      try:
         data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
         current_user = User.query.get(data['id'])
      except Exception as e:
         print(e)
         return jsonify({'message': 'token is invalid'})

      return f(current_user, *args, **kwargs)
   return decorator
