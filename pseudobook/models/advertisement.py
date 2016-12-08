from pseudobook.database import mysql, MySQL
from pseudobook.models import user as user_model

searchable_ad_columns = dict()
searchable_ad_columns['Item Name'] = 'A.itemName'
searchable_ad_columns['Type'] = 'A.adType'
searchable_ad_columns['Company'] = 'A.company'
searchable_ad_columns['Posted By'] = 'CONCAT(E.firstName,\' \',E.lastName)'

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
        self.unitPrice = unitPrice
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
    def scroll_ads(offset, num_ads, searchcol, search, year, month):
        if not searchcol in searchable_ad_columns.keys():
            searchcol = 'Item Name'
        searchcol = searchable_ad_columns[searchcol]
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
                          FROM Advertisement AS A, User As E
                          WHERE A.employeeID = E.userID
                            AND {0} LIKE \'%{1}%\'
                            {2}
                            {3}
                          ORDER BY A.adID
                          LIMIT {4} OFFSET {5}
                          '''.format(searchcol, search, year, month, num_ads, offset * num_ads))
        
        results = cursor.fetchall()
        
        for result in results:
            ad = Advertisement.ad_from_dict(result) if result else None
            ads.append(ad)

        return ads

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