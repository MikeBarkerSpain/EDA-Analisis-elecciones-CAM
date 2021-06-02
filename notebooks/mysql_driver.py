import pymysql

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