from flask import Flask, render_template, Response
from flask_restful import Resource, reqparse, Api
from camera import Camera
from base import Movies, db
from movies import MoviesList

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


db.init_app(app)
app.app_context().push()
db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/home')
def home():
	return render_template('test_camera.html')

class AllMovies(Resource):

    def get(self):
        return {'Movies': list(map(lambda x: x.json(), Movies.query.all()))}


api.add_resource(AllMovies, '/movies')
api.add_resource(MoviesList, '/<string:movie>')

if __name__ == '__main__':

    app.run(debug=True)
