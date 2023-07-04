from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flask import session
from flask import current_app
from flask import jsonify
import datetime
import re
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from myproject.auth import login_required
from myproject.db import get_db

bp = Blueprint("stmt", __name__, url_prefix='/')

#################################################
# test pages
#################################################
@bp.route("/test/test", methods=('GET', 'POST'))
def test():
    """test page
        This is for test purpose only.

    Returns:
        list: flask will take the list or dict and turns to jason automatically.
    """
    cur = get_db().cursor()
    cur.execute(
        "SELECT * FROM tb_test"
    )
    test_list = []
    
    datasets = cur.fetchall()
    for row in datasets:
        temp_list = []
        for r in row:
            temp_list.append(r)
        test_list.append(temp_list)
    
    return {"tb_test": datasets}, 200
    # return "Hello 你好！", 200 # return string

#################################################
# Login page
#################################################
@bp.route("/")
@login_required
def index():
    """ Show the main page """
    cur = get_db().cursor()
    
    # total students
    cur.execute("select count(*) from tb_student")
    stu_num = cur.fetchone()
    session["stu_num"] = stu_num['count(*)']

    # total courses
    cur.execute("select count(*) from tb_course")
    stu_num = cur.fetchone()
    session["course_num"] = stu_num['count(*)']
    
    # total students
    cur.execute("select count(*) from tb_teacher")
    stu_num = cur.fetchone()
    session["tea_num"] = stu_num['count(*)']
    
    # user priveledge
    user_id = session["user_id"]
    cur.execute("select user_type from tb_user where user_id = %s", (user_id,))
    user_type = cur.fetchone()
    session["user_type"] = user_type["user_type"]
    
    # totally online users
    onlineUsers = current_app.onlineUsers
    
    # top 5 scores
    cur.execute( "select sc.id as id, sc.score as score, st.student_no as student_no,"
                " st.student_name as student_name, co.course_no as course_no, co.course_name as course_name"
                " from tb_score sc, tb_student st, tb_course co where sc.course_no = co.course_no and sc.student_no = st.student_no"
                " order by sc.score desc limit 10" )
    topScores = cur.fetchall()
    
    return render_template("stmt/main.html", topScores=topScores, onlineUsers=onlineUsers)

#################################################
# introduction view
#################################################

@bp.route("/introduction")
@login_required
def introduction():
    """introduction page

    Returns:
        template: introduction template
    """
    return render_template("stmt/introduction.html")

#################################################
# admin views
#################################################
# global dict for all table columns
tables = {
            'student': ['student_no', 'student_name', 'gender', 'age', 'year'],
            'teacher': ['teacher_no', 'teacher_name', 'gender'],
            'user': ['user_id', 'username', 'user_type', 'student_no', 'status'],
            }
 
@bp.route("/admin/list/<any(course, login_history, score, student, teacher, test, user):list_object>", methods=("GET", "POST"))
@login_required
def list_objects(list_object):
    """common API to return all table lines
        response to: http://127.0.0.1:5000/admin/list/students?draw=1&columns%5B0%5D%5Bdata%5D=&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc&start=0&length=20&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1687966300099

    Returns:
        objects: all list from a table
    """
    table = 'tb_' + list_object
    
    # arguments
    # post
    if request.method == "POST":
        draw = request.values.get('draw')
        start = request.values.get('start')
        length = request.values.get('length')
        searchValue = request.values.get('search[value]')
        order_col = request.values.get("order[0][column]")
        order_direction = request.values.get("order[0][dir]")
    # get
    if request.method == "GET":
        draw = request.args.get('draw') 
        start = request.args.get('start') 
        length = request.args.get('length') 
        searchValue = request.args.get('search[value]') 
        order_col = request.values.get("order[0][column]")
        order_direction = request.values.get("order[0][dir]")
    print("draw: " + draw)
    print("start: " + start)
    print("length: " + length)
    print("searchValue: " + searchValue)
    print("order_col: " + order_col)   # colum number
    print("order_direction: " + order_direction)  # desc or asc
    # SELECT storename, cn, ip, changedate, expiredate, status from tunovpnclients 
    # WHERE (storename LIKE ? OR cn LIKE ? or ip LIKE ?) 
    # ORDER BY status desc 
    # LIMIT ? OFFSET ?
    query = None

    # prepare sql for tb_student
    # cursor.execute("SELECT * FROM test WHERE text LIKE %s", f"%{param}%") # sql prepare

    columns = tables[list_object]
    query = "SELECT * FROM {}".format(table)
    total_sql = "SELECT count(*) FROM {}".format(table)
    if searchValue:
        query += " WHERE "
        flag = 0 # notify wether OR if needed
        for col in columns:
            if flag:
                query += "OR " + col + " LIKE %s "
            else:
                query += col + " LIKE %s "
                flag += 1
    query += " ORDER BY {0} {1}".format(columns[ int(order_col) - 1 ], order_direction)
    if length:
        query += " LIMIT {0} OFFSET {1}".format(length, start)
    print(__name__ + ": --------sql----------------------")
    print(query)
    print(__name__ + ": --------sql----------------------")
    cur = get_db().cursor()
    
    # table list
    # query = "SELECT * FROM {}".format(table)
    if searchValue:
        cur.execute(query, [f"%{searchValue}%"] * len(columns))
    else:
        cur.execute(query)
    results = cur.fetchall()  # is list
    
    # total students
    cur.execute(total_sql)
    total = cur.fetchone()
    
    # total num
    cur.execute(total_sql)
    total_num = cur.fetchone()
    total = int(total_num['count(*)'])
    
    data = {
        'recordsFiltered': total,
        'recordsTotal': total,
        'draw': draw,
        'data': results
    }
    
    return data

@bp.route("/adminStudent")
@login_required
def adminStudent():
    """admin-stutents page

    Returns:
        template: students template
    """
    
    # cur = get_db().cursor()
    
    # students list
    # cur.execute("select * from tb_student")
    # students = cur.fetchall()

     #return render_template("stmt/admin-students.html", students = students)
    template = "stmt/admin-student.html"
    return render_template(template)

@bp.route("/admin/getStudent", methods=("GET", "POST"))
@login_required
def getStudent():
    """admin-stutents page

    Returns:
        students: students object
    """
    stuNo = None
    # post
    if request.method == "POST":
        stuNo = request.values.get('studentNo')
    # get
    if request.method == "GET":
        stuNo = request.args.get('studentNo')    
    
    cur = get_db().cursor()
    
    # students list
    cur.execute("select * from tb_student where student_no = %s", (stuNo,))
    students = cur.fetchall()
    return jsonify(students)

@bp.route("/admin/getStudents", methods=("GET", "POST"))
@login_required
def getStudents():
    """admin-stutents API

    Returns:
        students: all students object
    """
    cur = get_db().cursor()
    
    # students list
    cur.execute("select * from tb_student")
    students = cur.fetchall()
    return jsonify(students)

def is_valid_id_card(id_card):
    ''' 校验是否为正确的身份证号码 '''
    pattern = '[1-9][0-9]{14}([0-9]{2}[0-9X])?'
    if isinstance(id_card, int):
        id_card = str(id_card)

    if not re.match(pattern, id_card):
        return False
    items = [int(item) for item in id_card[:-1]]
    # 加权因子表
    factors = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    # 计算17位数字各位数字与对应的加权因子的乘积
    copulas = sum([a * b for a, b in zip(factors, items)])
    # 校验码表
    ck_codes = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
    a = ck_codes[copulas % 11].upper()
    b = id_card[-1].upper()
    return a == b

@bp.route("/admin/add/student", methods=("POST",))
@login_required
def addStudent():
    """ add a student
        
    Returns:
        result: redirect to student admin page with failure/sucess
    """
    # arguments
    # post
    if request.method == "POST":
        student_no = request.values.get('student_no')
        student_name = request.values.get('student_name')
        id_card = request.values.get('id_card')
        gender = request.values.get('gender')
        age = request.values.get('age')
        year = request.values.get('year')
    args = [student_no, student_name, id_card, gender, age, year]
    print (args)
    # if null value submitted
    if not all(x for x in args):
        error = "Failed to add student info! Null value submitted: " + str(args)
        flash(error, 'danger')
        return redirect(url_for("stmt.adminStudent"))
    # if id_card invalidate 
    if not is_valid_id_card(id_card):
        error = "Invalidate id: " + id_card
        flash(error, 'danger')
        return redirect(url_for("stmt.adminStudent"))
    if not (int(gender) == 1 or int(gender) == 2):
        error = "Invalidate gender: " + str(gender)
        flash(error, 'danger')
        return redirect(url_for("stmt.adminStudent"))
    if not all([case.isdigit() for case in [age, year]]):
        error = "Invalidate year or age: " + str([age, year])
        flash(error, 'danger')
        return redirect(url_for("stmt.adminStudent"))       
    if int(age) < 10 or int(age) > 150 or int(year) > 2030 or int(year) < 1999:
        error = "Please check year or age: " + str([age, year])
        flash(error, 'danger')
        return redirect(url_for("stmt.adminStudent")) 
          
    db = get_db()
    cur = db.cursor()
    result = cur.execute(
        "insert into tb_student"
        " (student_no, student_name, id_card, gender, age, year)"
        " VALUES (%s, %s, %s, %s, %s, %s)",
        (student_no, student_name, id_card, gender, age, year)
    )
    db.commit()
    if result < 1:
        error = "Something wrong: " + str(args)
        flash(error, 'danger')
        return redirect(url_for("stmt.adminStudent"))

    success = "Add user successfully. Student_no: " + student_no
    flash(success, 'success')    
    return redirect(url_for("stmt.adminStudent"))

@bp.route("/admin/updateStudent", methods=("POST",))
@login_required
def updateStudent():
    """update-stutents url

    Returns:
        redirect: to students list and give result message
    """
    studentNo = None
    studentName = None
    idCard = None
    gender = None
    age = None
    year = None
    if request.method == "POST":
        studentNo = request.values.get('studentNo')
        studentName = request.values.get('studentName')
        idCard = request.values.get('idCard')
        gender = request.values.get('gender')
        age = request.values.get('age')
        year = request.values.get('year')
    if any(x is None for x in [studentNo, studentName, idCard, gender, age, year]):
        error = "Null value submited, student " + studentNo + " info not changed!"
        flash(error, 'danger')
        return redirect(url_for("stmt.adminStudents"))
        
    cur = get_db().cursor()
    
    # students list
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("update tb_student set" 
                " student_no=%s,"
                " student_name=%s,"
                " id_card=%s,"
                " age=%s,"
                " gender=%s,"
                " year=%s,"
                " update_time=%s"
                " where student_no=%s", [studentNo, studentName, idCard, int(age), int(gender), int(year), update_time, studentNo])
    get_db().commit()

    success = "Student " + studentNo + " info has just been changed!"
    flash(success, 'success')
    return redirect(url_for("stmt.adminStudent"))

@bp.route("/admin/delete/student", methods=("GET", "POST"))
@login_required
def deleteStudent():
    """ delete a student by student_no
        
    Returns:
        result: redirect to student admin page with failure/sucess
    """
    # arguments
    # post
    if request.method == "POST":
        student_no = request.values.get('student_no')
        # op = request.values.get('op')

    # get
    if request.method == "GET":
        student_no = request.args.get('student_no') 
        # op = request.args.get('op') 
   
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT student_no FROM tb_student where student_no=%s", (student_no,)
    )
    user = cur.fetchone()
    if user is None:
        error = "您尝试删除的学生信息不存在: " + student_no
        flash(error, 'danger')
        return redirect(url_for("stmt.adminStudent"))

    result = cur.execute("delete from tb_student where student_no = %s", (student_no,))
    db.commit()
    if result < 1:
        error = "Failed during delete student info. Student_no: " + student_no
        flash(error, 'danger')
        return redirect(url_for("stmt.adminStudent"))
    success = "Delete user successfully. Student_no: " + student_no
    flash(success, 'success')    
    return redirect(url_for("stmt.adminStudent"))

@bp.route("/admin/searchStudents", methods=("POST",))
@login_required
def searchStudents():
    """search students

    Returns:
        filtered studens
    """
    if request.method == "POST":
        query = request.values.get('query')
        print(__name__ + ": " + query)
        return "OKKKKKKKKKKKKK"
    # flash(error, 'danger')
    # return redirect(url_for("stmt.adminStudents"))
        
    cur = get_db().cursor()
    
    # students list
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("select * from tb_student")

    success = "Student " + studentNo + " info has just been changed!"
    flash(success, 'success')
    return redirect(url_for("stmt.adminStudents"))

@bp.route("/adminScore")
@login_required
def adminScore():
    """admin-score page

    Returns:
        template: admin-score template
    """
    return render_template("stmt/admin-score.html")

@bp.route("/adminCourse")
@login_required
def adminCourse():
    """introduction page

    Returns:
        template: introduction template
    """
    return render_template("stmt/introduction.html")

# admin-teacher page functions
@bp.route("/adminTeacher")
@login_required
def adminTeacher():
    """introduction page

    Returns:
        template: introduction template
    """
    return render_template("stmt/admin-teacher.html")

@bp.route("/admin/getTeacher", methods=("GET", "POST"))
@login_required
def getTeacher():
    """admin-stutents page

    Returns:
        students: students object
    """
    teacherNo = None
    # post
    if request.method == "POST":
        teacherNo = request.values.get('teacherNo')
    # get
    if request.method == "GET":
        teacherNo = request.args.get('teacherNo')    
    
    cur = get_db().cursor()
    
    # students list
    cur.execute("select * from tb_teacher where teacher_no = %s", (teacherNo,))
    teachers = cur.fetchall()
    return jsonify(teachers)


# user page

@bp.route("/adminUser")
@login_required
def adminUser():
    """introduction page

    Returns:
        template: introduction template
    """
    return render_template("stmt/admin-user.html")

@bp.route("/admin/delete/user", methods=("GET", "POST"))
@login_required
def deleteUser():
    """ delete a user by user info
        
    Returns:
        result: redirect to user admin page with failure/sucess
    """
    # arguments
    # post
    if request.method == "POST":
        username = request.values.get('username')
        # op = request.values.get('op')

    # get
    if request.method == "GET":
        username = request.args.get('username') 
        # op = request.args.get('op') 
    if username == "admin":
        error = "You can not delete admin!"
        flash(error, 'danger')
        return redirect(url_for("stmt.adminUser"))
    
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT username FROM tb_user where username=%s", (username,)
    )
    user = cur.fetchone()
    if user is None:
        error = "您尝试删除的用户不存在: " + username
        flash(error, 'danger')
        return redirect(url_for("stmt.adminUser"))

    result = cur.execute("delete from tb_user where username = %s", (username,))
    db.commit()
    if result < 1:
        error = "Failed during delete user. User: " + username
        flash(error, 'danger')
        return redirect(url_for("stmt.adminUser"))
    success = "Delete user successfully. User: " + username
    flash(success, 'success')    
    return redirect(url_for("stmt.adminUser"))

@bp.route("/admin/user/addStudent", methods=("POST",))
@login_required
def addStudentUser():
    """ add a student user account
        
    Returns:
        result: redirect to user admin page with failure/sucess
    """
    # arguments
    if request.method == "POST":
        username = request.values.get('student_username')
        student_no = request.values.get('student_no')
        password = request.values.get('password')

    # get
    if request.method == "GET":
        username = request.args.get('student_username') 
        student_no = request.args.get('student_no') 
        password = request.args.get('password') 
    
    db = get_db()
    cur = db.cursor()
    result = cur.execute(
        "select * from tb_user where username=%s or student_no=%s",(username, student_no)
    )
    
    if result > 0:
        danger = "Duplicated username or student account has been created before: " + str([username, student_no])
        flash(danger, 'danger')    
        return redirect(url_for("stmt.adminUser"))
    
    result = cur.execute(
        "select * from tb_student where student_no=%s",(student_no,)
    )
    
    if result < 1:
        danger = "Student info has not been enrolled: " + str([student_no,username,password])
        flash(danger, 'danger')    
        return redirect(url_for("stmt.adminUser"))
    
    result = cur.execute(
        "insert into tb_user"
        " (user_type, username, password, student_no, status)"
        " VALUES (%s, %s, %s, %s, %s)", (0, username, generate_password_hash(password), student_no, 1)
    )
    db.commit()
    if result < 1:
        danger = "Something wrong when add user. User: " + str([username, student_no])
        flash(danger, 'danger')    
        return redirect(url_for("stmt.adminUser"))   
    
    success = "Add student user successfully. User: " + str([username, student_no, password, result])
    flash(success, 'success')
    return redirect(url_for("stmt.adminUser"))   

@bp.route("/admin/user/addTeacher", methods=("POST",))
@login_required
def addTeachertUser():
    """ add a teacher user account
        
    Returns:
        result: redirect to user admin page with failure/sucess
    """
    # arguments
    if request.method == "POST":
        username = request.values.get('student-username')
        student_no = request.values.get('student_no')
        password = request.values.get('password')

    # get
    if request.method == "GET":
        username = request.args.get('student-username') 
        student_no = request.args.get('student_no') 
        password = request.args.get('password') 

    if username == "admin":
        error = "You can not delete admin!"
        flash(error, 'danger')
        return redirect(url_for("stmt.adminUser"))
    
    success = "Add teacher user successfully. User: " + str([username, student_no, password])
    flash(success, 'success')    
    return redirect(url_for("stmt.adminUser"))    

@bp.route("/admin/user/toggle", methods=("GET", "POST"))
@login_required
def toggleUser():
    """ toggle a user status
        
    Returns:
        result: redirect to User admin page with failure/sucess
    """
    # arguments
    # post
    if request.method == "POST":
        target_user = request.values.get('target_user')
        user_status = request.values.get('user_status')

    # get
    if request.method == "GET":
        target_user = request.args.get('target_user') 
        user_status = request.args.get('user_status')
    print("userstatus: " + user_status)
    print("target_user: " + target_user)
    if not(user_status == "1" or user_status == "2"):
        error = "Error occurs, user_status: " + user_status
        flash(error, 'danger')
        return redirect(url_for("stmt.adminUser"))
     
    db = get_db()
    cur = db.cursor()
    result = cur.execute(
        "SELECT username FROM tb_user where username=%s", (target_user,)
    )

    if result < 1:
        error = "The user does not exist: " + target_user
        flash(error, 'danger')
        return redirect(url_for("stmt.adminUser"))

    if user_status == "1":
        user_status = 2
    else:
        user_status = 1
    
    result = cur.execute("update tb_user set status=%s where username = %s", (user_status, target_user))
    db.commit()
    if result < 1:
        error = "Failed during toggle user status. User: " + target_user
        flash(error, 'danger')
        return redirect(url_for("stmt.adminUser"))
    
    success = "Toggle user successfully. User: " + target_user
    flash(success, 'success')    
    return redirect(url_for("stmt.adminUser"))    
         
#################################################
# User views
#################################################

@bp.route("/userScore")
@login_required
def userScore():
    """introduction page

    Returns:
        template: introduction template
    """
    return render_template("stmt/introduction.html")                    

@bp.route("/userInfo")
@login_required
def userInfo():
    """introduction page

    Returns:
        template: introduction template
    """
    return render_template("stmt/introduction.html")   

#################################################
# Others, examples
#################################################

def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
