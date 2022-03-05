from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import show_model

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least three characters.", "first_name")
            is_valid = False
        if (user['first_name']).isalpha() == False:
            flash("Name must only contain letters", "nameletters")
        if len(user['last_name']) < 3:
            flash("Last name must be at least three characters.", "last_name")
            is_valid = False
        if (user['last_name']).isalpha() == False:
            flash("Name must only contain letters", "nameletters")
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address", "email")
            is_valid = False
        if user['password'] != user['confirmpass']:
            flash('Password and Confirm Password did not match! Try again.', "passmatch")
            is_valid = False
        if len(user['password']) < 8:
            flash('Password requires at least 8 characters.', "passlength")
            is_valid = False
        return is_valid

# ********************CREATE********************

    @classmethod
    def register(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        flash('Successfully registered new account!', "newacct")
        return connectToMySQL('tv_shows').query_db(query, data)

# ********************READ**********************

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('tv_shows').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('tv_shows').query_db(query, data)
        return cls(result[0])
