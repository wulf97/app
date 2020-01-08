import psycopg2
from psycopg2.extras import DictCursor
from wtforms import Form, StringField, PasswordField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms.validators import Required, NumberRange

from dbconfig import dbconfig

# ********************************
class LoginForm(Form):
    login = StringField('login', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    submit = SubmitField('Вход')

# ********************************
class RegistrationStudentForm(Form):
    login = StringField('login', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    confirm_password = PasswordField('confirm_password', validators = [Required()])
    surname = StringField('surname', validators = [Required()])
    name = StringField('name', validators = [Required()])
    patronymic = StringField('patronymic', validators = [Required()])
    submit = SubmitField('Отправить')
    group_number = SelectField('group_number', choices = [('0', 'None')])

# ********************************
class RegistrationTeacherForm(Form):
    login = StringField('login', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    confirm_password = PasswordField('confirm_password', validators = [Required()])
    surname = StringField('surname', validators = [Required()])
    name = StringField('name', validators = [Required()])
    patronymic = StringField('patronymic', validators = [Required()])
    science_degree = StringField('science_degree', validators = [Required()])
    number_of_publications = IntegerField('number_of_publications', validators = [NumberRange(0, 500)])
    submit = SubmitField('Отправить')
    department_number = SelectField('department_number', choices = [('0', 'None')])

# ********************************
class profileStudentForm(Form):
    login = StringField('login', validators = [Required()])
    surname = StringField('surname', validators = [Required()])
    name = StringField('name', validators = [Required()])
    patronymic = StringField('patronymic', validators = [Required()])
    submit = SubmitField('Сохранить')
    conn = psycopg2.connect(dbname = dbconfig['dbname'],
                            user = dbconfig['user'],
                            password = dbconfig['password'],
                            host = dbconfig['host'])
    cursor = conn.cursor()
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
    cursor.close()
    conn.close()

    group_number = SelectField('group_number', choices = choices)

# ********************************
class profileTeacherForm(Form):
    login = StringField('login', validators = [Required()])
    surname = StringField('surname', validators = [Required()])
    name = StringField('name', validators = [Required()])
    patronymic = StringField('patronymic', validators = [Required()])
    submit = SubmitField('Сохранить')
    science_degree = StringField('science_degree', validators = [Required()])
    number_of_publications = IntegerField('number_of_publications', validators = [NumberRange(0, 500)])

    conn = psycopg2.connect(dbname = dbconfig['dbname'],
                            user = dbconfig['user'],
                            password = dbconfig['password'],
                            host = dbconfig['host'])
    cursor = conn.cursor()
    sql = '''select "number" from "department"'''
    cursor.execute(sql)
    rec = cursor.fetchall()

    if rec:
        choices = []
        if len(rec) > 0:
            for i in rec:
                choices += [(str(i[0]), str(i[0]))]
    else:
        choices = [(0, None)]
    cursor.close()
    conn.close()

    department_number = SelectField('department_number', choices = choices)

# ********************************
class AddDepartment(Form):
    department_number = IntegerField('department_number', validators = [NumberRange(0, 50)])
    submit = SubmitField('Добавить')

# ********************************
class AddSpeciality(Form):
    speciality_number = IntegerField('speciality_number', validators = [NumberRange(0, 50)])
    speciality_name = StringField('speciality_name', validators = [Required()])
    submit = SubmitField('Добавить')

# ********************************
class AddSemesterCurriculum(Form):
    semester_number = IntegerField('semester_number', validators = [NumberRange(0, 12)])
    speciality_number = IntegerField('speciality_number', validators = [NumberRange(0, 50)])
    submit = SubmitField('Добавить')

# ********************************
class AddSubjectInTheCurriculum(Form):
    subject_name = StringField('subject_name', validators = [Required()])
    number_of_lection = IntegerField('number_of_lection', validators = [NumberRange(0, 40)])
    number_of_labs = IntegerField('number_of_lection', validators = [NumberRange(0, 40)])
    kr = BooleanField('kr')
    semester_id = IntegerField('semester_id')
    submit = SubmitField('Добавить')

# ********************************
class AddLesson(Form):
    day_of_the_week = IntegerField('day_of_the_week', validators = [NumberRange(1, 7)])
    serial_number = IntegerField('serial_number', validators = [NumberRange(1, 10)])
    subject_type = IntegerField('subject_type', validators = [NumberRange(1, 2)])
    audience_number = IntegerField('subject_type', validators = [NumberRange(1, 999)])
    subject_id = IntegerField('subject_id')
    submit = SubmitField('Добавить')

# ********************************
class AddGroup(Form):
    group_number = IntegerField('group_number', validators = [NumberRange(0, 9999)])
    current_sem = IntegerField('current_sem', validators = [NumberRange(0, 12)])
    speciality_number = IntegerField('speciality_number', validators = [NumberRange(0, 50)])
    submit = SubmitField('Добавить')

# ********************************
class AddAudience(Form):
    audience_number = IntegerField('audience_number', validators = [NumberRange(0, 999)])
    submit = SubmitField('Добавить')
