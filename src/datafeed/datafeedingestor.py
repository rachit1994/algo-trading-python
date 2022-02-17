import os
from constants.common import CSV_PATH
import pandas as pd
from src.SQLAlchemy import TargetSqlalchemy
import time

chunksize = 10**4 
at = '@'
colon = ':'
slash = '/'
mysql = 'mysql+mysqlconnector://'
counterstart=1
counterend=1


class CSVDataFeedIngestor():

    def __init__(self):
        targetdbsession, targetdbengine = TargetSqlalchemy()
        self.ingestOneMinuteHistoricalData(targetdbsession, targetdbengine)   

    def ingestOneMinuteHistoricalData(self, targetdbsession, targetdbengine):
         counter=1
         for root,dirs,files in os.walk(CSV_PATH):
            for file in files:
                print("counter -> "+ counter.__str__())
                print("file -> "+ file)
                if (file).endswith(".csv") and counter >= counterstart and  counter <= counterend:
                    filenamewithoutextension=file.replace(".csv", "")
                    print(CSV_PATH+filenamewithoutextension)
                    self.createTable(filenamewithoutextension, targetdbengine)
                    for chunk in pd.read_csv(CSV_PATH+file,chunksize=chunksize, header=None):
                        self.insertDataFeedIntoTable(filenamewithoutextension, targetdbengine, chunk)
                        chunk= None
                counter=counter+1
                        
        

    def createTable(self, tableName, dbengine):
        query = " \
                    CREATE TABLE `" + tableName + "` ( \
                    `INDEX` int(11), \
                    `TIMESTAMP` text, \
                    `OPEN` double DEFAULT NULL, \
                    `HIGH` double DEFAULT NULL, \
                    `LOW` double DEFAULT NULL, \
                    `CLOSE` double DEFAULT NULL, \
                    `VOLUME` int(11) DEFAULT NULL, \
                    `OI` int(11) DEFAULT 0, \
                    PRIMARY KEY (`INDEX`)\
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
                    
        with dbengine.connect() as con:
            con.execute("DROP TABLE IF EXISTS `" + tableName + "`;")
            rs = con.execute(query)
            print("Table "+tableName+" created at --> " + time.strftime(
                                        "%Y-%m-%d %H:%M:%S"))
            con.close()

    def insertDataFeedIntoTable(self, tableName, dbengine, chunk):
        try:
            print("Insertion for table "+tableName+" started at --> " + time.strftime(
                                        "%Y-%m-%d %H:%M:%S"))
            chunk.columns = ['TIMESTAMP', 'OPEN', 'HIGH', 'LOW','CLOSE', 'VOLUME', 'OI']
            chunk.to_sql(tableName, con=dbengine.connect(), schema='GOMARK_ONEMIN_TICK_DATA',
                                             if_exists='append', index=True, )
            print("Insertion for table "+tableName+" finished at --> " + time.strftime(
                                        "%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            print("Error occured while ingesting data into database !")
  

        return True
   

CSVDataFeedIngestor()