from flask import Flask, request, Response, jsonify
from . import problem
from server.api.models import Problem
import json, base64
from server.api.tasks import upload_image
from sqlalchemy import exc
import logging

            
@problem.route("/Problem", methods=["POST"])
def create_problem():
    image = request.files["image"] 
    data = request.files["data"]
    problemData = json.loads(data.read().decode("utf-8"))
    problem = Problem(problemData)
    if problem.insert():
        string = base64.b64encode(image.read())
        upload_image.delay(problem.id, string.decode("utf-8"))
        return Response(status=201)
    return Response(response="Error: Failed to report problem", status=400)



@problem.route("/House/<int:houseId>/Problem")
def get_problems_by_house_id(houseId):
    try:
        problems = Problem.query.filter(Problem.houseId == houseId).all()
        return jsonify([problem.toJson() for problem in problems])
    except exc.OperationalError:
        return jsonify([])


@problem.route("Problem/<int:problemId>/Status", methods=["PUT"])
def update_problem(problemId):
    problemData = request.get_json()
    problem = Problem.query.get(problemId)
    problem.status = problemData["status"]
    problem.lastUpdated = problemData["lastUpdated"]
    if problem.update():
        return Response(status=200)
    return Response(response="Error: Failed to update problem", status=400)

@problem.route("Problem/<int:problemId>")
def get_problem(problemId):
    problem = Problem.query.get(problemId)
    if problem:
        return jsonify(problem.toJson())
    return Response(response="Error: Problem not found", status=404)