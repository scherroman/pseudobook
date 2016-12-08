from pseudobook.database import mysql, MySQL
from pseudobook.models import user as user_model

searchable_sale_columns = dict()
searchable_sale_columns['Item Name'] = 'ItemName'
searchable_sale_columns['Company'] = 'Company'
searchable_sale_columns['Ad Posted By'] = 'CustomerRepName'
searchable_sale_columns['Customer'] = 'CustomerName'

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
        self.transactionDateTime = str(TransactionDateTime)
        self.transactionID = TransactionID

    def __repr__(self):
        return ('{{transactionID: {}, adID: {}, buyerID: {}, buyerAccount: {}}}').format(
                self.transactionID,
                self.adID,
                self.buyerID,
                self.buyerAccount
        )
    
    @staticmethod
    def scroll_sales(offset, num_sales, searchcol, search, year, month):
        if not searchcol in searchable_sale_columns.keys():
            searchcol = 'Item Name'
        searchcol = searchable_sale_columns[searchcol]
        search = search if search else ""

        if year.isdigit():
            year = "AND YEAR(TransactionDateTime) = " + year
        else:
            year = ""
        if month.isdigit():
            month = "AND MONTH(TransactionDateTime) = " + month
        else:
            month = ""
        sales = []

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT *
                          FROM SalesReport
                          WHERE {0} LIKE \'%{1}%\'
                            {2}
                            {3}
                          ORDER BY TransactionID
                          LIMIT {4} OFFSET {5}
                          '''.format(searchcol, search, year, month, num_sales, offset * num_sales))
         
        results = cursor.fetchall()
        
        for result in results:
            sale = Sale.sale_from_dict(result) if result else None
            sales.append(sale)

        return sales

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
    def get_months_with_sales():
        rawMonths = []
        months = []

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT TransactionDateTime
                          FROM SalesReport S
                          ''')
        
        results = cursor.fetchall()

        for result in results:
            date = result.get('TransactionDateTime')
            yearMonth = (date.year, date.month)
            if yearMonth not in rawMonths:
                rawMonths.append(yearMonth)

        intToMonth = ["","Jan","Feb","March","April","May","June","July","Aug","Sep","Oct","Nov","Dec"]

        for month in sorted(rawMonths):
            months.append((str(month[0])+","+str(month[1]), str(month[0]) + " " + intToMonth[month[1]]))

        return months