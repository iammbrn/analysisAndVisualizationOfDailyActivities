import sqlite3
import time
import re


class LinkDatabase():

    def __init__(self):
        self.createConnectWithDatabase()

    def createConnectWithDatabase(self):
        self.connect = sqlite3.connect("LinkDatabase.db")
        self.cursor = self.connect.cursor()

        self.cursor.execute("Create Table If Not Exists LinkDatabase(deviceType TEXT, statsAccessLink TEXT)")
        self.connect.commit()

    def addDataToDatbase(self, deviceType, statsAccessLink):
        self.cursor.execute("Insert Into LinkDatabase Values(?,?)", (deviceType, statsAccessLink))
        self.connect.commit()

    def deleteDataFromDatabase(self, devcieType, statsAccessLink):
        self.cursor.execute("Delete From LinkDatabase Where deviceType=? And statsAccessLink=?", (deviceType, statsAccessLink))

        self.connect.commit()

    def getDataFromDatabase(self):
        self.cursor.execute("Select * From LinkDatabase")
        data = self.cursor.fetchall()
        return data

    def closeConnection(self):
        self.connect.close()


class LinkExtractionFromDatabase(LinkDatabase):

    def __init__(self):
        super().__init__()

    def linkExtractionFromDatabase(self):
        data = self.getDataFromDatabase()
        urlList = list()

        for deviceType, url in data:
            access_link_match = re.search(r'<url>(.*?)</url>', url, re.IGNORECASE)

            if access_link_match:
                urlList.append((deviceType, access_link_match.group(1)))

        return urlList


print("Dear user, what would you like to do?\n"
      "If the operation is 'q', the program will terminate.\n"
      "If the operation is '1', new data will be added to the database.\n"
      "If the operation is '2', access links are retrieved as a list from the device types and URLs of the data in the database.\n"
      "If the operation is '3', we can delete the data we want by entering the data we want to delete from the database.\n")

if __name__ == "__main__":
    object = LinkExtractionFromDatabase()

    while True:
        operation = input("Operation=")

        if operation == "q":
            try:
                object.closeConnection()
                print("The program is being terminated...")
                time.sleep(2)
                print("The program has terminated.")
                break

            except Exception as e:
                print("Error! The program could not terminate.")
                print(e)

        elif operation == "1":
            try:
                deviceType = input("devcieType=")
                statsAccessLink = input("statsAccessLink=")
                print("The data is being added to the database...")
                time.sleep(2)
                object.addDataToDatbase(deviceType, statsAccessLink)
                print("The data has been added to the database.")

            except Exception as e:
                print("Error! The data could not be added to the database.")
                print(e)

        elif operation == "2":
            try:
                print("The data is being retrieved from the database...")
                time.sleep(2)
                print(object.linkExtractionFromDatabase())
                print("The data has been retrieved from the database.")

            except Exception as e:
                print("Error! The data could not be retrieved from the database.")
                print(e)

        elif operation == "3":
            try:
                deviceType = input("devcieType=")
                statsAccessLink = input("statsAccessLink=")
                print("The data is being deleted from the database...")
                time.sleep(2)
                object.deleteDataFromDatabase(deviceType, statsAccessLink)
                print("The data has been deleted from the database.")

            except Exception as e:
                print("Error! The data could not be deleted from the database.")
                print(e)
        else:
            print("Error! Please enter the correct operation you want to perform.")