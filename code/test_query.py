import psycopg2
from psycopg2 import Error

try:
   # Connect to an test database 
   # NOTE: 
   # 1. NEVER store credential like this in practice. This is only for testing purpose
   # 2. Replace your "database" name, "user" and "password" that we provide to test the connection to your database 
   connection = psycopg2.connect(
   database="grp2_dairyfarm",  # TO BE REPLACED
   user='grp02',    # TO BE REPLACED
   password='!XxIy#YG', # TO BE REPLACED
   host='dbcourse2022.cs.aalto.fi', 
   port= '5432'
   )

   # Create a cursor to perform database operations
   cursor = connection.cursor()
   F_path = open(".\project-dairy-farm\code\Test_query.sql", "r")
   sqlFile = F_path.read()
   queries = sqlFile.split(";")
   del(queries[-1])
   i = 1
   for query in queries:
       try:
           print("Query {}:".format(i))
           cursor.execute(query)
           print(cursor.fetchall())
       except(Exception, Error) as error:
           print(error)
       finally:
            i += 1

   connection.commit()

except (Exception, Error) as error:
   print(error)
finally:
   if (connection):
      cursor.close()
      connection.close()
      print("PostgreSQL connection is closed")
