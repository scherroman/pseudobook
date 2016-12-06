from enum import Enum
from pseudobook.database import mysql, MySQL
from pseudobook.models import user as user_model

searchable_sale_columns = dict()
searchable_sale_columns['Item Name'] = 'ItemName'
searchable_sale_columns['Item Type'] = 'ItemType'
searchable_sale_columns['Company'] = 'Company'
searchable_sale_columns['Ad Posted By'] = 'CustomerRepName'
searchable_sale_columns['Customer'] = 'CustomerName'

class REVENUE_REPORT_TYPES(Enum):
    Item = 1
    ItemType = 2
    Customer = 3
    Employee = 4

class Sale():
    def __init__(self, ItemName, ItemType, ItemID, Company, Price, CustomerRepName, CustomerRepID, CustomerName, CustomerID, CustomerEmail, CustomerAccountNumber, UnitsSold, TransactionDateTime, TransactionID):
        self.itemName = ItemName
        self.itemType = ItemType
        self.itemID = ItemID
        self.company = Company
        self.price = Price
        self.customerRepName = CustomerRepName
        self.customerRepID = CustomerRepID
        self.customerName = CustomerName
        self.customerID = CustomerID
        self.customerEmail = CustomerEmail
        self.customerAccountNumber = CustomerAccountNumber
        self.unitsSold = UnitsSold
        self.transactionDateTime = TransactionDateTime
        self.transactionID = TransactionID

    def __repr__(self):
        return ('{{transactionID: {}, adID: {}, buyerID: {}, buyerAccount: {}}}').format(
                self.transactionID,
                self.adID,
                self.buyerID,
                self.buyerAccount
        )
    
    @staticmethod
    def scroll_sales(offset, num_sales, search):
        search = search if search else ""
        sales = []

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT *
                          FROM SalesReport
                          ORDER BY TransactionID
                          LIMIT {0} OFFSET {1}
                          '''.format(num_sales, offset * num_sales))
         
        results = cursor.fetchall()
        
        for result in results:
            sale = Sale.sale_from_dict(result) if result else None
            sales.append(sale)

        return sales

    @staticmethod
    def scroll_revenues(offset, num_items, search, reportType):
        search = search if search else ""
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
                          GROUP BY {1}
                          ORDER BY SUM(Price * UnitsSold) DESC
                          LIMIT {2} OFFSET {3}
                          '''.format(extractedAttr, groupByAttr, num_items, offset * num_items))

        results = cursor.fetchall()

        for result in results:
            revenue = Sale.revenue_from_dict(result) if result else None
            revenues.append(revenue)

        return revenues

    @staticmethod
    def sale_from_dict(sale_dict):
        return Sale(sale_dict.get('ItemName'),
            sale_dict.get('ItemType'),
            sale_dict.get('ItemID'),
            sale_dict.get('Company'),
            sale_dict.get('Price'),
            sale_dict.get('CustomerRepName'),
            sale_dict.get('CustomerRepID'),
            sale_dict.get('CustomerName'),
            sale_dict.get('CustomerID'),
            sale_dict.get('CustomerEmail'),
            sale_dict.get('CustomerAccountNumber'),
            sale_dict.get('UnitsSold'),
            sale_dict.get('TransactionDateTime'),
            sale_dict.get('TransactionID')
        )

    @staticmethod
    def revenue_from_dict(revenue_dict):
        # return a tuple instead of class instance because different report types will give different meanings to values
        return (revenue_dict.get('Name'),
            "%.2f" % revenue_dict.get('Revenue'))