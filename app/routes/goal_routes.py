from flask import Blueprint, request, make_response, abort, Response
from app.models.goal import Goal
from ..db import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response({"message": f"Goal {goal_id} is invalid"}, 400))
    
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"message": f"Goal {goal_id} not found"}, 404))
    return goal

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    response = {"goal" : new_goal.goal_dict()}
    return response, 201

@goals_bp.get("")
def get_all_goals():
    goals = Goal.query.all()
    goals_response = [goal.goal_dict() for goal in goals]

    return make_response(goals_response, 200)

@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return {"goal": goal.goal_dict()}, 200

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    goal.title = request_body["title"]
    db.session.commit()

    return {"goal": goal.goal_dict()}, 200

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({
        "details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"
    }, 200)