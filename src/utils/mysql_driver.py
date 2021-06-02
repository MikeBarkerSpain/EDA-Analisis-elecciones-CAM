import pymysql
import sys, os

'''dir = os.path.dirname
src_path = dir(__file__)
sys.path.append(src_path)

from jsons import read_json_to_dict'''

class MySQL:

    def __init__(self, IP_DNS, USER, PASSWORD, BD_NAME, PORT):
        self.IP_DNS = IP_DNS
        self.USER = USER
        self.PASSWORD = PASSWORD
        self.BD_NAME = BD_NAME
        self.PORT = PORT
        self.SQL_ALCHEMY = 'mysql+pymysql://' + self.USER + ':' + self.PASSWORD + '@' + self.IP_DNS + ':' + str(self.PORT) + '/' + self.BD_NAME
        # 'mysql+pymysql://user:password@91.76.54.33:20001/apr_july_2021_tb'
    def connect(self):
        # Open database connection
        self.db = pymysql.connect(host=self.IP_DNS,
                                  user=self.USER, 
                                  password=self.PASSWORD, 
                                  database=self.BD_NAME, 
                                  port=self.PORT)
        # prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()
        print("Connected to MySQL server [" + self.BD_NAME + "]")
        return self.db

    def close(self):
        # disconnect from server
        self.db.close()
        print("Close connection with MySQL server [" + self.BD_NAME + "]")
    
    def execute_interactive_sql(self, sql, delete=False):
        """ NO SELECT """
        result = 0
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
            print("Executed \n\n" + str(sql) + "\n\n successfully")
            result = 1
        except Exception as error:
            print(error)
            # Rollback in case there is any error
            self.db.rollback()
        return result
        
    def execute_get_sql(self, sql):
        """SELECT"""
        results = None
        print("Executing:\n", sql)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()
        except Exception as error:
            print(error)
            print ("Error: unable to fetch data")
        
        return results

    def generate_insert_into_people_sql(self, to_insert):
        """
        This must be modified according to the table structure
        """
        nombre = to_insert[0]
        apellidos = to_insert[1]
        direccion = to_insert[2]
        edad = to_insert[3]
        nota = to_insert[4]
        
        sql = """INSERT INTO people
            (MOMENTO, ID_BARRIO,DISTRITOS,BARRIOS,LOCALES,LOCSCENSO,CENSO_2021,CENSO_2019,D_CENSO,CENSO,ABSTENCIÓN_2021,ABSTENCIÓN_2019,D_ABS,BLANCO_2021,BLANCO_2019,D_BLC,NULOS_2021,NULOS_2019,D_NULOS,PP_2021,PP_2019,D_PP,VARPP,VARPPCENSO,VARPPLOCALES,ANTERIOR,PSOE_2021,PSOE_2019,D_PSOE,VARPSOE,VARPSOECENSO,VOX_2021,VOX_2019,D_VOX,VARVOX,VARVOXCENSO,MAS_MADRID_2021,MAS_MADRID_2019,D_MAS_MADRID,VARMM,VARMMCENSO,PODEMOS_IU_2021,PODEMOS_IU_2019,D_PODEMOS_IU,VARPIU,VARPIUCENSO,CS_2021,CS_2019,D_CS,VARCS,VARCSCENSO)
            VALUES
            (NOW(), '""" + to_insert[0] + """', '""" + apellidos + """', '""" + direccion + """', '""" + edad + """', '""" + nota + """')"""

        sql = sql.replace("\n", "").replace("            ", " ")
        return sql

def define_SQL_type (stri):
    if stri == 'object':
        return 'VARCHAR(255)'
    elif stri == 'int64':
        return 'INT'
    elif stri == 'float64':
        return 'FLOAT(24)'
    else:
        return ' '

def replace_guion (stri):
    refi = stri.replace('-', '_')
    refi = refi.replace('Á', 'A')
    refi = refi.replace(' ', '_')
    return refi

if __name__ == "__main__":
    def create_table_EDA_MAD (df):
        # lectura de los datos de conexión a la base de datos y generación de las variables para conectarse
        json_readed = read_json_to_dict("sql_settings.json")
        IP_DNS = json_readed["IP_DNS"]
        USER = json_readed["USER"]
        PASSWORD = json_readed["PASSWORD"]
        BD_NAME = json_readed["BD_NAME"]
        PORT = json_readed["PORT"]

        # generación de la instancia de BDD y lanzamiento de conexión
        mysql_db = MySQL(IP_DNS=IP_DNS, USER=USER, PASSWORD=PASSWORD, BD_NAME=BD_NAME, PORT=PORT)
        mysql_db.connect()

        valores = df.dtypes

        sql_create_columns = ""
        for i in range(len(valores)):
            row = replace_guion(valores.index[i].upper()) + ' ' + define_SQL_type(str(valores.values[i])) + ' NOT NULL,'
            sql_create_columns += row

        # Create table as per requirement
        # Erase table if exiting already 
        mysql_db.execute_interactive_sql(sql="DROP TABLE IF EXISTS EDA_MAD")

        # Create the table to hold the data from the data set
        # Create the table with the columns automatically
        create_table_sql = f"""CREATE TABLE EDA_MAD(
            ID INT(11) NOT NULL AUTO_INCREMENT,
            MOMENTO TIMESTAMP NOT NULL,
            {sql_create_columns}
            PRIMARY KEY (ID))"""

        mysql_db.execute_interactive_sql(sql=create_table_sql)

        # create the loop to insert automatically all the rows in the dataframe
        sql_insert_columns = ""
        for i in range(len(valores)):
            row =',' +  replace_guion(valores.index[i].upper())
            sql_insert_columns += row

        for i in range (len (df)):
            values_list = df.iloc[i].to_list()
            sql_insert_values = ""
            for elem in values_list:
                sql_insert_values += ", '" + str(elem) + "'"

            insert_row_sql = f"""INSERT INTO EDA_MAD 
            (MOMENTO{sql_insert_columns})
                        VALUES 
            (NOW(){sql_insert_values})"""

            mysql_db.execute_interactive_sql(sql=insert_row_sql)
        
        mysql_db.close()
        return 'EDA_MAD table created successfully'