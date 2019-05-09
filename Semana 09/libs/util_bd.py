import mysql.connector
import myloginpath
import pandas as pd

def resultados_query(query):
    conf = myloginpath.parse('tesis2')
    conn = mysql.connector.connect(**conf, db="tesis2")
    cursor = conn.cursor()
    cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def ejecutar_query(query):
    conf = myloginpath.parse('tesis2')
    conn = mysql.connector.connect(**conf, db="tesis2")
    cursor = conn.cursor()
    cursor.execute(query)
    conn.close()

def mostrar_resultado_query(query):
    conf = myloginpath.parse('tesis2')
    conn = mysql.connector.connect(**conf, db="tesis2")
    df = pd.read_sql_query(query, conn)
    display(df)
    conn.close()
