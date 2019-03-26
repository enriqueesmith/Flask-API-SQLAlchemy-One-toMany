import os, copy
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Course, Member

app = Flask(__name__)
##Setting the place for the db to run
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/change_this_name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing the db (after registering the Models)
db.init_app(app)
#migration engine
migrate = Migrate(app, db)


def getElem(a):
    for i in Course["id"]:
        if a == i["id"]:
            return i
            
def getElement(a):
    for i in Member["id"]:
        if a == i["id"]:
            return i

@app.route('/')
def hello():
    members = Member.query.all()
    responseA =[]
    for m in members:
        responseA.append(m.to_dict())
    courses = Course.query.all()
    responseB =[]
    for c in courses:
        responseB.append(c.to_dict())
        
    return jsonify(responseA, responseB)
    
# Add a Course     - /courses/add  -  POST    
@app.route('/courses/add', methods=['POST'])
def addCourses():
    info = request.get_json() or {}
    course = Course(name=info['name'])
    db.session.add(course)
    db.session.commit()
    return jsonify({'response': 'Ok'}) 
    
    
# Add a Student (with a Course)  - /students/add  -  POST
@app.route('/students/add', methods=['POST'])
def addStudents():
    info = request.get_json() or {}
    member = Member(first_name=info['first_name'], last_name=info['last_name'], age=info['age'], course_id=info['course_id'])
    db.session.add(member)
    db.session.commit()
    return jsonify({'response': 'Ok'}) 
    
# List all Courses   - /courses  - GET    
@app.route('/courses', methods=['GET'])
def showCourses():
    courses = Course.query.all()
    response = []
    for c in courses:
        course = c.to_dict()
        response.append(course)
    
    return jsonify({"data": response})
    
# [GET] /courses/:int - Show a specific Course, including the list of Students.
@app.route('/courses/<int:id>', methods=['GET'])
def getCoursewithStudents(id):
    ele = Course.query.get(id)
    cour = ele.to_dict()
    if id > 0:
            
        return jsonify({"status_code": 200, "data": cour})
        
    
    response = jsonify({"error": 400, "message":"no member found" })
    response.status_code = 400
    return response

    
    
# List all Students  - /students  - GET
@app.route('/students', methods=['GET'])
def showStudents():
    members = Member.query.all()
    response =[]
    for m in members:
        member = m.to_dict()
        response.append(member)
        
    return jsonify({"data": response})


    


# [GET] /students/:int - Show a specific Student, including the Course information (object)
@app.route('/students/<int:id>', methods=['GET', 'PUT'])
def getStudentwithCourses(id):
    if request.method == 'GET':
        
        ele = Member.query.get(id)
        stud = ele.to_dict()
        if id > 0:
                
            return jsonify({"status_code": 200, "data": stud})
                
        response = jsonify({"error": 400, "message":"no member found" })
        response.status_code = 400
        return response    
    
# [PUT] /students/:int - Change a specific Student to a different Course    
    else:
        
        info = request.get_json() or {}
        ele = Member.query.get(id)
        ele.course_id = info['course_id']
        db.session.commit()
        
        
        return jsonify({"status_code": 200, "data": ele.to_dict()})
    
    response = jsonify({"error": 400, "message":"no member found" })
    response.status_code = 400
    return response





  
  
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))