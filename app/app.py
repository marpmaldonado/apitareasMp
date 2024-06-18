from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config
import matplotlib.pyplot as plt

app = Flask(__name__)
conexion = MySQL(app)

#Actualizar tareas

@app.route('/actualizartarea/<codigo>', methods = ['PUT'])
def actualizartarea(codigo):
   actu = request.json
   print(actu)
   nombre = actu['nombre']
   fechai= actu['fecha inicio']
   fechaf = actu['fecha final']
   esta = actu['estado']
   cursor = conexion.connection.cursor()
   cursor.execute("""UPDATE tareas SET nombretar =%s, fechainicio =%s, fechafin=%s, estado=%s WHERE IDtarea=%s""",(nombre,fechai,fechaf,esta,codigo))
   conexion.connection.commit()

   return jsonify({'message':'tarea actualizada'}),201

#Eliminar tarea
@app.route('/eliminartarea/<codigo>', methods = ['DELETE'])
def eliminartarea(codigo):
   cursor = conexion.connection.cursor()
   cursor.execute("DELETE FROM tareas WHERE IDtarea = %s",[codigo])
   conexion.connection.commit()

   return jsonify({'message':'tarea eliminada'})
 
#Ruta para crear tareas
@app.route('/creartarea',methods=['POST'])
def crearTarea():
    tarea = request.json
    nombret = tarea['nombre'],
    fechain = tarea['fecha inicio'],
    fechafin = tarea['fecha final']
    estado = tarea['estado']
    cursor = conexion.connection.cursor()
    cursor.execute("INSERT INTO tareas(nombretar,fechainicio,fechafin,estado)VALUES(%s,%s,%s,%s)",(nombret,fechain,fechafin,estado))
    conexion.connection.commit()
    return jsonify({'message':'tarea agregada con exito'}),201


#Muestra todas las tareas registradas
@app.route('/listartareas', methods=['GET'])
def listartareas():
  
  try:
      #crear la conexion
      cursor = conexion.connection.cursor()
      sql = "SELECT * FROM tareas"
      cursor.execute(sql)
      datos = cursor.fetchall()
      print(datos)

      tareas = []
      for fila in datos:
         #creamos el diccionario
         tarea = {
            'codigo': fila[0],
            'nombre': fila[1],
            'fecha inicio':str(fila[2]),
            'fecha final':str(fila[3]),
            'estado':fila[4]
          }
         tareas.append(tarea)

      return jsonify({'Tareas':tareas,'mensaje':"listado de tareas", 'exito':True})
  
  except Exception as ex:
     return 'Error'

#Muestra todos los usuarios registrados
@app.route('/listarusuarios', methods=['GET'])
def listarusuarios():
  
  try:
      #crear la conexion
      cursor = conexion.connection.cursor()
      sql = "SELECT * FROM usuarios"
      cursor.execute(sql)
      datos = cursor.fetchall()
      print(datos)

      usuarios = []
      for fila in datos:
         #creamos el diccionario
         usuario = {
            'idUsuarios': fila[0],
            'nombre': fila[1],
            'apellido':str(fila[2]),
            'email':str(fila[3]),
            'usuario':fila[4],
            'rol':fila[6]
          }
         usuarios.append(usuario)

      return jsonify({'usuarios':usuario,'mensaje':"listado de usuarios", 'exito':True})
  
  except Exception as ex:
     return 'Error'


#Ruta para buscar tareas
@app.route('/buscartareas', methods = ['GET'])
def buscar_tareas():
   consulta = "SELECT * FROM tareas"
   filtro = []
   parametros = []

   nombre = request.args.get('nombre')
   if nombre:
      filtro.append("nombretar LIKE %s")
      parametros.append(f"%{nombre}%")

   fechainicio = request.args.get('fecha inicio')
   if fechainicio:
      filtro.append("fechainicio LIKE %s")
      parametros.append(f"%{fechainicio}%")

   fechafinal = request.args.get('fecha final')
   if fechafinal:
      filtro.append("fechafin LIKE %s")
      parametros.append(f"%{fechafinal}%")
   
   estado = request.args.get('estado')
   if estado:
      filtro.append("estado LIKE %s")
      parametros.append(f"%{estado}%")

   if not filtro:
      return jsonify({'message': 'no tiene parametros la busqueda'}),400
   
   consulta += " WHERE " + " AND ".join(filtro)
   print("consulta", consulta)
   cursor = conexion.connection.cursor()
   cursor.execute(consulta, parametros)
   datos = cursor.fetchall()
   tareas = []
   for fila in datos:

      tarea = {
         'codigo': fila[0],
         'nombre': fila[1],
         'fecha de inico':str(fila[2]),
         'fecha final':str(fila[3]),
         'estado':fila[4]
      }
      tareas.append(tarea)
   return jsonify(tareas)

#Ruta para buscar usuarios
@app.route('/buscarusuarios', methods = ['GET'])
def buscar_usuarios():
   consulta = "SELECT * FROM usuarios"
   filtro = []
   parametros = []

   codigo = request.args.get('codigo')
   if codigo:
      filtro.append("idUsuarios LIKE %s")
      parametros.append(f"%{codigo}%")

   email = request.args.get('email')
   if email:
      filtro.append("email LIKE %s")
      parametros.append(f"%{email}%")

   nomusu = request.args.get('usuario')
   if nomusu:
      filtro.append("usuario LIKE %s")
      parametros.append(f"%{nomusu}%")
   
   if not filtro:
      return jsonify({'message': 'no tiene parametros la busqueda'}),400
   
   consulta += " WHERE " + " AND ".join(filtro)
   print("consulta", consulta)
   cursor = conexion.connection.cursor()
   cursor.execute(consulta, parametros)
   datos = cursor.fetchall()
   usuarios = []
   for fila in datos:

      usuario = {
         'idUsuarios': fila[0],
         'nombre': fila[1],
         'apellido':str(fila[2]),
         'email':str(fila[3]),
         'usuario':fila[4],
         'rol':fila[6]
      }
      usuarios.append(usuario)
   return jsonify(usuarios)

#Ruta grafico

@app.route('/grafico', methods=['GET'])
def generar_grafico():
    try:
        cursor = conexion.connection.cursor()

        # Contar usuarios registrados
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios_registrados = cursor.fetchone()[0]

        # Contar tareas registradas
        cursor.execute("SELECT COUNT(*) FROM tareas")
        tareas_registradas = cursor.fetchone()[0]

        # Contar tareas en estado terminado
        cursor.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'terminado'")
        tareas_terminadas = cursor.fetchone()[0]

        # Contar tareas en estado en proceso
        cursor.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'en proceso'")
        tareas_en_proceso = cursor.fetchone()[0]

        # Contar tareas en estado por asignar
        cursor.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'por asignar'")
        tareas_por_asignar = cursor.fetchone()[0]

        # Grafico de barras
        categorias = ['Usuarios', 'Tareas', 'Tareas Terminadas', 'Tareas en Proceso', 'Tareas por Asignar']
        cantidades = [usuarios_registrados, tareas_registradas, tareas_terminadas, tareas_en_proceso, tareas_por_asignar]

        plt.bar(categorias, cantidades)
        plt.xlabel('Categoría')
        plt.ylabel('Cantidad')
        plt.title('Cantidad de Usuarios y Tareas')
        plt.show()

        return jsonify({'mensaje': 'Gráfico generado correctamente', 'exito': True})

    except Exception as ex:
        return jsonify({'mensaje': 'Error al generar el gráfico', 'exito': False, 'error': str(ex)})
    

#Ruta rol usuario
@app.route('/grafico_usuario/<int:id_Usuario1>', methods=['GET'])
def generar_grafico_usuario(id_Usuario1):
    try:
        cursor = conexion.connection.cursor()

        # Contar tareas en estado terminado para el usuario
        cursor.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'terminado' AND id_Usuario1 = %s", (id_Usuario1,))
        tareas_terminadas = cursor.fetchone()[0]

        # Contar tareas en estado en proceso para el usuario
        cursor.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'en proceso' AND id_Usuario1 = %s", (id_Usuario1,))
        tareas_en_proceso = cursor.fetchone()[0]

        # Contar tareas en estado por asignar para el usuario
        cursor.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'por asignar' AND id_Usuario1 = %s", (id_Usuario1,))
        tareas_por_asignar = cursor.fetchone()[0]

        # Generar el gráfico de barras
        categorias = ['Tareas Terminadas', 'Tareas en Proceso', 'Tareas por Asignar']
        cantidades = [tareas_terminadas, tareas_en_proceso, tareas_por_asignar]
        colores = ['blue', 'yellow', 'red']

        
        plt.bar(categorias, cantidades, color=colores)
        plt.xlabel('Estado de Tareas')
        plt.ylabel('Cantidad')
        plt.title(f'Cantidad de Tareas del Usuario {id_Usuario1}')
        plt.show()

        # Convertir el gráfico en una imagen para mostrar en el navegador
      

        return jsonify({'mensaje': 'Gráfico generado correctamente', 'exito': True,})

    except Exception as ex:
        return jsonify({'mensaje': 'Error al generar el gráfico', 'exito': False, 'error': str(ex)})



if __name__=='main_':
  app.config.from_object(config['config'])
  app.run(debug=True)