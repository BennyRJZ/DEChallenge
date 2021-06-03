# General Imports
import pandas as pd
import os


"""
EXTRACTING 
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
    print("\nLectura del CSV Exitosa\n")
except BaseException as exception:
    print(f"Ha ocurrido un error: {exception}")
"""
TRANSFORMING 
"""
#Functions
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
#Analyzing the data.
# print(mainDF)
# print(mainDF.dtypes)

#Changing DateType
mainDF['fecha_nacimiento'] = pd.to_datetime(mainDF['fecha_nacimiento'])
mainDF['fecha_vencimiento'] = pd.to_datetime(mainDF['fecha_vencimiento'])
# print(mainDF)
# print(mainDF.dtypes)

#Dataframe: Clients
clients = mainDF[['fiscal_id','first_name','last_name','gender']].astype('string') # I pass this columns as we have in the original df

today = pd.to_datetime("today") #setting the time using pandas

clients['birthday']= mainDF['fecha_nacimiento']
clients['age']= (today - mainDF['fecha_nacimiento']).astype('<m8[Y]').astype('int') 
clients['age_group']= clients['age'].apply(lambda x: ageGroup(x))
clients['due_date']= mainDF['fecha_vencimiento']
clients['delinquency']= (today - mainDF['fecha_vencimiento']).astype('<m8[D]').astype('int')
clients['due_balance']= mainDF['deuda'].astype('int')
clients['address']= mainDF['direccion'].astype('string')
# print(clients)
# print(clients.dtypes)

#Changing the necessary column names and  for EMAILS and PHONES dfs
mainDF=mainDF.rename(columns = {'correo':'email',
                                'estatus_contacto':'status',
                                'telefono':'phone',
                                'prioridad':'priority'})
#Dataframe: EMAILS
emails = mainDF[['fiscal_id','email','status']].astype('string')
emails['priority'] = mainDF['priority'].astype('Int64')
# print(emails)
# print(emails.dtypes)

#Dataframe: PHONES
phones = mainDF[['fiscal_id','phone','status','priority']].astype('string')
phones['priority'] = mainDF['priority'].astype('Int64')
print(emails.loc[[588]])
print(emails.dtypes)

"""
LOADING
"""

