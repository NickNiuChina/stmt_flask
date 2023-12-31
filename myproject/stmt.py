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
from pymysql.err import IntegrityError

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
    user = getattr(g, 'user', None)
    if user is not None:
            if user.get('status'):
                current_app.logger.info('user status --------------------------: ' + str(g.user['status']))
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
            'course': ['course_no', 'course_name', 'student_num'],
            }
 
@bp.route("/admin/list/<any(login_history, student, teacher, test, user):list_object>", methods=("GET", "POST"))
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
    total_sql = "SELECT * FROM {}".format(table)
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
    
    # total students
    total = cur.execute(total_sql)
    
    # table list
    # query = "SELECT * FROM {}".format(table)
    ftotal = 0
    if searchValue:
        ftotal = cur.execute(query, [f"%{searchValue}%"] * len(columns))
    else:
        ftotal = cur.execute(query)
        ftotal = total
    results = cur.fetchall()  # is list

    data = {
        'recordsFiltered': ftotal,
        'recordsTotal': total,
        'draw': draw,
        'data': results
    }
    
    return data

#####################
# admin student management views
#####################
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
        students: all students object or unregistered student
    """
    
    if request.method == "POST":
        unregistered = request.values.get('unregistered')
    
    cur = get_db().cursor()
    students = None
    if unregistered == '1':
        # return only unregistered students
        cur.execute("SELECT * FROM tb_student AS ts"
                    " WHERE NOT EXISTS ("
                    " SELECT *"
                    " FROM tb_user AS tu" 
                    " WHERE ts.student_no=tu.student_no)"
                    )
        students = cur.fetchall()
    else: 
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
    
    # if duplicated info: id, name, no
          
    db = get_db()
    cur = db.cursor()
    
    result = cur.execute( 
                         "select * from tb_student where student_no = %s "
                         " or student_name=%s "
                         " or id_card = %s", [student_no, student_name, id_card]
                         )
    if result > 0:
        error = "Duplicated studentno or studentname or ID: " + str([student_no, student_name, id_card])
        flash(error, 'danger')
        return redirect(url_for("stmt.adminStudent"))        
    
    
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

#####################
# admin teacher management views
#####################
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

@bp.route("/admin/add/teacher", methods=("POST",))
@login_required
def addTeacher():
    """ add a teacher
        
    Returns:
        result: redirect to teacher admin page with failure/sucess
    """
    # arguments
    # post
    result = None
    if request.method == "POST":
        teacher_no = request.values.get('teacher_no')
        teacher_name = request.values.get('teacher_name')
        gender = request.values.get('gender')

    args = [teacher_no, teacher_name, gender]

    # if null value submitted
    if not all(x for x in args):
        error = "Failed to add teacher info! Null value submitted: " + str(args)
        flash(error, 'danger')
        return redirect(url_for("stmt.adminStudent"))

    if not (int(gender) == 1 or int(gender) == 2):
        error = "Invalidate gender: " + str(gender)
        flash(error, 'danger')
        return redirect(url_for("stmt.adminStudent"))
     
    db = get_db()
    cur = db.cursor()
    result = cur.execute( 
                         "select * from tb_teacher where teacher_no = %s ", [teacher_no,]
                         )
    if result > 0:
        error = "Duplicated teacherno: " + str([teacher_no,])
        flash(error, 'danger')
        return redirect(url_for("stmt.adminTeacher"))    
    

    result = cur.execute(
        "insert into tb_teacher"
        " (teacher_no, teacher_name, gender)"
        " VALUES (%s, %s, %s)",
        (teacher_no, teacher_name, gender)
    )
    db.commit()

    if result < 1:
        error = "Something wrong: " + str(args)
        flash(error, 'danger')
        return redirect(url_for("stmt.adminStudent"))

    success = "Add teacher info successfully. Teacher: " + str(args)
    flash(success, 'success')    
    return redirect(url_for("stmt.adminTeacher"))


@bp.route("/admin/updateTeacher", methods=("POST",))
@login_required
def updateTeacher():
    """admin-teacher update teacher

    Returns:
        teachers: to teacher admin page with update result failure/success
    """
    # post
    if request.method == "POST":
        teacher_no = request.values.get('teacherNo')
        teacher_name = request.values.get('teacherName')
        gender = request.values.get('gender')
        
    # get
    if request.method == "GET":
        teacher_no = request.args.get('teacherNo')    
        teacher_name = request.args.get('teacherName')    
        gender = request.args.get('gender')    
    
    db = get_db()
    cur = db.cursor()
    
    # students list
    result = cur.execute("select * from tb_teacher where teacher_no = %s", (teacher_no,))
    if result < 1:
        error = "TeacherNo does not exist, please check: " + teacher_no
        flash(error, 'danger')
        return redirect(url_for("stmt.adminTeacher")) 
    if any(x is None for x in [teacher_no, teacher_name, gender]):
        error = "Null value submited, student info not changed! " + str([teacher_no, teacher_name, gender])
        flash(error, 'danger')
        return redirect(url_for("stmt.adminTeacher"))
    
    result = cur.execute(
                        "update tb_teacher set"
                        " teacher_name = %s,"
                        " gender = %s"
                        " where teacher_no=%s", [teacher_name, gender, teacher_no]
                         )
    db.commit()
    # 未修改时 返回0，后面用 try except 捕获错误
    if result < 1:
        error = "Info not changed. Teacher: " + str([teacher_no, teacher_name, gender])
        flash(error, 'danger')
        return redirect(url_for("stmt.adminTeacher"))
        
    success = "Teacher info has just been changed: " + str([teacher_no, teacher_name, gender])
    flash(success, 'success')
    # return render_template("stmt/admin-teacher.html")
    return redirect(url_for("stmt.adminTeacher"))

@bp.route("/admin/delete/teacher", methods=("GET", "POST"))
@login_required
def deleteTeacher():
    """ delete a teacher by teacher_no
        
    Returns:
        result: redirect to teacher admin page with failure/sucess
    """
    # arguments
    # post
    if request.method == "POST":
        teacher_no = request.values.get('teacher_no')

    # get
    if request.method == "GET":
        teacher_no = request.args.get('teacher_no') 
   
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT teacher_no FROM tb_teacher where teacher_no=%s", (teacher_no,)
    )
    user = cur.fetchone()
    if user is None:
        error = "The teacher does not existed: " + teacher_no
        flash(error, 'danger')
        return redirect(url_for("stmt.adminTeacher"))

    try:
        cur.execute("delete from tb_teacher where teacher_no = %s", (teacher_no,))
        db.commit()
    except IntegrityError as e:
        error = "Failed during delete teacher info cause this teacher is referenced somewhere. Error: " + str(e)
        flash(error, 'danger')
        return redirect(url_for("stmt.adminTeacher"))
    except Exception as e:
        error = "Failed during delete teacher info cause this teacher is referenced somewhere. Error: " + str(e)
        flash(error, 'danger')
        return redirect(url_for("stmt.adminTeacher"))
   
    success = "Delete user successfully. Teacher_no: " + teacher_no
    flash(success, 'success')    
    return redirect(url_for("stmt.adminTeacher"))


#####################
# admin course management views
#####################

@bp.route("/adminCourse")
@login_required
def adminCourse():
    """introduction page

    Returns:
        template: introduction template
    """
    return render_template("stmt/admin-course.html")

@bp.route("/admin/list/course", methods=("GET", "POST"))
@login_required
def listCourse():
    """ API to return all course lines 
        response to: http://127.0.0.1:5000/admin/list/course
        
    Returns:
        objects: list from course table
    """

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
    columns = ["course_no", "course_name", "teacher_name", "student_num"]
    query = "select c.course_no, c.course_name, \
(select teacher_name from  tb_teacher as t where c.teacher_no=t.teacher_no ) as teacher_name, \
(select count(s.id) from  tb_score as s where c.course_no=s.course_no ) as student_num \
from  tb_course as c"
    total_sql = query
    if searchValue:
        query += " WHERE course_no like %s OR course_name LIKE %s OR teacher_name like %s "

    query += " ORDER BY {0} {1}".format(columns[ int(order_col) - 1 ], order_direction)
    if length:
        query += " LIMIT {0} OFFSET {1}".format(length, start)
    print(__name__ + ": --------sql----------------------")
    print(query)
    print(__name__ + ": --------sql----------------------")
    cur = get_db().cursor()
    
    # toal num
    total = cur.execute(total_sql)
    
    # table list
    # query = "SELECT * FROM {}".format(table)
    result = 0
    if searchValue:
        ftotal = cur.execute(query, [f"%{searchValue}%"] * (len(columns) - 1))
    else:
        ftotal = cur.execute(query)
        ftotal = total
    results = cur.fetchall()  # is list

    data = {
        'recordsFiltered': ftotal,
        'recordsTotal': total,
        'draw': draw,
        'data': results
    }
    
    return data


#####################
# admin score management views
#####################

@bp.route("/adminScore")
@login_required
def adminScore():
    """admin-score page

    Returns:
        template: admin-score template
    """
    return render_template("stmt/admin-score.html")

#####################
# admin user management views
#####################

@bp.route("/adminUser")
@login_required
def adminUser():
    """introduction page

    Returns:
        template: introduction template
    """
    return render_template("stmt/admin-user.html")

@bp.route("/admin/updateUser", methods=("POST",))
@login_required
def updateUser():
    """update-user url

    Returns:
        redirect: Return to user list with failure/success
    """
    user_id = None
    username = None
    password = None
    display_name = None

    if request.method == "POST":
        user_id = request.values.get('user_id')
        username = request.values.get('username')
        password = request.values.get('password')
        display_name = request.values.get('display_name')
    if any(x is None for x in [username, password]):
        error = "Null value submited, Info: " + str([username, password])
        flash(error, 'danger')
        return redirect(url_for("stmt.adminUser"))
    
    args = [user_id, username, password, display_name]    
    cur = get_db().cursor()
    
    # students list
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = cur.execute("update tb_user set" 
                " username=%s,"
                " password=%s,"
                " display_name=%s,"
                " update_time=%s"
                " where user_id=%s", [username, generate_password_hash(password), display_name, update_time, user_id])
    get_db().commit()
    if result < 1:
        error = "Failed during update user. User: " + username
        flash(error, 'danger')
        return redirect(url_for("stmt.adminUser"))
    
    success = "User info has just been changed! User: " + str(args)
    flash(success, 'success')
    return redirect(url_for("stmt.adminUser"))

@bp.route("/admin/getUser", methods=("GET", "POST"))
@login_required
def getUser():
    """admin-user get a user by user_id

    Returns:
        students: students object
    """
    user_id = None
    # post
    if request.method == "POST":
        user_id = request.values.get('user_id')
    # get
    if request.method == "GET":
        user_id = request.args.get('user_id')    
    
    cur = get_db().cursor()
    
    # students list
    cur.execute("select * from tb_user where user_id = %s", (user_id,))
    user = cur.fetchall()
    return jsonify(user)

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
def addTeacherUser():
    """ add a teacher user account
        
    Returns:
        result: redirect to user admin page with failure/sucess
    """
    # arguments
    if request.method == "POST":
        username = request.values.get('username')
        password = request.values.get('password')

    # get
    if request.method == "GET":
        username = request.args.get('username') 
        password = request.args.get('password') 
    
    db = get_db()
    cur = db.cursor()
    result = cur.execute(
        "select * from tb_user where username=%s",(username,)
    )
    if result > 0:
        danger = "This username has been used: " + username
        flash(danger, 'danger')    
        return redirect(url_for("stmt.adminUser"))
    
    result = cur.execute(
        "insert into tb_user"
        " (user_type, username, password, student_no, status)"
        " VALUES (%s, %s, %s, %s, %s)", (1, username, generate_password_hash(password), 0, 1)
    )
    db.commit()
    if result < 1:
        danger = "Something wrong when add user. User: " + str([username, password])
        flash(danger, 'danger')    
        return redirect(url_for("stmt.adminUser"))      
               
    success = "Add teacher user successfully. User: " + str([username, password])
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
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = cur.execute("update tb_user set status=%s, update_time=%s where username = %s", 
                         (user_status, update_time,target_user)
                         )
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
