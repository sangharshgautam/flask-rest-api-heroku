from flask import Flask, request, send_from_directory, render_template, send_file
from flask_restful import Resource, reqparse, Api
from flask_cors import CORS, cross_origin

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, template_folder="templates")
api = Api(app)
cors = CORS(application, resources={r"/uploader": {"origins": "*"}})
app.config['UPLOAD_FOLDER'] = 'static'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

from base import Movies, db
db.init_app(app)
app.app_context().push()
db.create_all()

@app.route('/upload')
def upload_html():
	return render_template('upload.html')
		
class Movies_List(Resource):
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
    
class All_Movies(Resource):
    def get(self):
        return {'Movies': list(map(lambda x: x.json(), Movies.query.all()))}

api.add_resource(All_Movies, '/movies')
api.add_resource(Movies_List, '/<string:movie>')

if __name__=='__main__':
    
    app.run(debug=True)
