from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import url_for

import psycopg2
from psycopg2.extras import DictCursor

from dbconfig import dbconfig
from user import Student
from forms import *

app = Flask(__name__)
app.secret_key = 'key'

# **********************************************************
# Главная страница
@app.route('/')
@app.route('/index')
def index():
	if not session.get('acc_type'):
		return redirect(url_for('login'))

	return render_template('index.html')

# **********************************************************
# Вход в систему
@app.route('/login', methods = ['POST', 'GET'])
def login():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
			login = request.form.get('login', '')
			password = request.form.get('password', '')

			if login != 'admin' and password != 'admin':
				conn = psycopg2.connect(dbname = dbconfig['dbname'],
										user = dbconfig['user'],
										password = dbconfig['password'],
										host = dbconfig['host'])
				cursor = conn.cursor()
				sql = '''select * from "user" where "login" = '{}' and password = '{}' '''.format(login, password)
				cursor.execute(sql)
				rec = cursor.fetchone()

				if rec:
					session['id'] = rec[0]
					session['login'] = rec[1]
					session['name'] = rec[3]
					session['surname'] = rec[4]
					session['patronymic'] = rec[5]
					session['acc_type'] = rec[6];

				cursor.close()
				conn.close()
			else:
				session['acc_type'] = 3;

	if session.get('acc_type'):
		return redirect(url_for('index'))
	else:
		return render_template('login.html', form = form)

# **********************************************************
# Регистрация в системе
@app.route('/registration', methods = ['POST', 'GET'])
def registration():
	# Записываем в базу данные пользователя
	conn = psycopg2.connect(dbname = dbconfig['dbname'],
							user = dbconfig['user'],
							password = dbconfig['password'],
							host = dbconfig['host'])
	cursor = conn.cursor()

	if request.args.get('acc_type', '') == 'student':
		acc_type = 1
		form = RegistrationStudentForm(request.form)
	elif request.args.get('acc_type', '') == 'teacher':
		acc_type = 2
		form = RegistrationTeacherForm(request.form)

	# Если кнопка 'Отправить' нажата
	if request.method == 'POST' and form.validate():
		login = request.form.get('login', '')
		password = request.form.get('password', '')
		name = request.form.get('name', '')
		surname = request.form.get('surname', '')
		patronymic = request.form.get('patronymic', '')

		# Проверяем правильность пароля
		if password != request.form.get('confirm_password', ''):
			print('Check password')
			return render_template('registration.html', form = form, acc_type = acc_type)

		sql = '''insert into "user"("login", "password", "name", "surname", "patronymic", "user_type")'''
		sql += '''values('{}', '{}', '{}', '{}', '{}', '{}') returning "id"'''.format(login, password, name, surname, patronymic, acc_type)
		cursor.execute(sql)
		id = cursor.fetchone()[0];


		if acc_type == 1:
			# Регистрация студента
			group_number = request.form.get('group_number', '')

			# Запишем в базу данные о студенте
			sql = '''insert into "student"("user_id", "group_number") values('{}', '{}')'''.format(id, group_number)
			cursor.execute(sql)

		elif acc_type == 2:
			print('teach')
			# Регистрация преподавателя
			science_degree = request.form.get('science_degree', '')
			number_of_publications = request.form.get('number_of_publications', '')
			department_number = request.form.get('department_number', '')

			# Запишем в базу данные о преподавателе
			sql = '''insert into "teacher"("user_id", "science_degree", "number_of_publications", "number_of_department")'''
			sql += '''values('{}', '{}', '{}', '{}')'''.format(id, science_degree, number_of_publications, department_number)
			cursor.execute(sql)

		# Закрытие соединения с базой
		conn.commit()
		cursor.close()
		conn.close()

		return redirect(url_for('index'))

	#
	if acc_type == 1:
		# conn = psycopg2.connect(dbname = dbconfig['dbname'],
	    #                         user = dbconfig['user'],
	    #                         password = dbconfig['password'],
	    #                         host = dbconfig['host'])
		# cursor = conn.cursor()
		sql = '''select "number" from "group"'''
		cursor.execute(sql)
		rec = cursor.fetchall()

		if rec:
			choices = []
			if len(rec) > 0:
				for i in rec:
					choices += [(str(i[0]), str(i[0]))]
			else:
				choices = [(0, None)]

		form.group_number.choices = choices;

	# Закрытие соединения с базой
	conn.commit()
	cursor.close()
	conn.close()

	return render_template('registration.html', form = form, choices = choices, acc_type = acc_type)

# **********************************************************
# Выход из профиля
@app.route('/logout')
def logout():
	# Удаление сессий
	session.pop('id', None)
	session.pop('login', None)
	session.pop('name', None)
	session.pop('surname', None)
	session.pop('patronymic', None)
	session.pop('acc_type', None)
	return redirect(url_for('login'))

# **********************************************************
# Панель администратора
@app.route('/control_panel', methods = ['GET', 'POST'])
def control_panel():
	rec, form = update_control_panel_content();
	if request.method == 'POST' and form.validate():
		if request.args.get('act', '') == 'department':
			department_number = request.form.get('department_number', '')
			sql = '''insert into "department"("number") values('{}')'''.format(department_number)
		elif request.args.get('act', '') == 'speciality':
			speciality_number = request.form.get('speciality_number', '')
			speciality_name = request.form.get('speciality_name', '')
			sql = '''insert into "speciality"("number", "name") values('{}', '{}')'''.format(speciality_number, speciality_name)
		elif request.args.get('act', '') == 'semester_curriculum':
			id = request.form.get('id', '')
			semester_number = request.form.get('semester_number', '')
			speciality_number = request.form.get('speciality_number', '')
			sql = '''insert into "semester_curriculum"("semester_number", "speciality_number") values('{}', '{}')'''.format(semester_number, speciality_number)
		elif request.args.get('act', '') == 'subject_in_the_curriculum':
			subject_name = request.form.get('subject_name', '')
			number_of_lection = request.form.get('number_of_lection', '')
			number_of_labs = request.form.get('number_of_labs', '')
			kr = request.form.get('kr', '')
			if kr == '': kr = 'n'
			semester_id = request.form.get('semester_id', '')
			sql = '''insert into "subject_in_the_curriculum"("name", "number_of_lection", "number_of_labs", "kr", "semester_curriculum_id") values('{}', '{}', '{}', '{}', '{}')'''.format(subject_name, number_of_lection, number_of_labs, kr, semester_id)
		elif request.args.get('act', '') == 'lesson':
			day_of_the_week = request.form.get('day_of_the_week', '')
			serial_number = request.form.get('serial_number', '')
			subject_type = request.form.get('subject_type', '')
			audience_number = request.form.get('audience_number', '')
			subject_id = request.form.get('subject_id', '')
			sql = '''insert into "lesson"("day_of_the_week", "serial_number", "subject_type", "audience_number", "subject_id") values('{}', '{}', '{}', '{}', '{}')'''.format(day_of_the_week, serial_number, subject_type, audience_number, subject_id)

		# Открытие соединения с БД
		conn = psycopg2.connect(dbname = dbconfig['dbname'],
								user = dbconfig['user'],
								password = dbconfig['password'],
								host = dbconfig['host'])
		cursor = conn.cursor()
		# Выполнение записи в БД
		cursor.execute(sql)

		# Закрытие соединения с БД
		conn.commit()
		cursor.close()
		conn.close()

		rec, form = update_control_panel_content();

	# Удаление строк из БД
	if request.args.get('del', ''):
		conn = psycopg2.connect(dbname = dbconfig['dbname'],
								user = dbconfig['user'],
								password = dbconfig['password'],
								host = dbconfig['host'])
		cursor = conn.cursor()
		if request.args.get('act', '') == 'department':
			sql = '''delete from "department" where "number" = {}'''.format(request.args.get('del', ''))
		elif request.args.get('act', '') == 'speciality':
			sql = '''delete from "speciality" where "number" = {}'''.format(request.args.get('del', ''))
		elif request.args.get('act', '') == 'semester_curriculum':
			sql = '''delete from "semester_curriculum" where "id" = {}'''.format(request.args.get('del', ''))

		cursor.execute(sql)
		# Закрытие соединения с БД
		conn.commit()
		cursor.close()
		conn.close()
		return redirect(url_for('control_panel', act = request.args.get('act')))

	return render_template('control_panel.html', form = form, rec = rec)

# **********************************************************
def update_control_panel_content():
	conn = psycopg2.connect(dbname = dbconfig['dbname'],
							user = dbconfig['user'],
							password = dbconfig['password'],
							host = dbconfig['host'])
	cursor = conn.cursor()

	if request.args.get('act', '') == 'department':
		form = AddDepartment(request.form)
		sql = '''select * from "department"'''
	elif request.args.get('act', '') == 'speciality':
		form = AddSpeciality(request.form)
		sql = '''select * from "speciality"'''
	elif request.args.get('act', '') == 'semester_curriculum':
		form = AddSemesterCurriculum(request.form)
		sql = '''select * from "semester_curriculum"'''
	elif request.args.get('act', '') == 'subject_in_the_curriculum':
		form = AddSubjectInTheCurriculum(request.form)
		sql = '''select * from "subject_in_the_curriculum"'''
	elif request.args.get('act', '') == 'lesson':
		form = AddLesson(request.form)
		sql = '''select * from "lesson"'''
	elif request.args.get('act', '') == 'group':
		form = AddLesson(request.form)
		sql = '''select * from "group"'''
	elif request.args.get('act', '') == 'audience':
		form = AddAudience(request.form)
		sql = '''select * from "audience"'''

	cursor.execute(sql)
	return cursor.fetchall(), form

# **********************************************************
# Редактирование личного профиля
@app.route('/profile')
def profile():
	if session['acc_type'] == 1:
		form = profileStudentForm(request.form)
	elif session['acc_type'] == 2:
		form = profileTeacherForm(request.form)

	return render_template('profile.html', form = form)
