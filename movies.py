from base import Movies, db
from flask_restful import Resource, reqparse, Api

class MoviesList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('director', type=str, required=False, help='Director of the movie')
    parser.add_argument('genre', type=str, required=False, help='Genre of the movie')
    parser.add_argument('collection', type=int, required=True, help='Gross collection of the movie')

    def get(self, movie):
        item = Movies.find_by_title(movie)
        if item:
            return item.json()
        return {'Message': 'Movie is not found'}

    def post(self, movie):
        if Movies.find_by_title(movie):
            return {' Message': 'Movie with the  title {} already exists'.format(movie)}
        args = Movies_List.parser.parse_args()
        item = Movies(movie, args['director'], args['genre'], args['collection'])
        item.save_to()
        return item.json()

    def put(self, movie):
        args = Movies_List.parser.parse_args()
        item = Movies.find_by_title(movie)
        if item:
            item.collection = args['collection']
            item.save_to()
            return {'Movie': item.json()}
        item = Movies(movie, args['director'], args['genre'], args['collection'])
        item.save_to()
        return item.json()

    def delete(self, movie):
        item  = Movies.find_by_title(movie)
        if item:
            item.delete_()
            return {'Message': '{} has been deleted from records'.format(movie)}
        return {'Message': '{} is already not on the list'.format()}
