from flask import Blueprint, abort
from flask import render_template, url_for, request, redirect 
from flask_login import login_required, current_user
import json

from pseudobook.database import mysql

from pseudobook.models import employee as employee_model
from pseudobook.models import advertisement as ads_model
from pseudobook.models import sale as sales_model

from pseudobook.forms.create_ad import CreateAd as CreateAdForm

EMPLOYEES_PER_PAGE = 15
ADS_PER_PAGE = 5

'''
Setup Blueprint
'''
mod = Blueprint('employees', __name__, template_folder='../templates/employees')

'''
View Routes
'''
@mod.route('/employee/<string:userID>', methods=['GET'])
@login_required
def employee_page(userID):
	employee = employee_model.Employee.get_employee_by_id(userID)
	if employee:
		create_ad_form = CreateAdForm()
		searchable_columns = [c for c in ads_model.searchable_columns.keys() if not c == 'Posted By']
		return render_template('employee_page.html',
								employee=employee,
								is_current_employees_page=(current_user.userID == employee.userID),
								create_ad_form=create_ad_form,
								searchable_columns=searchable_columns)
	else:
		abort(404)

@mod.route('/employees', methods=['GET'])
@login_required
def employees():
	employees_offset = request.values.get('employees_offset')
	employees_offset = int(employees_offset) if employees_offset else 0

	total_employees = employee_model.Employee.count_employees()
	employees = employee_model.Employee.scroll_employees(employees_offset, EMPLOYEES_PER_PAGE)
	prev_employees = True if employees_offset > 0 else False
	next_employees = True if ((employees_offset + 1) * EMPLOYEES_PER_PAGE) < total_employees else False

	return render_template('employees.html', 
							employees=employees, 
							prev_employees=prev_employees, 
							next_employees=next_employees,
							employees_offset=employees_offset)

'''
Post Methods
'''
@mod.route('/employee/getownads', methods=['POST'])
@login_required
def getownads():
    userID = request.json['userID']

    ads = ads_model.Advertisement.get_ads_made_by_user(0, ADS_PER_PAGE, userID)
    return json.dumps([o.__dict__ for o in ads])

@mod.route('/employee/delete_ad', methods=['POST'])
def delete_ad():
	adID = request.json['adID']

	ad = ads_model.Advertisement.get_ad_by_id(adID)
	if ad != None and ad.employeeID == current_user.userID:
		ads_model.Advertisement.delete_ad(adID)
	else:
		abort(403)
	
	return ""

'''
Form Routes
'''
@mod.route('/employees/forms/create_ad', methods=['POST'])
@login_required
def create_ad_form():
	itemName = request.form['itemName']
	itemType = request.form['itemType']
	company = request.form['company']
	content = request.form['content']

	create_ad_form = CreateAdForm(request.form)
	if request.form and create_ad_form.validate_on_submit():
		try:
			ads_model.Advertisement.create_new_ad()
		except (mysql.connection.Error, mysql.connection.Warning) as e:
			print(e)
			flash('There was an error creating this ad.')
	else:
		flash('There was an error creating this ad.')

	return redirect(request.referrer)
