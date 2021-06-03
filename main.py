# General Imports
import pandas as pd
import os
import sqlite3

"""
EXTRACT
"""

# Reading CSV 
filepath = input("Ingresa la ruta del CSV: \n")
while not os.path.isfile(filepath):
    print("Error: Ruta no valida, intenta de nuevo.")
    filepath = input("Ingresa la ruta del CSV: \n")
# After analyzing the csv, we can see that the delimiter in this db it's a ';' instead a comma
# So, in order to read this csv, first we need to spicify the delimiter
mainDF =  pd.read_csv(filepath, sep=';')
try:
    mainDF =  pd.read_csv(filepath, sep=';')
    print("\t **** Lectura del CSV Exitosa\n")
except BaseException as exception:
    print(f"Ha ocurrido un error: {exception}")


# filepath = '/Users/benny/Downloads/clientes.csv'
# mainDF =  pd.read_csv(filepath, sep=';')

print(f"\t **** Extraccion del CSV Realizada\n")

"""
TRANSFORM 
"""
#Function to get the age group
def ageGroup(x):
      if x>60:
            return 6
      elif x>50:
            return 5
      elif x>40:
            return 4
      elif x>30:
            return 3
      elif x>20:
            return 2
      else:
            return 1

#Changing DateType
mainDF['fecha_nacimiento'] = pd.to_datetime(mainDF['fecha_nacimiento'], utc=False)
mainDF['fecha_vencimiento'] = pd.to_datetime(mainDF['fecha_vencimiento'], utc=False)
mainDF['telefono'] = mainDF['telefono'].astype('Int64')
### Dataframe: CUSTOMERS
customers = mainDF[['fiscal_id','first_name','last_name','gender']].astype('string') # I pass this columns as we have in the original df

today = pd.to_datetime("today") #setting the time using pandas

customers['birth_date']= mainDF['fecha_nacimiento']
customers['age']= (today - mainDF['fecha_nacimiento']).astype('<m8[Y]').astype('int') 
customers['age_group']= customers['age'].apply(lambda x: ageGroup(x))
customers['due_date']= mainDF['fecha_vencimiento']
customers['delinquency']= (today - mainDF['fecha_vencimiento']).astype('<m8[D]').astype('int')
customers['due_balance']= mainDF['deuda'].astype('int')
customers['address']= mainDF['direccion'].astype('string')

#To Upper
customers['fiscal_id'] = customers['fiscal_id'].str.upper()
customers['first_name'] = customers['first_name'].str.upper()
customers['last_name'] = customers['last_name'].str.upper()
customers['gender'] = customers['gender'].str.upper()
customers['address'] = customers['address'].str.upper()
# print(customers.head)
# print(customers.dtypes)

#Changing the necessary column names and  for EMAILS and PHONES dfs
mainDF=mainDF.rename(columns = {'correo':'email',
                                'estatus_contacto':'status',
                                'telefono':'phone',
                                'prioridad':'priority'})
#Dataframe: EMAILS
emails = mainDF[['fiscal_id','email','status']].astype('string')
emails['priority'] = mainDF['priority'].astype('Int64')

#To Upper
emails['fiscal_id'] = emails['fiscal_id'].str.upper()
emails['email'] = emails['email'].str.upper()
emails['status'] = emails['status'].str.upper()

# print(emails.head)
# print(emails.dtypes)

#Dataframe: PHONES
phones = mainDF[['fiscal_id','phone','status','priority']].astype('string')
phones['priority'] = mainDF['priority'].astype('Int64')

phones['fiscal_id'] = phones['fiscal_id'].str.upper()
phones['phone'] = phones['phone'].str.upper()
phones['status'] = phones['status'].str.upper()

# print(phones.head)
# print(phones.dtypes)

print(f"\t **** Dataframes Generados\n")

"""
LOAD
"""

## XLSX
if not os.path.exists('output'): #Create the folder "output if it doesnt exists"
    os.makedirs('output')

path = 'output/'
customers.to_excel(path+'clientes.xlsx',index=False)
emails.to_excel(path+'emails.xlsx',index=False)
phones.to_excel(path+'phones.xlsx',index=False)

print(f"\t **** Exportacion a XLSX Realizada\n")

## Database
conn = sqlite3.connect("database.db3")  #Connection /creation of the database.
c = conn.cursor() #Cursor Object 

##Table: Customers
c.execute(
    """
    CREATE TABLE IF NOT EXISTS customers (
        fiscal_id TEXT,
        first_name TEXT,
        last_name TEXT,
        gender TEXT,
        birth_date TEXT,
        age INTEGER,
        age_group INTEGER,
        due_date TEXT,
        delinquency INTEGER,
        due_balance INTEGER,
        address TEXT
        );
     """
)
##Table: MAILS
c.execute(
    """     
      CREATE TABLE IF NOT EXISTS emails (
        fiscal_id TEXT,
        email TEXT,
        status TEXT,
        priority INTEGER
        );
     """
)
#Table: PHONES
c.execute(
    """
      CREATE TABLE IF NOT EXISTS phones (
        fiscal_id TEXT,
        phone INTEGER,
        status TEXT,
        priority INTEGER
        );
     """
)

customers.to_sql('customers', conn, if_exists='append', index=False)
emails.to_sql('emails', conn, if_exists='append', index=False)
phones.to_sql('phones', conn, if_exists='append', index=False)

print(f"\t **** Exportacion a Base de Datos Completa\n")


print(mainDF['phone'])