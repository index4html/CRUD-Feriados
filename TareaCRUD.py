import json
import mysql.connector
from mysql.connector import Error

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',       # Tu usuario local
            password='123',       # Tu clave local
            database='Feriados' # La BD 
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def crear_tabla():
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feriados2024 (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                comentarios TEXT,
                fecha DATE,
                irrenunciable VARCHAR(10),
                tipo VARCHAR(100)
            )
        ''')
        conexion.commit()
        conexion.close()

def cargar_json_a_bd():
    try:
        with open('Feriados_2024.json', 'r', encoding='utf-8') as archivo:
            datos_json = json.load(archivo)
        
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            for feriado in datos_json:
                query = '''INSERT INTO feriados2024 (nombre, comentarios, fecha, irrenunciable, tipo) 
                           VALUES (%s, %s, %s, %s, %s)'''
                valores = (feriado.get('nombre'), feriado.get('comentarios'), 
                           feriado.get('fecha'), feriado.get('irrenunciable'), feriado.get('tipo'))
                cursor.execute(query, valores)
            conexion.commit()
            print("\n✅ ¡Archivo JSON cargado exitosamente en la base de datos!")
            conexion.close()
    except Exception as e:
        print(f"\n❌ Error: {e}")

def imprimir_resultados(resultados):
    if not resultados:
        print("No se encontraron registros.")
        return
    for r in resultados:
        print(f"ID: {r[0]} | Fecha: {r[3]} | Nombre: {r[1]} | Tipo: {r[5]} | Irrenunciable: {r[4]}")

def a_obtener_todos():
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM feriados2024")
        imprimir_resultados(cursor.fetchall())
        conexion.close()

def b_obtener_religiosos():
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM feriados2024 WHERE tipo = 'Religioso'")
        imprimir_resultados(cursor.fetchall())
        conexion.close()

def c_obtener_irrenunciables():
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM feriados2024 WHERE irrenunciable = '1' OR irrenunciable = 1")
        imprimir_resultados(cursor.fetchall())
        conexion.close()

def d_obtener_rango_fechas():
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM feriados2024 WHERE fecha BETWEEN '2024-03-11' AND '2024-08-31'")
        imprimir_resultados(cursor.fetchall())
        conexion.close()

def e_agregar_feriado(nombre, comentarios, fecha, irrenunciable, tipo):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        query = '''INSERT INTO feriados2024 (nombre, comentarios, fecha, irrenunciable, tipo) 
                   VALUES (%s, %s, %s, %s, %s)'''
        cursor.execute(query, (nombre, comentarios, fecha, irrenunciable, tipo))
        conexion.commit()
        print(f"\n✅ Feriado '{nombre}' agregado.")
        conexion.close()

def f_eliminar_por_nombre(nombre):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        query = "DELETE FROM feriados2024 WHERE nombre = %s"
        cursor.execute(query, (nombre,))
        conexion.commit()
        if cursor.rowcount > 0:
            print(f"\n✅ Se eliminaron {cursor.rowcount} feriado(s) con el nombre '{nombre}'.")
        else:
            print(f"\n⚠️ No se encontró ningún feriado llamado '{nombre}'.")
        conexion.close()

def menu():
    crear_tabla()
    while True:
        print("\n" + "="*40)
        print("     MENÚ DE FERIADOS MYSQL CHILE")
        print("="*40)
        print("0. Cargar archivo Feriados_2024.json a BD")
        print("1. (a) Obtener todos los feriados")
        print("2. (b) Obtener solo feriados de tipo 'Religioso'")
        print("3. (c) Obtener solo feriados irrenunciables")
        print("4. (d) Feriados entre 11-marzo y 31-agosto")
        print("5. (e) Agregar nuevo feriado (Manual)")
        print("6. (f) Eliminar feriado por nombre")
        print("7. (*) Insertar feriado ESPECÍFICO (Unión de los dos paisajes) [2 Pts extra]")
        print("8. Salir")
        print("="*40)
        opcion = input("Elige una opción choro: ")
        
        if opcion == '0': cargar_json_a_bd()
        elif opcion == '1': a_obtener_todos()
        elif opcion == '2': b_obtener_religiosos()
        elif opcion == '3': c_obtener_irrenunciables()
        elif opcion == '4': d_obtener_rango_fechas()
        elif opcion == '5':
            e_agregar_feriado(input("Nombre: "), input("Comentarios: "), input("Fecha (YYYY-MM-DD): "), input("Irrenunciable (0 o 1): "), input("Tipo: "))
        elif opcion == '6': f_eliminar_por_nombre(input("Nombre exacto a eliminar: "))
        elif opcion == '7':
            e_agregar_feriado("Unión de los dos paisajes", "Primera vez que una expedición chilena logró unir la Cordillera de los Andes y la costa del Pacífico en un solo día", "2024-03-11", "0", "Religioso")
        elif opcion == '8': break
        else: print("\nOpción no válida.")

if __name__ == "__main__":
    menu()