from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model

class Show:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']

        self.creator_info = []

    @staticmethod
    def validate_show_info(show):
        is_valid = True
        if len(show['title']) < 3:
            flash("Show title must have at least three characters.", "title")
            is_valid = False
        if len(show['network']) < 3:
            flash("Network name must have at least three characters.", "network")
            is_valid = False
        if len(show['release_date']) < 1:
            flash("You must provide a release date for this TV Show.", "release_date")
            is_valid = False
        if len(show['description']) < 3:
            flash("Descriptions must be at least three characters long.", "description_tooshort")
            is_valid = False
        if len(show['description']) > 500:
            flash("Description character limit is 500 - dont' give too much of the plot away!", "description_toolong")
            is_valid = False
        return is_valid

# ********************CREATE********************

    @classmethod
    def add_show(cls, data):
        query = "INSERT INTO shows (title, network, release_date, description, created_at, updated_at, creator_id) VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, NOW(), NOW(), %(creator_id)s);"
        return connectToMySQL('tv_shows').query_db(query, data)

# ********************READ**********************

    @classmethod
    def view_all_shows(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL('tv_shows').query_db(query)
        show_list = []
        for row in results:
            show_list.append(cls(row))
        return show_list

    @classmethod
    def view_show_by_id(cls, data):
        query = "SELECT * FROM shows WHERE id = %(id)s;"
        results = connectToMySQL('tv_shows').query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def show_creator_by_id(cls, data):
        query = "SELECT * FROM shows LEFT JOIN users ON users.id = shows.creator_id WHERE shows.id = %(id)s;"
        results = connectToMySQL('tv_shows').query_db(query, data)
        creator = cls(results[0])
        for row in results:
            creator_info = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            creator.creator_info.append(user_model.User(creator_info))
        print(creator)
        return creator_info

    @classmethod
    def show_creators(cls):
        query = "SELECT * FROM shows LEFT JOIN users ON users.id = shows.creator_id;"
        results = connectToMySQL('tv_shows').query_db(query)
        creator = cls(results[0])
        for row in results:
            creator_info = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            creator.creator_info.append(user_model.User(creator_info))
        print("printing creator:")
        print(creator)
        return creator_info

# ********************UPDATE********************

    @classmethod
    def update(cls, data):
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s, updated_at = NOW() WHERE shows.id = %(id)s;"
        return connectToMySQL('tv_shows').query_db(query, data)

# ********************DELETE********************

    @classmethod
    def delete(cls, data):
        query = "SET SQL_SAFE_UPDATES = 0"
        query = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL('tv_shows').query_db(query, data)