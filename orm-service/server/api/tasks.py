from server import c, create_app
from server import bucket
from server.api.models import Problem
import base64

@c.task()
def upload_image(problemId, imageString):
    blob = bucket.blob("Problem_" + str(problemId) + ".jpg")
    imageBytes = imageString.encode("utf-8")
    blob.upload_from_string(base64.b64decode(imageBytes), content_type="image/jpg")
    app = create_app('dev')
    with app.app_context():
        problem = Problem.query.get(problemId)
        problem.imageURL = blob.public_url
        problem.update()
        