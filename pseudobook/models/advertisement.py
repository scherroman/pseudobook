from pseudobook.database import mysql, MySQL
from pseudobook.models import user as user_model

searchable_columns = dict()
searchable_columns['Item Name'] = 'A.itemName'
searchable_columns['Type'] = 'A.adType'
searchable_columns['Company'] = 'A.company'
searchable_columns['Posted By'] = 'CONCAT(E.firstName,\' \',E.lastName)'

class Advertisement():
    def __init__(self, adID, employeeID, employeeName, adType, datePosted, company, itemName, content, unitPrice, numberAvailableUnits):
        self.adID = adID
        self.employeeID = employeeID
        self.employeeName = employeeName
        self.adType = adType
        self.datePosted = str(datePosted)
        self.company = company
        self.itemName = itemName
        self.content = content
        self.unitPrice = "%.2f" % unitPrice
        self.numberAvailableUnits = numberAvailableUnits
    
    def __repr__(self):
        return '{"itemName": "%s", "employeeName": "%s", "adType": "%s", "datePosted": "%s", "company": "%s", "unitPrice": "%s", "numberAvailableUnits": "%s"}' % (
            self.itemName,
            self.employeeName,
            self.adType,
            self.datePosted,
            self.company,
            self.unitPrice,
            self.numberAvailableUnits
        )

    @staticmethod
    def create_new_ad(employeeID, itemName, itemType, company, content, price, numberAvailableUnits):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''CALL createAd(@adID, "{}", "{}", "{}", "{}", "{}", "{}", "{}")
                              '''.format(employeeID, itemType, company, itemName, content, price, numberAvailableUnits))
            mysql.connection.commit()
            cursor.execute('''SELECT @adID''')
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            raise
        else:
            result = cursor.fetchone()
            adID = result.get('@adID') if result else None
            
        return adID

    '''
    Standard search method for ads
    '''
    @staticmethod
    def scroll_ads(offset, num_ads, searchcol, search, year, month):
        if not searchcol in searchable_columns.keys():
            searchcol = 'Item Name'
        searchcol = searchable_columns[searchcol]
        search = search if search else ""

        if year.isdigit():
            year = "AND YEAR(A.datePosted) = " + year
        else:
            year = ""
        if month.isdigit():
            month = "AND MONTH(A.datePosted) = " + month
        else:
            month = ""
        ads = []

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT A.adID, A.employeeID, CONCAT(E.firstName,\' \',E.lastName) AS employeeName, A.adType, A.datePosted, A.company, A.itemName, A.content, A.unitPrice, A.numberAvailableUnits
                          FROM Advertisement AS A, User AS E
                          WHERE A.employeeID = E.userID
                            AND {0} LIKE \'%{1}%\'
                            {2}
                            {3}
                          ORDER BY A.adID
                          -- LIMIT {4} OFFSET {5}
                          '''.format(searchcol, search, year, month, num_ads, offset * num_ads))
        
        results = cursor.fetchall()
        
        for result in results:
            ad = Advertisement.ad_from_dict(result) if result else None
            ads.append(ad)

        return ads
    
    '''
    Get all ads made by the given user
    '''
    @staticmethod
    def get_ads_made_by_user(offset, num_ads, userID):
        ads = []

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT A.adID, A.employeeID, CONCAT(E.firstName,\' \',E.lastName) AS employeeName, A.adType, A.datePosted, A.company, A.itemName, A.content, A.unitPrice, A.numberAvailableUnits
                          FROM Advertisement AS A, User AS E
                          WHERE A.employeeID = E.userID
                            AND A.employeeID = {0}
                          ORDER BY A.adID
                          -- LIMIT {1} OFFSET {2}
                          '''.format(userID, num_ads, offset * num_ads))
        
        results = cursor.fetchall()
        
        for result in results:
            ad = Advertisement.ad_from_dict(result) if result else None
            ads.append(ad)

        return ads

    '''
    Get item suggestions for a particular user
    i.e. items sold by a company that the user has purchased from before
    '''
    @staticmethod
    def get_suggestions_for_user(offset, num_ads, userID, searchcol, search):
        if not searchcol in searchable_columns.keys():
            searchcol = 'Item Name'
        searchcol = searchable_columns[searchcol]
        search = search if search else ""
        ads = []

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT DISTINCT A.adID, A.employeeID, S.CustomerRepName as employeeName, A.adType, A.datePosted, A.company, A.itemName, A.content, A.unitPrice, A.numberAvailableUnits
                          FROM Advertisement A
                          JOIN SalesReport S ON A.company = S.Company
                          WHERE S.CustomerID = {0}
                            AND {1} LIKE \'%{2}%\'
                          ORDER BY A.adID
                          -- LIMIT {3} OFFSET {4}
                          '''.format(userID, searchcol, search, num_ads, offset * num_ads))
        
        results = cursor.fetchall()
        
        for result in results:
            ad = Advertisement.ad_from_dict(result) if result else None
            ads.append(ad)

        return ads
    
    '''
    Get "best selling" items
    i.e. all items, ordered by their total amount purchased
    '''
    @staticmethod
    def get_best_sellers(offset, num_ads, searchcol, search):
        if not searchcol in searchable_columns.keys():
            searchcol = 'Item Name'
        searchcol = searchable_columns[searchcol]
        search = search if search else ""
        ads = []

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT A.adID, A.employeeID, CONCAT(E.firstName,\' \',E.lastName) AS employeeName, A.adType, A.datePosted, A.company, A.itemName, A.content, A.unitPrice, A.numberAvailableUnits
                          FROM Advertisement AS A, User AS E, Sales AS S
                          WHERE A.employeeID = E.userID AND S.adID = A.adID
                            AND {0} LIKE \'%{1}%\'
                          GROUP BY A.adID
                          ORDER BY SUM(S.numberOfUnits) DESC
                          -- LIMIT {2} OFFSET {3}
                          '''.format(searchcol, search, num_ads, offset * num_ads))
        
        results = cursor.fetchall()
        
        for result in results:
            ad = Advertisement.ad_from_dict(result) if result else None
            ads.append(ad)

        return ads

    @staticmethod
    def get_ad_by_id(adID):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT SELECT A.adID, A.employeeID, CONCAT(E.firstName,\' \',E.lastName) AS employeeName, A.adType, A.datePosted, A.company, A.itemName, A.content, A.unitPrice, A.numberAvailableUnits
                          FROM Advertisement A, User E
                          WHERE A.adID = {0}
                          '''.format(adID))
        result = cursor.fetchone()
        ad = ad_from_dict(result) if result else None
        return ad

    '''
    Create an Advertisement object from a row retrieved from the database
    '''
    @staticmethod
    def ad_from_dict(ad_dict):
        return Advertisement(ad_dict.get('adID'),
            ad_dict.get('employeeID'),
            ad_dict.get('employeeName'),
            ad_dict.get('adType'),
            ad_dict.get('datePosted'),
            ad_dict.get('company'),
            ad_dict.get('itemName'),
            ad_dict.get('content'),
            ad_dict.get('unitPrice'),
            ad_dict.get('numberAvailableUnits')
        )
    
    '''
    Get all months in which ads were posted
    '''
    @staticmethod
    def get_months_with_ads():
        rawMonths = []
        months = []

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT A.datePosted
                          FROM Advertisement AS A
                          ''')
        
        results = cursor.fetchall()

        for result in results:
            date = result.get('datePosted')
            yearMonth = (date.year, date.month)
            if yearMonth not in rawMonths:
                rawMonths.append(yearMonth)

        intToMonth = ["","Jan","Feb","March","April","May","June","July","Aug","Sep","Oct","Nov","Dec"]

        for month in sorted(rawMonths):
            months.append((str(month[0])+","+str(month[1]), str(month[0]) + " " + intToMonth[month[1]]))

        return months