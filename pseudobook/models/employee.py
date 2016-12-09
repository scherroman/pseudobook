from pseudobook.database import mysql, MySQL

class Employee():
    def __init__(self, userID, SSN, startDate, hourlyRate, firstName, lastName, email, passwordHash):
        self.userID = userID
        self.SSN = SSN
        self.startDate = startDate
        self.hourlyRate = hourlyRate
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password_hash = passwordHash

    @staticmethod
    def scroll_employees(offset, num_employees):
        employees = []
        
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT E.userID, E.SSN, E.startDate, E.hourlyRate, U.firstName, U.lastName, U.email, U.passwordHash
                          FROM Employee E, User U
                          WHERE E.userID = U.userID
                          ORDER BY U.firstName
                          LIMIT {0} OFFSET {1}
                          '''.format(num_employees, offset * num_employees))
        results = cursor.fetchall()
        
        for result in results:
            employee = Employee.employee_from_dict(result) if result else None
            employees.append(employee)

        return employees

    @staticmethod
    def count_employees():
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT COUNT(*) AS count
                          FROM Employee E
                          '''.format())
        results = cursor.fetchone()
        count = results.get('count')

        return count

    @staticmethod
    def get_employee_by_id(userID):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT E.userID, E.SSN, E.startDate, E.hourlyRate, U.firstName, U.lastName, U.email, U.passwordHash
                          FROM Employee E, User U
                          WHERE E.userID = U.userID AND E.userID = {0}
                          '''.format(userID))
        result = cursor.fetchone()
        employee = Employee.employee_from_dict(result) if result else None
        return employee

    @staticmethod
    def employee_from_dict(e_dict):
        return Employee(e_dict.get('userID'),
            e_dict.get('SSN'),
            e_dict.get('startDate'),
            e_dict.get('hourlyRate'),
            e_dict.get('firstName'),
            e_dict.get('lastName'),
            e_dict.get('email'),
            e_dict.get('passwordHash'))