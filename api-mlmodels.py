import time
import mysql.connector
import sklearn
import pandas as pd
from pandas import DataFrame
from sklearn.cluster import KMeans
import pickle


import mysql.connector as connection
import pandas as pd

dbConnection = mysql.connector.connect(
    host="localhost",
    port="33060",
    user="sample",
    password="sample",
    database="coffee-mate"
    )


""" try:
    query = "Select userId, questionValue as questionValue1 from responses where questionId = '1'"
    result_dataFrame = pd.read_sql(query,dbConnection, index_col='userId')
    dbConnection.close() #close the connection
except Exception as e:
    dbConnection.close()
    print(str(e))
    
print(result_dataFrame)
 """


try:
    query = "Select userId, cafeId, rankingValue from rankings where rankingValue = 5"
    rankings_dataFrame = pd.read_sql(query,dbConnection)
    print(rankings_dataFrame)
    pivoted_dataframe = rankings_dataFrame.pivot(index='userId', columns = 'cafeId', values='rankingValue')
    dbConnection.close() #close the connection
    print(pivoted_dataframe)
except Exception as e:
    dbConnection.close()
    print(str(e))

