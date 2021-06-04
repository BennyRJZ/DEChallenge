# Data Engineer Challenge

Este desarrollo consta de 3 etapas:
    
*   Extracción.
    *   Solicitamos la ruta del archivo, extraemos los datos de "clientes.csv" y almacenamos la información en "mainDF"
*   Transformación.
    *  Basándonos en "mainDF" creamos 3 dataframes distintos 
        *    1. Customers 
             *    Se renombraron columnas, se calculó la edad, se creó un atributo por rango de edades y se calcularon días de deuda.
        *    2. Emails 
             *    Formateo de Datos
        *    3. Phones
             *    Formateo de Datos
*   Carga.
    *   Despues de transformar los datos desde nuestros nuevos dataframes, los cargamos a 2 destinos distintos:
        *   XLSX (Clientes.xlsx,Phones.xlsx,Emails.xlsx)
        *   Base de Datos SQLite (Customers, Emails, Phones)


### Version de Python Utilizada:
        Python 3.8

### Librerias Utilizadas:
        Pandas 1.1.3
        SQLite 3.33.0
        OS



Benny Ruiz.