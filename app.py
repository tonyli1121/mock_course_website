# Import
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, select

# create application object
app = Flask(__name__)

app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'

# create object for database
db = SQLAlchemy(app)

global glo_id
glo_id = "nonono"

############## Init tables for db.create_all() / other db calls #################################
# regrade table
class Regrade(db.Model):

	grade_id = db.Column(db.Integer, primary_key = True)
	student_id = db.Column(db.Text, nullable = False)
	instructor_id = db.Column(db.Text, nullable = False)
	reason = db.Column(db.Text, nullable = False)


	def __repr__(self):
		return f"('{self.grade_id}', '{self.student_id}', '{self.reason}')"


# Users table
class User(db.Model):

	user_id = db.Column(db.Text, primary_key = True)
	name = db.Column(db.Text, nullable = False)
	password = db.Column(db.Text, nullable = False)
	email = db.Column(db.Text, nullable = False)
	isInstructor = db.Column(db.Integer, nullable = False)

	def __repr__(self):
		return f"('{self.user_id}', '{self.name}', '{self.password}', '{self.isInstructor}')"

# Feedback table
class Feedback(db.Model):

	feedback_id = db.Column(db.Integer, primary_key = True)
	answer1 = db.Column(db.Text)
	answer2 = db.Column(db.Text)
	answer3 = db.Column(db.Text)
	answer4 = db.Column(db.Text)
	instructor_id = db.Column(db.Text, nullable = False)

	def __repr__(self):
		return f"('{self.instructor_id}', '{self.answer1}', '{self.answer2}', '{self.answer3}', '{self.answer4}')"

# Grades table
class Grades(db.Model):

	grade_id = db.Column(db.Integer, primary_key = True)
	student_id = db.Column(db.Text, nullable = False)
	course_id = db.Column(db.Text, nullable = False)
	full_score = db.Column(db.Integer, nullable = False)
	grade = db.Column(db.Integer, nullable = False)
	test_name = db.Column(db.Text, nullable = False)
	markder = db.Column(db.Text, nullable = False) #instructor_id

	def __repr__(self):
		return f"('{self.student_id}', '{self.course_id}', '{self.test_name}', '{self.grade}')"

##############################################################################################################

#use decorator to link function to url 
# route for default homepage
@app.route("/")
@app.route("/index.html")
def index():
	return render_template("index.html")

# route for sign in
@app.route("/sign_in.html", methods = ['GET','POST'])
@app.route("/sign_in", methods = ['GET','POST'])
def sign_in():
	if request.method == 'POST':
		# get the key values

		id = request.form.get('id')
		password = request.form.get('password')

		#check if the user with this id exist
		user = User.query.filter_by(user_id = id, password = password).first()

		if user:

			#check if he/she is an instructor
			
			is_ins = User.query.filter_by(user_id = id, password = password, isInstructor = 1).first()
			global glo_id
			glo_id = id
			if is_ins:
				return redirect(url_for('instructor_index'))
			else:
				return redirect(url_for('student_index'))
				

		#does not exist --> try again
		else:
			flash(password)
			return redirect(url_for('sign_in'))

	return render_template("sign_in.html")


# route for register
@app.route("/register.html", methods = ['GET','POST'])
@app.route("/register", methods = ['GET','POST'])
def register():
	if request.method == 'POST':
		# get the key values
		name = request.form.get('name')
		id = request.form.get('id')
		type = request.form.get('type')
		email = request.form.get('email')
		password = request.form.get('password')

		# if password is not the same as repeated one
		if (request.form.get('password-repeat')!= password):
			flash("diff password entered")
			return redirect(url_for('register'))

		# check if the user_id is registered
		user = User.query.filter_by(user_id = id).first()

		# pre existing id --> pop up error msg
		if user:
			flash('id already registered')
			return redirect(url_for('register'))

		# otherwise insert into databse
		else:
			user = User(user_id = id, name = name, password = password, email = email, isInstructor = type)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('sign_in'))

	return render_template("register.html")
	
dummy = [[0,10012,"CSCB20",100,30,"Jan 23","Quiz1","prof Mike"],
    [1,10086,"CSCB20",100,0,"Jan 23", "Quiz2","prof John"],
    [2,110,"CSCB20",100,100,"Jan 23","Quiz200","prof Jack"]]

feedbacks = [[0,"a","a2","a3","a4","Jan 23",2001,"CSCB20"],
    [1,"b","b2","b3","b4","Jan 24", 2001,"CSCB20"],
    [2,"c","c2","c3","c4","Jan 25",2001,"CSCB20"]]

regrades = [[0,1001,2001,"badbad","CSCB20","Quiz1","Jan 23"],
    [1,1001,2001,"me 100%","CSCB20","Quiz2","Jan 23"],
    [2,1001,2001,"4.0 please","CSCB20","Quiz3","Jan 23"]]

@app.route("/student_grades", methods=['GET', 'POST'])
@app.route("/student_grades.html", methods=['GET', 'POST'])
def student_grades():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	grades = []
	if request.method == 'POST':
		# get the key values
		reason = request.form.get('reason')
		grade_id = request.form.get('grade_id')
		instructor_id = request.form.get('instructor_id')

		if(db.session.query(db.exists().where(Regrade.grade_id == grade_id)).scalar()):
			flash("A regrade request already exists for this entry.")
		else:
			regd = Regrade(grade_id=grade_id, student_id=glo_id, instructor_id=instructor_id, reason=reason)
			db.session.add(regd)
			db.session.commit()

	for u in Grades.query.all():
		tmp_dict = u.__dict__
		if (tmp_dict['student_id'] == glo_id):
			temp = []
			temp.append(tmp_dict['grade_id'])
			temp.append(tmp_dict['student_id'])
			temp.append(tmp_dict['course_id'])
			temp.append(tmp_dict['full_score'])
			temp.append(tmp_dict['grade'])
			temp.append(tmp_dict['test_name'])
			temp.append(tmp_dict['markder'])
			grades.append(temp)

	return render_template("student_grades.html", grades_num=len(grades), grades=grades)

@app.route("/instructor_grade", methods=['GET', 'POST'])
@app.route("/instructor_grade.html", methods=['GET', 'POST'])
def instructor_grades():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	grades = []
	if request.method == 'POST':
		# get the key values
		student_id = request.form.get('student')
		course_id = request.form.get('course')
		grade_title = request.form.get('title')
		grade_full = request.form.get('full')
		grade_score = request.form.get('grade')

		student = User.query.filter_by(user_id=student_id, isInstructor=False).first()
		next_id = Grades.query.order_by(Grades.grade_id.desc()).first()
		if (next_id):
			next_id = next_id.grade_id + 1
		else:
			next_id = 0

		if (student):
			gd = Grades(grade_id=next_id, student_id=student_id, course_id=course_id, full_score=grade_full, grade=grade_score, test_name=grade_title, markder=glo_id)
			db.session.add(gd)
			db.session.commit()
		else:
			flash("Student not found")


	for u in Grades.query.all():
		tmp_dict = u.__dict__
		temp = []
		temp.append(tmp_dict['grade_id'])
		temp.append(tmp_dict['student_id'])
		temp.append(tmp_dict['course_id'])
		temp.append(tmp_dict['full_score'])
		temp.append(tmp_dict['grade'])
		temp.append(tmp_dict['test_name'])
		temp.append(tmp_dict['markder'])
		grades.append(temp)

	return render_template("instructor_grade.html", grades_num=len(grades), grades=grades)

@app.route("/instructor_feedback")
@app.route("/instructor_feedback.html")
def instructor_feedbacks():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	feedbacks = []
	for u in Feedback.query.all():
		tmp_dict = u.__dict__
		temp = []
		temp.append(tmp_dict['feedback_id'])
		temp.append(tmp_dict['answer1'])
		temp.append(tmp_dict['answer2'])
		temp.append(tmp_dict['answer3'])
		temp.append(tmp_dict['answer4'])
		temp.append(tmp_dict['instructor_id'])
		feedbacks.append(temp)

	return render_template("instructor_feedback.html", feedbacks_num=len(feedbacks), feedbacks=feedbacks)

@app.route("/instructor_regrade_requests")
@app.route("/instructor_regrade_requests.html")
def instructor_regrades():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	# joining regrade and grades table
	q = db.session.query(Regrade, Grades).filter(Regrade.grade_id == Grades.grade_id).all()
	regrades = []
	for u in q:
		tmp_dict = u[0].__dict__
		temp = []
		temp.append(tmp_dict['grade_id'])
		temp.append(tmp_dict['student_id'])
		temp.append(tmp_dict['instructor_id'])
		temp.append(tmp_dict['reason'])
		tmp_dict = u[1].__dict__
		temp.append(tmp_dict['course_id'])
		temp.append(tmp_dict['test_name'])
		regrades.append(temp)
	return render_template("instructor_regrade_requests.html", regrades_num=len(regrades), regrades=regrades)



# route for instructor_index
@app.route("/instructor_index.html")
@app.route("/instructor_index")
def instructor_index():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	return render_template('instructor_index.html')




# route for student_index
@app.route("/student_index.html")
@app.route("/student_index")
def student_index():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	return render_template('student_index.html')


# route for student_feedback
@app.route("/student_feedback.html", methods=['GET', 'POST'])
@app.route("/student_feedback", methods=['GET', 'POST'])
def student_feedback():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	if request.method == 'POST':
		# get the key values
		ins_id = request.form.get('instructor_id')
		ans1 = request.form.get('fb1')
		ans2 = request.form.get('fb2')
		ans3 = request.form.get('fb3')
		ans4 = request.form.get('fb4')

		instructor = User.query.filter_by(user_id=ins_id, isInstructor=True).first()
		next_id = Feedback.query.order_by(Feedback.feedback_id.desc()).first()
		if(next_id):
		 	next_id = next_id.feedback_id + 1
		else:
			next_id = 0

		if (instructor):
			fb = Feedback(feedback_id = next_id, answer1 = ans1, answer2 = ans2, answer3 = ans3, answer4 = ans4, instructor_id = ins_id)
			db.session.add(fb)
			db.session.commit()
			return redirect(url_for('student_index'))
		else:
			flash("Instructor not found")
	return render_template("student_feedback.html")


# route for student_lecture
@app.route("/student_lecture.html")
@app.route("/student_lecture")
def student_lecture():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	return render_template('student_lecture.html')


# route for student_news
@app.route("/student_news.html")
@app.route("/student_news")
def student_news():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	return render_template('student_news.html')


# route for student_resources
@app.route("/student_resources.html")
@app.route("/student_resources")
def student_resources():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	return render_template('student_resources.html')

# route for student_coursework
@app.route("/student_courseworks.html")
@app.route("/student_courseworks")
def student_courseworks():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	return render_template('student_courseworks.html')

# route for student_lecture
@app.route("/instructor_lecture.html")
@app.route("/instructor_lecture")
def instructor_lecture():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	return render_template('instructor_lecture.html')


# route for instructor_news
@app.route("/instructor_news.html")
@app.route("/instructor_news")
def instructor_news():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	return render_template('instructor_news.html')


# route for instructor_resources
@app.route("/instructor_resources.html")
@app.route("/instructor_resources")
def instructor_resources():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	return render_template('instructor_resources.html')

# route for instructor_coursework
@app.route("/instructor_courseworks.html")
@app.route("/instructor_courseworks")
def instructor_courseworks():
	if glo_id == "nonono":
		return redirect(url_for('sign_in'))
	return render_template('instructor_courseworks.html')

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)