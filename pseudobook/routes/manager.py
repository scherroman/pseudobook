from flask import Blueprint, abort
from flask import render_template, url_for, request, redirect 
from flask_login import login_required, current_user
from datetime import datetime
import json

from pseudobook.database import mysql

from pseudobook.models import user as user_model
from pseudobook.models import advertisement as ads_model
from pseudobook.models import sale as sale_model
from pseudobook.models import revenue as rev_model

ITEMS_PER_PAGE = 15

'''
Setup Blueprint
'''
mod = Blueprint('manager', __name__, template_folder='../templates/manager')

'''
Routes
'''
@mod.route('/manager/reports', methods=['GET'])
@login_required
def reports():
    ad_columns = ads_model.searchable_ad_columns.keys()
    sale_columns = sale_model.searchable_sale_columns.keys()

    months_with_ads = ads_model.Advertisement.get_months_with_ads()
    months_with_sales = sale_model.Sale.get_months_with_sales()
    return render_template('reports.html',
        ad_columns=ad_columns,
        sale_columns=sale_columns,
        months_with_ads=months_with_ads,
        months_with_sales=months_with_sales)

@mod.route('/manager/reports/getads', methods=['POST'])
def getads():
    year = request.json['year']
    month = request.json['month']
    searchcol = request.json['searchcol']
    search = request.json['search']

    ads = ads_model.Advertisement.scroll_ads(0, ITEMS_PER_PAGE, searchcol, search, year, month)
    return json.dumps([o.__dict__ for o in ads])

@mod.route('/manager/reports/getsales', methods=['POST'])
def getsales():
    year = request.json['year']
    month = request.json['month']
    searchcol = request.json['searchcol']
    search = request.json['search']

    sales = sale_model.Sale.scroll_sales(0, ITEMS_PER_PAGE, searchcol, search, year, month)
    return json.dumps([o.__dict__ for o in sales])

@mod.route('/manager/reports/getrevenue', methods=['POST'])
def getrevenue():
    year = request.json['year']
    month = request.json['month']
    search = request.json['search']
    revenuetype = request.json['revenuetype']
    try:
        revenuetype = int(revenuetype) if revenuetype else 1
        revenuetype = rev_model.REVENUE_REPORT_TYPES(revenuetype)
    except:
        revenuetype = rev_model.REVENUE_REPORT_TYPES.Item

    revenues = rev_model.Revenue.scroll_revenues(0, ITEMS_PER_PAGE, revenuetype, search, year, month)
    return json.dumps([o.__dict__ for o in revenues])