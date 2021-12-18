from flask import Flask, request, Response, jsonify
from . import problem
from server.api.models import Problem
import json, base64, requests
from sqlalchemy import exc
from server.api.RequestManager import Zookeeper, RequestManager

zookeeper = Zookeeper()



            
@problem.route("/Problem", methods=["POST"])
def create_problem():
    if not request.files or "data" not in request.files or "image" not in request.files:
        return Response(response="Error: Invalid key entry", status=400)

    data = request.files["data"]
    problemData = json.loads(data.read().decode("utf-8"))
    
    problem = Problem(problemData)
    if problem.insert():
        service = zookeeper.get_service("image-upload-service")
        if not service:
            return Response(response="Error: Upload Service Currently Unavailable", status=503)

        manager = RequestManager(request, service)
        manager.post_problem(problem.id)
        return jsonify(problem.toJson())
        

    return Response(response="Error: Failed to report problem", status=400)

    



@problem.route("Problem/<int:problemId>/imageURL", methods=["PUT"])
def update_imageURL(problemId):
    problemData = request.get_json()
    if not problemData or "imageURL" not in problemData:
        return Response(response="Error: Invalid Request", status=400)
    problem = Problem.query.get(problemId)
    problem.imageURL = problemData["imageURL"]
    if problem.update():
        return Response(status=200)
    return Response(response="Error: Failed to update problem", status=400)

      

@problem.route("/House/<int:houseId>/Problem")
def get_problems_by_house_id(houseId):
    problems = Problem.query.filter(Problem.houseId == houseId).all()
    return jsonify([problem.toJson() for problem in problems])



@problem.route("Problem/<int:problemId>/Status", methods=["PUT"])
def update_problem(problemId):
    problemData = request.get_json()
    if not problemData or "status" not in problemData or "lastUpdated" not in problemData:
        return Response(response="Error: Invalid Request", status=400)
    problem = Problem.query.get(problemId)
    if problem:
        problem.status = problemData["status"]
        problem.lastUpdated = problemData["lastUpdated"]
        if problem.update():
            return jsonify(problem.toJson())
        return Response(response="Error: Failed to update problem", status=409)
    return Response(response="Error: Problem not found", status=404)

@problem.route("Problem/<int:problemId>")
def get_problem(problemId):
    problem = Problem.query.get(problemId)
    if problem:
        return jsonify(problem.toJson())
    return Response(response="Error: Problem not found", status=404)