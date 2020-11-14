from flask import Flask, request, Response, jsonify
from . import problem
from server.api.models import Problem
import json, base64
from server.api.tasks import upload_image
from sqlalchemy import exc


            
@problem.route("/Problem", methods=["POST"])
def create_problem():
    image = request.files["image"] 
    data = request.files["data"]
    problemData = json.loads(data.read().decode("utf-8"))
    print(problemData)
    problem = Problem(problemData)
    if problem.insert():
        string = base64.b64encode(image.read())
        upload_image.delay(problem.id, string.decode("utf-8"))
        return Response(status=201)
    return Response(response="Error: Failed to report problem", status=400)



@problem.route("/Problem/<int:houseId>")
def get_problems_by_house_id(houseId):
    try:
        problems = Problem.query.filter(Problem.houseId == houseId).all()
        print([problem.toJson() for problem in problems])

        return jsonify([problem.toJson() for problem in problems])
    except exc.OperationalError:
        return jsonify([])

@problem.route("Homeowner/Problem/<int:problemId>", methods=["PUT"])
def update_problem(problemId):
    problemData = request.get_json()
    problem = Problem.query.get(problemId)
    problem.status = problemData["status"]
    problem.lastUpdated = problemData["lastUpdated"]
    if problem.update():
        print(problem.toJson())
        return Response(status=201)

    return Response(response="Error: Failed to update problem", status=400)

