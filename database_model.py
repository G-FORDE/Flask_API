class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	views = db.Column(db.Integer, nullable = False)
	like = db.Column(db.Integer, nullable = False)

	def __repr__(self):
		return f"video(name = {name} , views = {views}, likes = {likes})"

db.create_all() only once