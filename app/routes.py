from app import app
from flask import render_template, flash, redirect, request, jsonify, url_for
from app.forms import LoginForm
import requests

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'mcotter'}
    classes = [{'classInfo': {'code': 'CSC324', 'title': 'DevOps'}, 'instructor': 'Baoqiang Yan'},{'classInfo': {'code': 'CSC184', 'title': 'Python Programming'}, 'instructor': 'Evan Noynaert'}]
    return render_template('index.html', title='Home', user=user, classes=classes) 



@app.route('/mcotter1')
def mcotter1():
    user = {'username': 'mcotter'}
    classes = [{'classInfo': {'code': 'CSC324', 'title': 'DevOps'}, 'instructor': 'Baoqiang Yan'},{'classInfo': {'code': 'CSC184', 'title': 'Python Programming'}, 'instructor': 'Evan Noynaert'}]
    return render_template('mcotter1.html', title='Home', user=user, classes=classes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            credentials = {"username": form.username.data, "password": form.password.data}
            response = requests.post(url_for('loginAPI', _external=True), json=credentials)
            dict = response.json()
            if dict['Success']:
                flash('Welcome user {}({})! You opted for remember_me={}'.format(form.username.data, dict['uid'], form.remember_me.data))
                return redirect(url_for('mcotter1'))
            else:
                flash('Invalid credentials')
    else:
        if request.args:
            flash('GET method not allowed for login!')
        # else:
        #     flash('No data in request!')

    return render_template('login.html', title='Sign In', form=form)


@app.route('/json')
def jsonTest():
    # return jsonify(list(range(5)))
    instructor = {"username": "byan",
                  "role": "instructor",
                  "uid": 11,
                  "name":
                      {"firstname": "Baoqiang",
                       "lastname": "Yan"
                       }
                  }
    student = {"username": "mcotter",
               "role": "student",
               "uid": 12,
               "name":
                   {"firstname": "Matthew",
                    "lastname": "Cotter"
                    }
             }

    return jsonify(student)

@app.route('/loginapi', methods=['GET', 'POST'])
def loginAPI():
    json_data = request.get_json(force = True)
    if json_data:
        username = json_data["username"]
        password = json_data["password"]
    else:
        return jsonify(Success=False)
    if username == 'byan' and password == '123':
        return jsonify(Success=True, uid=11)
    if username == 'mcotter' and password == '123':
        return jsonify(Success=True, uid=12)
    return jsonify(Success=False)
