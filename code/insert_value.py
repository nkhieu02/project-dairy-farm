import psycopg2
from psycopg2 import Error

try:

   connection = psycopg2.connect(
   database="grp2_dairyfarm",  # TO BE REPLACED
   user='grp02',    # TO BE REPLACED
   password='!XxIy#YG', # TO BE REPLACED
   host='dbcourse2022.cs.aalto.fi', 
   port= '5432'
   )

   # Create a cursor to perform database operations
   cursor = connection.cursor()
   CSV_names = ["Stops"]
   insert_query = """
   COPY {} FROM STDIN WITH
        CSV
        HEADER
        DELIMITER AS ','
        """
   file_name = r".\project-dairy-farm\data\{}.csv"
   for name in CSV_names:
       insert_query_copy = insert_query.format(name)
       file_opened = open(file_name.format(name))
       cursor.copy_expert(sql = insert_query_copy, file = file_opened )
       print("Values copied to {}".format(name))
       connection.commit()
except (Exception, Error) as error:
   print("Error while connecting to PostgreSQL", error)
finally:
   if (connection):
      cursor.close()
      connection.close()
      print("PostgreSQL connection is closed")