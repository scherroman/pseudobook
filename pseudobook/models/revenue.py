from enum import Enum
from pseudobook.database import mysql, MySQL
from pseudobook.models import user as user_model

class REVENUE_REPORT_TYPES(Enum):
    Item = 0
    ItemType = 1
    Customer = 2
    Employee = 3

class Revenue():
    def __init__(self, Name, Revenue):
        self.name = Name
        self.revenue = "%.2f" % Revenue

    def __repr__(self):
        return ('{{name: {}, revenue: {}}}').format(
                self.name,
                self.revenue
        )

    @staticmethod
    def scroll_revenues(offset, num_items, reportType, search, year, month):
        search = search if search else ""

        if year.isdigit():
            year = "AND YEAR(TransactionDateTime) = " + year
        else:
            year = ""
        if month.isdigit():
            month = "AND MONTH(TransactionDateTime) = " + month
        else:
            month = ""
        revenues = []

        extractedAttr = ""
        groupByAttr = ""

        if reportType == REVENUE_REPORT_TYPES.Item:
            extractedAttr = "ItemName"
            groupByAttr = "ItemID"
        elif reportType == REVENUE_REPORT_TYPES.ItemType:
            extractedAttr = "ItemType"
            groupByAttr = "ItemType"
        elif reportType == REVENUE_REPORT_TYPES.Customer:
            extractedAttr = "CustomerName"
            groupByAttr = "CustomerID"
        elif reportType == REVENUE_REPORT_TYPES.Employee:
            extractedAttr = "CustomerRepName"
            groupByAttr = "CustomerRepID"

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT {0} AS Name, SUM(Price * UnitsSold) AS Revenue
                          FROM SalesReport
                          WHERE {0} LIKE \'%{1}%\'
                            {2}
                            {3}
                          GROUP BY {4}
                          ORDER BY SUM(Price * UnitsSold) DESC
                          LIMIT {5} OFFSET {6}
                          '''.format(extractedAttr, search, year, month, groupByAttr, num_items, offset * num_items))

        results = cursor.fetchall()

        for result in results:
            revenue = Revenue.revenue_from_dict(result) if result else None
            revenues.append(revenue)

        return revenues

    @staticmethod
    def revenue_from_dict(revenue_dict):
        return Revenue(revenue_dict.get('Name'),
            revenue_dict.get('Revenue'))