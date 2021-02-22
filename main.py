from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
#initialize the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	views = db.Column(db.Integer, nullable = False)
	like = db.Column(db.Integer, nullable = False)

	def __repr__(self):
		return f"video(name = {name} , views = {views}, likes = {likes})"

class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Video(name = {name}, views = {views}, likes = {likes})"
#create new RequestParser object
video_put_args = reqparse.RequestParser()
#describe the manditory keys and error messages
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

#the return value from the video resource below, is serialized with these fields
resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}

#get request for all information that contans the video_id
class Video(Resource):
	@marshal_with(resource_fields) 
		#querries the dataase for the video id
	def get(self, video_id):
		result = VideoModel.query.filter_by(id=video_id).first()
		#calls abort() method
		if not result:
			abort(404, message="Could not find video with that id")
		return result

	@marshal_with(resource_fields)
	def put(self, video_id):
		#takes the arguments from the request
		args = video_put_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		#calls abort() if video with that id already exists
		if result:
			abort(409, message="Video id taken...")

		video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
		#temporarily adds the video to the db
		db.session.add(video)
		#permenantly adds the video to the db
		db.session.commit()
		#tells the sender that the video has been created
		return video, 201

	#the sender can update videos		
	@marshal_with(resource_fields)
	def patch(self, video_id):
		args = video_update_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Video doesn't exist, cannot update")

		if args['name']:
			result.name = args['name']
		if args['views']:
			result.views = args['views']
		if args['likes']:
			result.likes = args['likes']
		#commits changes to the db
		db.session.commit()

		return result

	#deletes the video or aborts if the id doesn't exist
	def delete(self, video_id):
		abort_if_video_id_doesnt_exist(video_id)
		del videos[video_id]
		return '', 204


#resource for video_id
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
	app.run(debug=True)