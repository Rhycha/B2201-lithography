import sqlite3
import datetime
from time import sleep
##################
# DB Start
##################


class SQLite():
    # class attribute

    def __init__(self, DB='test'):
        SQLite.DB = DB+'.db'

    # ------------------------------------------------------
    def connect(self):
        try:
            conn = sqlite3.connect(SQLite.DB)
            cursor = conn.cursor()
        except Exception as ex:
            print(f"Connection error : {ex}")
        return conn, cursor



    #---------------------------------------------
    def connect_without_detect_types(self):
        try:
            conn = sqlite3.connect('LITHO_package/StudentAssignment.db')
            cursor = conn.cursor()

        except Exception as ex:
            print(f"Connection error : {ex}")
        return conn, cursor


    #-------------------------------------------------------
    # Make the database connection with detect_types
    def connect_with_detect_types(self):
        try:
            conn = sqlite3.connect(SQLite.DB,
                             detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES)
            cursor = conn.cursor()

        except Exception as ex:
            print(f"Connection error : {ex}")
        return conn, cursor


    # ------------------------------------------------------
    def dropTables(self):
        # connect to SQLite
        conn, cursor = self.connect()

        try:
            cursor.execute("DROP TABLE IF EXISTS Quoations2")
            cursor.execute("DROP TABLE IF EXISTS Quotations2")
            cursor.execute("DROP TABLE Quotations")
            cursor.execute("DROP TABLE Books")
            print("Drop successful")
        except Exception as ex:
            print(f"Error : {ex}")
        # close cursor and connection
        self.close(cursor, conn)

    def dropTrials(self):
        # connect to SQLite
        conn, cursor = self.connect()

        try:
            cursor.execute("DROP TABLE IF EXISTS Trials")
            print("Drop successful")
        except Exception as ex:
            print(f"Error : {ex}")
        # close cursor and connection


    def dropMeasures(self):
        # connect to SQLite
        conn, cursor = self.connect()

        try:
            cursor.execute("DROP TABLE IF EXISTS Measures")
            print("Drop successful")
        except Exception as ex:
            print(f"Error : {ex}")
        # close cursor and connection



    def dropASSIGN(self):
        # connect to SQLite
        # conn, cursor = self.connect_with_detect_types()
        conn, cursor = self.connect_without_detect_types()

        try:
            cursor.execute("DROP TABLE IF EXISTS ASSIGNMENT")
            print("Drop successful")
        except Exception as ex:
            print(f"Error : {ex}")
        # close cursor and connection


    def close(self, cursor, conn):
        # close cursor
        cursor.close()

        # close connection to SQLite
        conn.close()

    # ------------------------------------------------------
    def createTables(self):
        # connect to SQLite
        conn, cursor = self.connect()

        try:
            # create Table inside DB
            cursor.execute("CREATE TABLE IF NOT EXISTS Books (       \
                  Book_id INTEGER  AUTO_INCREMENT, \
                  Book_Title TEXT,     \
                  Book_Page INTEGER,              \
                  PRIMARY KEY (Book_id)                \
                );")

            # create second Table inside DB
            print("Create successful")
            cursor.execute("CREATE TABLE IF NOT EXISTS Quotations ( \
                    Quote_id INTEGER AUTO_INCREMENT,      \
                    Quotation TEXT,           \
                    Books_Book_id INTEGER,                \
                    PRIMARY KEY (Quote_id),           \
                    FOREIGN KEY (Books_Book_id)       \
                        REFERENCES Books(Book_id)     \
                        ON DELETE CASCADE             \
                );")


        except Exception as ex:
            print(f"Error : {ex}")
        # close cursor and connection
        self.close(cursor, conn)

    def createASSIGNTable(self):

        # conn, cursor = self.connect_with_detect_types()
        conn, cursor = self.connect_without_detect_types()


        createTable = '''CREATE TABLE IF NOT EXISTS ASSIGNMENT (
            StudentId INTEGER,
            StudentName VARCHAR(100),
            SubmissionDate TIMESTAMP);'''
        cursor.execute(createTable)

    #------------------------------------------------------
    def createLithoTable(self):
        # connect to SQLite
        conn, cursor = self.connect()

        try:
            # create Table inside DB
            cursor.execute("CREATE TABLE IF NOT EXISTS Trials (       \
                              ExposureTime REAL,     \
                              ExposureEnergy INTEGER,              \
                              Power REAL,                \
                              StartTime TIMESTAMP,                \
                              StopTime TIMESTAMP                  \
                    );")

            # create second Table inside DB
            cursor.execute("CREATE TABLE IF NOT EXISTS Measures ( \
                    Trials_Trial_id INTEGER,                \
                    Current REAL,				\
                    Sensor REAL,				\
                    Opstatus TEXT,			\
                    MeasuringTime	TIMESTAMP,		\
                    Temperature	REAL,		\
                    FOREIGN KEY (Trials_Trial_id)       \
                        REFERENCES Trials(rowid)     \
                        ON DELETE CASCADE             \
                );")

            cursor.execute("PRAGMA foreign_keys = 1")
            # cursor.execute("CREATE TABLE IF NOT EXISTS LITHODB ( \

            print("Create successful")

        except Exception as ex:
            print(f"Error : {ex}")
        # close cursor and connection
        self.close(cursor, conn)

    #-------------------------------------------------------
    def getmax_Trial_id(self):
        conn, cursor = self.connect()

        try:
            cursor.execute('SELECT max(rowid) FROM Trials')
            max_Trial_id = cursor.fetchone()[0]
            if max_Trial_id:
                return max_Trial_id
            else:
                return 1
        except Exception as ex:
            print(f"Error : {ex}")
        # close cursor and connection

        finally:
            self.close(cursor, conn)

    #-------------------------------------------------------------------
    def insertTrialIntoTable(self, ExposureTime=-1, ExposureEnergy=-1, Power=-1, StartTime = datetime.datetime.now()):
    #Trial_id는 autoincrement여서 인수로 넣어주지 않아도 된다.
        conn, cursor = self.connect()

        try:

            sqlite_insert_with_param = """INSERT INTO Trials
                              (ExposureTime, ExposureEnergy, Power, StartTime)
                              VALUES (?, ?, ?, ?);"""

            insert_data_tuple = (ExposureTime, ExposureEnergy, Power, StartTime)
            cursor.execute(sqlite_insert_with_param, insert_data_tuple)
            self.Trial_id = cursor.lastrowid
            print(f"before commit Trialid : {self.Trial_id}")
            conn.commit()
            self.Trial_id = cursor.lastrowid

            print(f"after commit Trialid : {self.Trial_id}")

            print("Python Variables inserted successfully into table")

        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)

        finally:
            self.close(cursor, conn)

    # --------------------------------------------------------
    def updateTrial(self,StopTime=datetime.datetime.now()):
        conn, cursor = self.connect()

        try:
            sqlite_update_with_param = ''' UPDATE Trials
              SET StopTime = ? 
              WHERE rowid = ?'''
            update_data_tuple = (StopTime, self.Trial_id)
            cursor.execute(sqlite_update_with_param, update_data_tuple)
            conn.commit()
        except sqlite3.Error as error:
            print("Failed to update Python variable into sqlite table", error)

        finally:
            self.close(cursor, conn)


    # ----------------------------------------------------
    def insertMeasureIntoTable(self, Current= -1, Sensor = -1, Opstatus="", Temperature=-1, MeasuringTime=datetime.datetime.now()):
        conn, cursor = self.connect()

        try:
            print("Start insertMeasureIntoTable")

            sqlite_insert_with_param = """INSERT INTO Measures
                               (Trials_Trial_id, Current, Sensor, Opstatus, MeasuringTime, Temperature)
                               VALUES (?, ?, ?, ?, ?, ?);"""

            insert_data_tuple = (self.Trial_id, Current, Sensor, Opstatus, MeasuringTime, Temperature)
            cursor.execute(sqlite_insert_with_param, insert_data_tuple)

            conn.commit()

            print("End insertMeasureIntoTable")

        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)

        finally:
            self.close(cursor, conn)

    # ------------------------------------------------------
    def showTables(self):
        # connect to SQLite
        conn, cursor = self.connect()

        # show Tables from guidb DB
        cursor.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
        print(cursor.fetchall())

        # close cursor and connection
        self.close(cursor, conn)

        # ------------------------------------------------------

    def insertBooks(self, title, page, bookQuote):
        # connect to SQLite
        conn, cursor = self.connect()

        #
        sql = ''' INSERT INTO books(Book_Title,Book_Page)
                  VALUES(?,?) '''

        # insert data
        cursor.execute(sql, (title, page))

        # last inserted auto increment value
        keyID = cursor.lastrowid
        # print(keyID)

        cursor.execute("INSERT INTO quotations (Quotation, Books_Book_id) VALUES (?, ?)", \
                       (bookQuote, keyID))

        # commit transaction
        conn.commit()

        # close cursor and connection
        self.close(cursor, conn)

    # -----------------------------------------------------
    def insertASSIGN(self):
        # conn, cursor = self.connect_with_detect_types()
        conn, cursor = self.connect_without_detect_types()

        currentDateTime = datetime.datetime.now()
        insertQuery = """INSERT INTO ASSIGNMENT
            VALUES (?, ?, ?);"""

        cursor.execute(insertQuery, (1, "Virat Kohli",
                                     currentDateTime))
        cursor.execute(insertQuery, (2, "Rohit Pathak",
                                     currentDateTime))

        conn.commit()

        self.close(cursor, conn)

    # ------------------------------------------------------
    def insertBooksExample(self):
        # connect to SQLite
        conn, cursor = self.connect()

        # insert hard-coded data
        cursor.execute("INSERT INTO books (Book_Title, Book_Page) VALUES ('Design Patterns', 17)")

        # last inserted auto increment value
        keyID = cursor.lastrowid
        print(keyID)

        cursor.execute("INSERT INTO quotations (Quotation, Books_Book_id) VALUES (?, ?)", \
                       ('Programming to an Interface, not an Implementation', keyID))

        # commit transaction
        conn.commit()

        # close cursor and connection
        self.close(cursor, conn)

    # ------------------------------------------------------
    def showBooks(self):
        # connect to SQLite
        conn, cursor = self.connect()
        print(f"\nSTART ShowBooks\n")
        try :
            # print results
            cursor.execute("SELECT * FROM Books")
            allBooks = cursor.fetchall()
            print(allBooks)
        except Exception as ex:
            print(f"showBooks Exception : {ex}")

        print(f"\nEnd ShowBooks\n")

        # close cursor and connection
        self.close(cursor, conn)

        return allBooks

        # ------------------------------------------------------

    def showTrials(self):
        # connect to SQLite
        conn, cursor = self.connect()
        print(f"\nSTART ShowTrials\n")
        try:
            from pprint import pprint
            # print results
            cursor.execute("SELECT * FROM Trials")
            allTrials = cursor.fetchall()
            pprint(allTrials)

            return allTrials

        except Exception as ex:
            print(f"showTrials Exception : {ex}")

        finally:
            self.close(cursor, conn)

        print(f"\nEnd ShowTrials\n")

        # close cursor and connection

    # ------------------------------------------
    def showMeasures(self):
        # connect to SQLite
        conn, cursor, = self.connect_with_detect_types()

        print(f"\nSTART ShowMeasures\n")
        try:
            # print results
            cursor.execute("SELECT * FROM Measures")
            allMeasures = cursor.fetchall()
            print(allMeasures)

            return allMeasures

        except Exception as ex:
            print(f"showMeasures Exception : {ex}")

        finally:
            self.close(cursor, conn)

        print(f"\nEnd ShowMeasures\n")

        # close cursor and connection

    # ------------------------------------------------------
    def showTrialColumns(self):
        # connect to SQLite
        conn, cursor = self.connect()

        from pprint import pprint

        # execute command
        cursor.execute("PRAGMA table_info(Trials)")
        TrialColumns = cursor.fetchall()

        print('\n Print TrialS:\n--------------')
        pprint(TrialColumns)

        cursor.execute("SELECT sql FROM sqlite_master \
                       WHERE tbl_name = 'Trials' AND type = 'table'")
        TrialColumns = cursor.fetchall()
        print('\n Pretty Print:\n--------------')
        pprint(TrialColumns)

        # ------------------------------------------------------
    def showColumns(self):
        # connect to SQLite
        conn, cursor = self.connect()

        from pprint import pprint

        # # execute command
        # cursor.execute("PRAGMA table_info(Books)")
        # BookColumns = cursor.fetchall()
        #
        # print('\n Print BOOKS:\n--------------')
        # pprint(BookColumns)

        cursor.execute("SELECT sql FROM sqlite_master \
                       WHERE tbl_name = 'Books' AND type = 'table'")
        BookColumns = cursor.fetchall()
        print('\n Pretty Print:\n--------------')
        pprint(BookColumns)

        # # execute command
        # cursor.execute("SELECT sql FROM sqlite_master \
        #                WHERE tbl_name = 'ASSIGNMENT' AND type = 'table'")
        # ASSIGNColumns = cursor.fetchall()
        # print('\n Pretty Print:\n--------------')
        # pprint(ASSIGNColumns)

        cursor.execute("PRAGMA table_info(ASSIGNMENT)")
        ASSIGNColumns = cursor.fetchall()
        print('\n Pretty Print:\n--------------')
        pprint(ASSIGNColumns)
        # close cursor and connection
        self.close(cursor, conn)


        # ------------------------------------------------------
    def showData(self):
        # connect to SQLite
        conn, cursor = self.connect()

        from pprint import pprint

        print('\n Start ShowData:\n--------------')

        # execute command
        cursor.execute("SELECT * FROM books")
        pprint(cursor.fetchall())

        cursor.execute("SELECT * FROM quoations")
        pprint(cursor.fetchall())

        print('\n End ShowData:\n--------------')

        # close cursor and connection
        self.close(cursor, conn)

        # ------------------------------------------------------

    #----------------------------------------------
    def showASSIGNData(self):
        conn, cursor = self.connect_with_detect_types()
        # conn, cursor = self.connect_without_detect_types()

        cursor.execute("SELECT * from ASSIGNMENT where StudentId = 2")
        fetchedData = cursor.fetchall()

        for row in fetchedData:
            StudentID = row[0]
            StudentName = row[1]
            SubmissionDate = row[2]
            print(StudentName, ", ID -",
                  StudentID, "Submitted Assignments")
            print("Date and Time : ",
                  SubmissionDate)
            print("Submission date type is",
                  type(SubmissionDate))

        self.close(cursor, conn)

    def showDataWithReturn(self):
        # connect to SQLite
        conn, cursor = self.connect()

        # execute command
        cursor.execute("SELECT * FROM trials")
        trialsData = cursor.fetchall()

        cursor.execute("SELECT * FROM measures")
        measuresData = cursor.fetchall()

        # close cursor and connection
        self.close(cursor, conn)

        # print(booksData, quoteData)
        for record in measuresData:
            print(record)

        return trialsData, measuresData


    def fetchLastTenTrials(self):
        conn, cursor = self.connect_with_detect_types()

        try:
            cursor.execute("""SELECT * FROM (
            SELECT * FROM Trials ORDER BY rowid DESC LIMIT 10)
            ORDER BY rowid ASC;""")


        except Exception as ex:

            print(f"fetchLastTenTrials Exception : {ex}")


        finally:

            self.close(cursor, conn)


    # ------------------------------------------
    def fetchMeasuresByTrial_id(self):
        pass


    # ------------------------------------------------------
    def updateGOF(self):
        # connect to SQLite
        conn, cursor = self.connect()

        # execute command
        cursor.execute("SELECT Book_id FROM books WHERE "
                       "Book_Title = 'Design Patterns'")
        primKey = cursor.fetchall()[0][0]
        print("Primary key=" + str(primKey))

        cursor.execute("SELECT * FROM quotations WHERE Books_Book_id = (?)", (primKey,))
        print(cursor.fetchall())

        # close cursor and connection
        self.close(cursor, conn)

        # ------------------------------------------------------

    def updateGOF_commit(self):
        # connect to SQLite
        conn, cursor = self.connect()

        # execute command
        cursor.execute("SELECT Book_id FROM books WHERE Book_Title = 'Design Patterns'")
        primKey = cursor.fetchall()[0][0]
        # print(primKey)

        cursor.execute("SELECT * FROM quotations WHERE Books_Book_id = (?)", (primKey,))
        # print(cursor.fetchall())

        cursor.execute("UPDATE quotations SET Quotation = (%s) WHERE Books_Book_id = (%s)", \
                       ("Pythonic Duck Typing: If it walks like a duck and talks like a duck it probably is a duck...",
                        primKey))

        # commit transaction
        conn.commit()

        cursor.execute("SELECT * FROM quotations WHERE Books_Book_id = (?)", (primKey,))
        # print(cursor.fetchall())

        # close cursor and connection
        self.close(cursor, conn)

        # ------------------------------------------------------

    def deleteRecord(self):
        # connect to SQLite
        conn, cursor = self.connect()

        try:
            # execute command
            cursor.execute("SELECT Book_id FROM books WHERE Book_Title = 'Design Patterns'")
            primKey = cursor.fetchall()[0][0]
            # print(primKey)

            cursor.execute("DELETE FROM books WHERE Book_id = (?)", (primKey,))

            # commit transaction
            conn.commit()
        except:
            pass

        # close cursor and connection
        self.close(cursor, conn)


if __name__ == '__main__':

    SQLite = SQLite()


    try :
        print("START main")
        SQLite.connect()
        # SQLite.createTables()


        SQLite.showTables()
        # SQLite.showColumns()
        # SQLite.insertBooksExample()
        # SQLite.insertBooksExample()




        # SQLite.insertBooks("으앙", 35, "투명드래곤이 울부지젔다")

        # SQLite.showData()

        # SQLite.showBooks()

        # SQLite.dropTables()

        # SQLite.showColumns()


# ASSIGNMENT-----------------------------------

        # SQLite.createASSIGNTable()
        # SQLite.insertASSIGN()
        # SQLite.showASSIGNData()
        # SQLite.dropASSIGN()

# Trials------------------------------------

        SQLite.createLithoTable()
        SQLite.showTrialColumns()
        SQLite.insertTrialIntoTable(2,3,5)
        for i in (range(20)):
            from random import randint
            SQLite.insertTrialIntoTable(randint(1,5),randint(6,10),randint(11,15))

        SQLite.insertMeasureIntoTable(1,2,3,4)
        SQLite.insertMeasureIntoTable(5,6,7,8)
        SQLite.insertMeasureIntoTable(9,10,11, 12)
        # SQLite.showTrials()
        # SQLite.showMeasures()
        sleep(2)

        SQLite.updateTrial()
        SQLite.showTrials()

        SQLite.fetchLastTenTrials()

        SQLite.dropTrials()
        SQLite.dropMeasures()

        # max_id = SQLite.getmax_Trial_id()
        # print(max_id)


        # SQLite.showData()

    except Exception as ex:
        print(ex)