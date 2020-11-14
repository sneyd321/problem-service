from server import db
from sqlalchemy.exc import IntegrityError, OperationalError


class Problem(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(25))
    description = db.Column(db.String(140))
    imageURL = db.Column(db.String(223), nullable=True)
    status = db.Column(db.String(15))
    datePosted = db.Column(db.String(20))
    lastUpdated = db.Column(db.String(20))
    houseId = db.Column(db.Integer())

    def __init__(self, problemData):
        self.category = problemData["category"]
        self.description = problemData["description"]
        self.datePosted = problemData["datePosted"]
        self.lastUpdated = problemData["lastUpdated"]
        self.status = problemData["status"]
        self.houseId = problemData["houseId"]

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

    def toDict(self):
        return {
            Problem.category: self.category,
            Problem.description: self.description,
            Problem.imageURL: self.imageURL,
            Problem.status: self.status,
            Problem.datePosted: self.datePosted,
            Problem.lastUpdated: self.lastUpdated
        }

    def toJson(self):
        return {
            "problemId": self.id,
            "category": self.category,
            "description": self.description,
            "imageUrl": self.imageURL,
            "status": self.status,
            "datePosted": self.datePosted,
            "lastUpdated": self.lastUpdated,
            "houseId": self.houseId
        }


    def update(self):
        rows = Problem.query.filter(Problem.id == self.id).update(self.toDict(), synchronize_session=False)
        print(self.toJson())
        if rows == 1:
            try:
                db.session.commit()
                return True
            except OperationalError:
                db.session.rollback()
                return False
        return False

    def __repr__(self):
        return "< Problem: " + self.category + ": " + self.description + " >"
