from flask import Blueprint, abort
from flask import render_template, url_for, request, redirect 
from flask_login import login_required, current_user
import json

from pseudobook.database import mysql

from pseudobook.models import user as user_model
from pseudobook.models import advertisement as ads_model
from pseudobook.models import sale as sale_model

ITEMS_PER_PAGE = 15

'''
Setup Blueprint
'''
mod = Blueprint('manager', __name__, template_folder='../templates/manager')

'''
Routes
'''
@mod.route('/reports', methods=['GET'])
@login_required
def reports():
    revenuetype = request.values.get('revenuetype')
    try:
        revenuetype = int(revenuetype) if revenuetype else 1
        revenuetype = sale_model.REVENUE_REPORT_TYPES(revenuetype)
    except:
        print("Bad request.")
        revenuetype = sale_model.REVENUE_REPORT_TYPES.Item
    
    year = request.values.get('year')
    month = request.values.get('month')
    try:
        year = int(year) if year else 0
        month = int(month) if month else 0
    except:
        print("Bad request.")
        year = 0
        month = 0
    
    all_ads = ads_model.Advertisement.scroll_ads(0, ITEMS_PER_PAGE, "", "")
    all_sales = sale_model.Sale.scroll_sales(0, ITEMS_PER_PAGE, "")
    all_revenues = sale_model.Sale.scroll_revenues(0, ITEMS_PER_PAGE, "", revenuetype)

    ad_columns = ads_model.searchable_ad_columns.keys()
    sale_columns = []
    revenue_columns = []

    months = getAvailableMonths(all_sales)
    return render_template('reports.html',
        all_ads=all_ads,
        all_sales=all_sales,
        all_revenues=all_revenues,
        ad_columns=ad_columns,
        sale_columns=sale_columns,
        revenue_columns=revenue_columns,
        months=months)

@mod.route('/reports/getads', methods=['POST'])
def getads():
    year = request.json['year']
    month = request.json['month']
    searchcol = request.json['searchcol']
    search = request.json['search']

    deal = ads_model.Advertisement.scroll_ads(0, ITEMS_PER_PAGE, searchcol, search)
    newdeal = json.dumps([o.__dict__ for o in deal])
    return newdeal

'''
Helpers
'''
def getAvailableMonths(all_sales):
    rawMonths = []

    for sale in all_sales:
        yearMonth = (sale.transactionDateTime.year, sale.transactionDateTime.month)
        if yearMonth not in rawMonths:
            rawMonths.append(yearMonth)
    
    intToMonth = ["","Jan","Feb","March","April","May","June","July","Aug","Sep","Oct","Nov","Dec"]

    months = []
    for month in sorted(rawMonths):
        months.append((month, str(month[0]) + " " + intToMonth[month[1]]))
    
    return months