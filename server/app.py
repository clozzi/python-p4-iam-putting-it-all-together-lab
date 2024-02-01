#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):

    def post(self):

        user = User(
            username = request.get_json()['username'],
            image_url = request.get_json()['image_url'],
            bio = request.get_json()['bio']
        )
        user.password_hash = request.get_json()['password']

        try:

            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id
            
            return user.to_dict(), 201
        
        except IntegrityError:
            return {'error': '422 Unprocessable Entity'}, 422

class CheckSession(Resource):
    
    def get(self):
        user_id = session['user_id']
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict(), 200
        else: 
            return {}, 401

class Login(Resource):
    
    def post(self):

        username = request.get_json()['username']
        password = request.get_json()['password']
        user = User.query.filter(User.username == username).first()

        if user:
            if user.authenticate(password):
                session['user_id'] = user.id
                return user.to_dict(), 200
    
        return {'error': '401 Unauthorized'}, 401


class Logout(Resource):
    
    def delete(self):
        
        # if session['user_id']:
        #     session['user_id'] = None
        #     return {'message': '204: No Content'}, 204
        # return {'message': '401 Unauthorized'}, 401

        session['user_id'] = None
        return {}, 204

class RecipeIndex(Resource):
    pass

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)