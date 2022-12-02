import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def get_musics_by_user(user):

    try:
        print(f" c: {user}")
        return list(db.musics.find({},{"user" : 1}))

    except Exception as e:
        return e



def build_query_sort_project(filters):
    """
    Builds the `query` predicate, `sort` and `projection` attributes for a given
    filters dictionary.
    """
    query = {}
    # The field "tomatoes.viewer.numReviews" only exists in the musics we want
    # to display on the front page of MFlix, because they are famous or
    # aesthetically pleasing. When we sort on it, the musics containing this
    # field will be displayed at the top of the page.
    sort = [("tomatoes.viewer.numReviews", -1)]
    project = None
    if filters:
        if "text" in filters:
            query = {"$text": {"$search": filters["text"]}}
            meta_score = {"$meta": "textScore"}
            sort = [("score", meta_score)]
            project = {"score": meta_score}
        elif "cast" in filters:
            query = {"cast": {"$in": filters["cast"]}}
        elif "genres" in filters:

            """
            Ticket: Text and Subfield Search

            Given a genre in the "filters" object, construct a query that
            searches MongoDB for movies with that genre.
            """

            # TODO: Text and Subfield Search
            # Construct a query that will search for the chosen genre.
            query = {}

    return query, sort, project



def get_musics(filters, page, musics_per_page):
    """
    Returns a cursor to a list of movie documents.

    Based on the page number and the number of musics per page, the result may
    be skipped and limited.

    The `filters` from the API are passed to the `build_query_sort_project`
    method, which constructs a query, sort, and projection, and then that query
    is executed by this method (`get_musics`).

    Returns 2 elements in a tuple: (musics, total_num_musics)
    """
    query, sort, project = build_query_sort_project(filters)
    if project:
        cursor = db.musics.find(query, project).sort(sort)
    else:
        cursor = db.musics.find(query).sort(sort)

    total_num_musics = 0
    if page == 0:
        total_num_musics = db.musics.count_documents(query)
 
    musics = cursor.limit(musics_per_page)

    return (list(musics), total_num_musics)


def get_musics(id):
    """
    Given a movie ID, return a movie with that ID, with the comments for that
    movie embedded in the movie document. The comments are joined from the
    comments collection using expressive $lookup.
    """
    try:

        pipeline = [
            {
                "$match": {
                    "_id": ObjectId(id)
                }
            }
        ]

        movie = db.musics.aggregate(pipeline).next()
        return movie

    # TODO: Error Handling
    # If an invalid ID is passed to `get_movie`, it should return None.
    except (StopIteration) as _:

        return None

    except Exception as e:
        return {}


def get_all_genres():
    """
    Returns list of all genres in the database.
    """
    return list(db.musics.aggregate([
        {"$unwind": "$genres"},
        {"$group": {"_id": None, "genres": {"$addToSet": "$genres"}}}
    ]))[0]["genres"]

