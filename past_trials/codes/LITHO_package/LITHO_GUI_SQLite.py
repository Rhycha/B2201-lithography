import sqlite3
import datetime
from time import sleep
import pandas as pd
import matplotlib.figure as Figure
import csv
##################
# DB Start
##################


class SQLite():
    # class attribute

    def __init__(self, DB='test'):
        SQLite.DB = DB+'.db'
        conn, cursor = self.connect_with_detect_types()
        # SQLite.trialNum = self.getmax_Trial_id()

        self.Trial_id = self.getmax_Trial_id()

        self.close(cursor, conn)
    # ------------------------------------------------------
    def connect(self):
        try:
            conn = sqlite3.connect(SQLite.DB)
            cursor = conn.cursor()
        except Exception as ex:
            print(f"Connection error : {ex}")
        return conn, cursor


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

    def close(self, cursor, conn):
        # close cursor
        cursor.close()

        # close connection to SQLite
        conn.close()


    #------------------------------------------------------
    def createLithoTable(self):
        # connect to SQLite
        conn, cursor = self.connect()

        try:
            # create Table inside DB
            cursor.execute("CREATE TABLE IF NOT EXISTS Trials (       \
                              Trial_id INTEGER, \
                              ExposureTime REAL,     \
                              ExposureEnergy INTEGER,              \
                              Power REAL,                \
                              StartTime TIMESTAMP,                \
                              StopTime TIMESTAMP,                  \
                           PRIMARY KEY(Trial_id AUTOINCREMENT)    \
                    );")

            # create second Table inside DB
            cursor.execute("CREATE TABLE IF NOT EXISTS Measures ( \
                    Trials_Trial_id INTEGER,                \
                    Ampere REAL,				\
                    Sensor REAL,				\
                    Temperature	REAL,		\
                    IntervalNum INTEGER,           \
                    Opstatus TEXT,			\
                    MeasuringTime	TIMESTAMP,		\
            FOREIGN KEY (Trials_Trial_id)       \
                        REFERENCES Trials(Trial_id)     \
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
            cursor.execute('SELECT max(Trial_id) FROM Trials')
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
            # self.Trial_id = cursor.lastrowid
            # print(f"before commit Trialid : {self.Trial_id}")

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
              WHERE Trial_id = ?'''
            update_data_tuple = (StopTime, self.Trial_id)
            cursor.execute(sqlite_update_with_param, update_data_tuple)
            conn.commit()
        except sqlite3.Error as error:
            print("Failed to update Python variable into sqlite table", error)

        finally:
            self.close(cursor, conn)


    # ----------------------------------------------------
    def insertMeasureIntoTable(self, Ampere= -1, Sensor = -1, Temperature=-1,  IntervalNum=-1, Opstatus="", MeasuringTime=datetime.datetime.now()):
        conn, cursor = self.connect()

        try:
            print("Start insertMeasureIntoTable")

            sqlite_insert_with_param = """INSERT INTO Measures
                               (Trials_Trial_id, Ampere, Sensor, Temperature, IntervalNum, Opstatus, MeasuringTime)
                               VALUES (?, ?, ?, ?, ?, ?, ?);"""

            insert_data_tuple = (self.Trial_id, Ampere, Sensor, Temperature, IntervalNum, Opstatus, MeasuringTime)
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
            from pprint import pprint
            # print results
            cursor.execute("SELECT * FROM Measures")
            allMeasures = cursor.fetchall()
            pprint(allMeasures)

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
    def showMeasureColumns(self):
        # connect to SQLite
        conn, cursor = self.connect()

        from pprint import pprint

        # execute command
        cursor.execute("PRAGMA table_info(Measures)")
        MeasureColumns = cursor.fetchall()

        print('\n Print MeasureS:\n--------------')
        pprint(MeasureColumns)

        cursor.execute("SELECT sql FROM sqlite_master \
                       WHERE tbl_name = 'Measures' AND type = 'table'")
        MeasureColumns = cursor.fetchall()
        print('\n Pretty Print:\n--------------')
        pprint(MeasureColumns)



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
            SELECT * FROM trials ORDER BY Trial_id DESC LIMIT 10)
            ORDER BY Trial_id ASC;""")

            result = cursor.fetchall()

            return result
        except Exception as ex:

            print(f"fetchLastTenTrials Exception : {ex}")


        finally:

            self.close(cursor, conn)


    # ------------------------------------------
    def fetchMeasuresByTrial_id(self):
        conn, cursor = self.connect_with_detect_types()

        try:


            cursor.execute("""SELECT * FROM (
            SELECT * FROM measures ORDER BY Trials_Trial_id DESC LIMIT 10)
            ORDER BY Trials_Trial_id ASC;""")

            results = cursor.fetchall()
            print("352", results)
            print("357", type(results))

            return results

        except Exception as e:
            print(f"fetchMeasuresAtLastTrial_id : {e}")

        finally:
            self.close(cursor, conn)


    def fetchMeasuresAtLastTrial_id(self):
        conn, cursor = self.connect_with_detect_types()

        try:
            cursor.execute("""SELECT * from MEASURES where Trials_Trial_id=(?)
            """, (self.Trial_id, ))

            result = cursor.fetchone()

            return result

        except Exception as e:
            print(f"fetchMeasuresAtLastTrial_id : {e}")

        finally:
            self.close(cursor, conn)

    def fetchMeasuresAtLastTrial_id2(self):
        conn, cursor = self.connect_with_detect_types()

        try:
            query = """SELECT * from MEASURES where Trials_Trial_id=(?)"""
            measures_lastTrial_df = pd.read_sql_query(query, conn, params=(self.Trial_id, ), index_col="MeasuringTime")

            return measures_lastTrial_df

        except Exception as e:
            print(f"fetchMeasuresAtLastTrial_id : {e}")

        finally:
            self.close(cursor, conn)


    # def fetchToDataframe(self):
    #     conn, cursor = self.connect_with_detect_types()
    #
    #     # Load the data into a DataFrame
    #     trials_df = pd.read_sql_query("SELECT * from trials", conn)
    #     print("390", trials_df)
    #     last10trials_df = trials_df[trials_df.Trial_id == 3]
    #     print("392", last10trials_df)


    def fromDBtoDataframe(self):

        conn, cursor = self.connect_with_detect_types()

        query = """SELECT * FROM (
            SELECT * FROM measures ORDER BY Trials_Trial_id DESC LIMIT 10)
            ORDER BY Trials_Trial_id ASC;"""

        measures_df = pd.read_sql_query(query, conn)
        print(measures_df)

    def insertinputdata(self):
        conn, cursor = self.connect_with_detect_types()

        trials_df = pd.read_csv("trialssampledata.csv")
        #TODO: 이미 있는 table이라고 한다. 이미 있는 table에 insert 하는 방법 찾아보기.
        trials_df.to_sql("trials", conn, if_exists="replace")
    #TODO: not enough values to unpack (expected 2, got 1) 대체 왜그러냐구우
    def fetchCSVdata(self):
        conn, cursor = self.connect_with_detect_types()
        a_file = open("measuressampledata.csv")
        rows = csv.reader(a_file)
        print(rows)
        new = [row[0].split(';') for row in rows]
        print(len(new))
        print(type(new[0]))

        # for row in rows:
        #     print('442', row)
        #     print('446', type(row))
        #     print('446', len(row))

        cursor.executemany("INSERT INTO measures (Trials_Trial_id, Ampere, Sensor, Temperature, IntervalNum, Opstatus, MeasuringTime) values (?,?,?,?,?,?,?)",new)
        cursor.execute("SELECT * FROM measures")
        print(cursor.fetchall())
        # conn.commit()
        self.close(cursor, conn)


if __name__ == '__main__':

    sql = SQLite()


    try :
        print("START main")
        sql.connect()
        print(sql.Trial_id)
        # sql.dropASSIGN()

# Trials------------------------------------

        # sql.createLithoTable()
        # sql.showTrialColumns()
        sql.insertTrialIntoTable(2,3,5)
        for i in (range(20)):
            from random import randint
            sql.insertTrialIntoTable(randint(1,5),randint(6,10),randint(11,15))
        #

        sql.insertMeasureIntoTable(1,2,3,4)
        sql.insertMeasureIntoTable(5,6,7,8)
        sql.insertMeasureIntoTable(9,10,11, 12)
        sql.showTrials()
        # sleep(2)

        # sql.updateTrial()
        # sql.showTrials()

        # result = sql.fetchLastTenTrials()
        # from pprint import pprint
        # pprint(result)

        # sql.showMeasureColumns()
        # result = sql.fetchMeasuresAtLastTrial_id()
        # from pprint import pprint
        # pprint(result)

        sql.fetchMeasuresByTrial_id()
        print("477")
        sql.fetchMeasuresAtLastTrial_id()
        print("-----------------")
        print(sql.fetchMeasuresAtLastTrial_id2())
        print("481")
        sql.fetchCSVdata()
        sql.showMeasures()


        #TODO: 함수고치기
        # sql.fromDBtoDataframe()

        # sql.insertinputdata()
        # sql.dropTrials()
        # sql.dropMeasures()



        # sql.showData()

    except Exception as ex:
        print(ex)