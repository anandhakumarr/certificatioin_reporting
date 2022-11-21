import csv
import json
from flask import Flask, request, render_template, json, jsonify, send_file
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

EMPLOYEE_REF = 'data/employee_ref.csv'
LOGIN_REF = 'data/users.csv'
CERTIFICATION_DATA = 'data/certification.csv'
TRAINING_DATA = 'data/training.csv'
CERTIFICATION_LIST = 'data/list_of_certifications.csv'
TRAINING_LIST = 'data/list_of_trainings.csv'
TRAINING_CATEGORY_LIST = 'data/training_category.csv'
CATEGORY_LIST = 'data/category.csv'

def read_csv(file_name):
  with open(file_name, 'r') as f:
      dict_reader = csv.DictReader(f)
      list_of_dict = list(dict_reader)
      return list_of_dict

users = {}
logins = read_csv(LOGIN_REF)
for user in logins:
  users[user['username']] = generate_password_hash(user['password'])

def write_to_file(data, output_path):
    print(f"Writing to {output_path}")
    with open(output_path, 'a') as file:
        writer_object = csv.writer(file)
        writer_object.writerow(data)

app = Flask(__name__)

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/', methods = ['GET'])
@auth.login_required
def home():
    is_admin = False
    for user in logins:
        if user['username'] == request.authorization.username:
            is_admin = bool(int(user['admin']))
    employees = read_csv(EMPLOYEE_REF)
    certification_list = read_csv(CERTIFICATION_LIST)
    training_list = read_csv(TRAINING_LIST)
    training_category_list = read_csv(TRAINING_CATEGORY_LIST)
    employees_json = json.dumps(employees)
    categories = read_csv(CATEGORY_LIST)
    certifications = read_csv(CERTIFICATION_DATA)
    trainings = read_csv(TRAINING_DATA)  

    reports = {}
    project = {}
    project_cost = {}
    for row in certifications:
        project_name = row['project'].strip()
        if row['intellect'] == 'In Intellect':
            if project.get(project_name):
                project[project_name]['after'] = project[project_name].get('after',0)+1
            else:
                project[project_name] = {'before': 0, 'after': 1}
      
        elif row['intellect'] == 'Before Intellect':
            if project.get(project_name):
                project[project_name]['before'] = project[project_name].get('before',0)+1
            else:
                project[project_name] = {'before': 1, 'after': 0}

        if project_cost.get(project_name):
            project_cost[project_name]['cost'] = project_cost[project_name].get('cost',0) + float(row['cost'])
        else:
            project_cost[project_name] = {'cost': float(row['cost'])}

    project_list = []
    before_intellect_list = []
    after_intellect_list = []
    for key, value in project.items():
        project_list.append(key.strip())
        before_intellect_list.append(value['before'])
        after_intellect_list.append(value['after'])

    c_project_list = []
    cost_list = []
    for key, val in project_cost.items():
        c_project_list.append(key.strip())
        cost_list.append(val['cost'])

    reports['intellect'] = {'after_intellect_list': after_intellect_list,
    'before_intellect_list': before_intellect_list,
    'project_list': project_list}

    reports['project_cost'] = {'project_list': c_project_list, 'cost': cost_list}

    return render_template('index.html', employees = employees, 
      employees_json = employees_json, certification_list = certification_list,
      categories = categories, training_list = training_list,
      training_category_list = training_category_list, is_admin = is_admin,
      certifications = certifications, trainings = trainings,
      reports = reports)

@app.route('/post_data', methods = ['POST'])
def post_data():
    request_data = request.get_json()

    if request_data['data_type'] == 'certification':
      output_path  = CERTIFICATION_DATA
    else:
      output_path  = TRAINING_DATA
    request_data.pop('data_type')

    write_to_file(list(request_data.values()), output_path)

    return jsonify({"return": "True"})


@app.route('/get_emp_details', methods = ['POST'])
def get_emp_details():
    request_data = request.get_json()
    employee_id = request_data['employee_id']

    certifications = read_csv(CERTIFICATION_DATA)
    trainings = read_csv(TRAINING_DATA)
    print(employee_id)
    
    user_certifications = [row for row in certifications if row['employee_id'] == employee_id]
    user_trainings = [row for row in trainings if row['employee_id'] == employee_id]
    print(user_certifications, user_trainings)
    return jsonify({"return": "True", 
        "user_certifications": user_certifications,
        "user_trainings": user_trainings})



@app.route('/download/certification')
def downloadCFile():
    return send_file('data/certification.csv', as_attachment=True)

@app.route('/download/training')
def downloadTFile():
    return send_file('data/training.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)