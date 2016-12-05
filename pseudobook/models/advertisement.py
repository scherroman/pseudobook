from pseudobook.database import mysql, MySQL

from pseudobook.models import user as user_model

class Advertisement():
    def __init__(self, adID, employeeID, adType, datePosted, company, itemName, content, unitPrice, numberAvailableUnits):
        self.adID = adID
        self.employeeID = employeeID
        associatedEmployee = user_model.User.get_user_by_id(employeeID)
        self.associatedEmployeeName = associatedEmployee.firstName + " " + associatedEmployee.lastName
        self.adType = adType
        self.datePosted = datePosted
        self.company = company
        self.itemName = itemName
        self.content = content
        self.unitPrice = unitPrice
        self.numberAvailableUnits = numberAvailableUnits

    def __repr__(self):
        return ('{{id: {}, name: {}, company: {}}').format(
                self.adID,
                self.itemName,
                self.company
        )
    
    @staticmethod
    def scroll_ads(offset, num_ads, search):
        search = search if search else ""
        ads = []
        
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT A.adID, A.employeeID, A.adType, A.datePosted, A.company, A.itemName, A.content, A.unitPrice, A.numberAvailableUnits
                          FROM Advertisement AS A
                          WHERE A.itemName LIKE \'{0}%\'
                          ORDER BY A.adID
                          LIMIT {1} OFFSET {2}
                          '''.format(search, num_ads, offset * num_ads))
        # WHERE 
        results = cursor.fetchall()
        
        for result in results:
            ad = Advertisement.ad_from_dict(result) if result else None
            ads.append(ad)

        return ads

    @staticmethod
    def ad_from_dict(ad_dict):
        return Advertisement(ad_dict.get('adID'),
            ad_dict.get('employeeID'),
            ad_dict.get('adType'),
            ad_dict.get('datePosted'),
            ad_dict.get('company'),
            ad_dict.get('itemName'),
            ad_dict.get('content'),
            ad_dict.get('unitPrice'),
            ad_dict.get('numberAvailableUnits')
        )