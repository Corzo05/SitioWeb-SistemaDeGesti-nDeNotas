from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import database as db
from fpdf import FPDF
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import json
from decimal import Decimal

app= Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
    
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

#Home
@app.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

#Ruta de Redireccion a Home y deslogueado
@app.route('/home', methods=['POST', 'GET'])
@login_required
def redireccion():
    logout_user()
    return redirect(url_for('home'))

#Ruta de Listado Notas Finales
@app.route('/sistema', methods=['POST', 'GET'])
@login_required
def sistemaT():
    
    session['opcion_seleccionada'] = '1'
    
    #Tabla A
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM seccion_a")
    myresult = cursor.fetchall()
    #Datos a diccionario
    insertObject=[]
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
        
    #Tabla B
    cursor.execute("SELECT * FROM seccion_b")
    resultadoB = cursor.fetchall()
    #Datos a diccionario
    insertObjectB=[]
    columnNamesB = [column[0] for column in cursor.description]
    for recordB in resultadoB:
        insertObjectB.append(dict(zip(columnNamesB, recordB)))
    
    #Recuperacion de Datos de logueado
    val_admin = session['rol']
    id_admin = session['id']
    sqlAdmin = "SELECT Nombre_apellido, Rol FROM administradores WHERE ID = %s"
    cursor.execute(sqlAdmin, (id_admin,))
    name_admin = cursor.fetchone()
    nombre_admin = name_admin[0]
    rol_admin = name_admin[1]
    
    cursor.close()
    return render_template('sistema.html', data=insertObject, dataB=insertObjectB, nombre_admin=nombre_admin, rol_admin=rol_admin, val_admin=val_admin)

#Ruta de Cargar Notas Finales A
@app.route('/cargarA/<string:id>', methods=['POST', 'GET'])
def cargarA(id):
    
    #Castellano
    cursor = db.database.cursor()
    sqlCastellano1 = "SELECT Castellano FROM primer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlCastellano1, (id, ))
    castellano1 = cursor.fetchone()[0]
    
    sqlCastellano2 = "SELECT Castellano FROM segundo_lapso_a WHERE Nro = %s"
    cursor.execute(sqlCastellano2, (id, ))
    castellano2 = cursor.fetchone()[0]
    
    sqlCastellano3 = "SELECT Castellano FROM tercer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlCastellano3, (id, ))
    castellano3 = cursor.fetchone()[0]
    
    if isinstance(castellano1, tuple): 
        castellano1 = castellano1[0] 
    if isinstance(castellano2, tuple): 
        castellano2 = castellano2[0] 
    if isinstance(castellano3, tuple): 
        castellano3 = castellano3[0]
    
    if castellano1 and castellano2 and castellano3:
        notaCastellano = (castellano1 + castellano2 + castellano3) / 3
        sqlCastellano= "UPDATE seccion_a SET Castellano = %s WHERE Nro = %s"
        cursor.execute(sqlCastellano, (notaCastellano, id))
        db.database.commit()
        
    #Matematica
    sqlMatematica1 = "SELECT Matematica FROM primer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlMatematica1, (id, ))
    matematica1 = cursor.fetchone()[0]
    
    sqlMatematica2 = "SELECT Matematica FROM segundo_lapso_a WHERE Nro = %s"
    cursor.execute(sqlMatematica2, (id, ))
    matematica2 = cursor.fetchone()[0]
    
    sqlMatematica3 = "SELECT Matematica FROM tercer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlMatematica3, (id, ))
    matematica3 = cursor.fetchone()[0]
    
    if isinstance(matematica1, tuple): 
        matematica1 = matematica1[0] 
    if isinstance(matematica2, tuple): 
        matematica2 = matematica2[0] 
    if isinstance(matematica3, tuple): 
        matematica3 = matematica3[0]
    
    if matematica1 and matematica2 and matematica3:
        notaMatematica = (matematica1 + matematica2 + matematica3) / 3
        sqlMatematica= "UPDATE seccion_a SET Matematica = %s WHERE Nro = %s"
        cursor.execute(sqlMatematica, (notaMatematica, id))
        db.database.commit()
        
    #GHC
    sqlGHC1 = "SELECT GHC FROM primer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlGHC1, (id, ))
    GHC1 = cursor.fetchone()[0]
    
    sqlGHC2 = "SELECT GHC FROM segundo_lapso_a WHERE Nro = %s"
    cursor.execute(sqlGHC2, (id, ))
    GHC2 = cursor.fetchone()[0]
    
    sqlGHC3 = "SELECT GHC FROM tercer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlGHC3, (id, ))
    GHC3 = cursor.fetchone()[0]
    
    if isinstance(GHC1, tuple): 
        GHC1 = GHC1[0] 
    if isinstance(GHC2, tuple): 
        GHC2 = GHC2[0] 
    if isinstance(GHC3, tuple): 
        GHC3 = GHC3[0]
    
    if GHC1 and GHC2 and GHC3:
        notaGHC = (GHC1 + GHC2 + GHC3) / 3
        sqlGHC= "UPDATE seccion_a SET GHC = %s WHERE Nro = %s"
        cursor.execute(sqlGHC, (notaGHC, id))
        db.database.commit()
    
    #Religion
    sqlReligion1 = "SELECT Religion FROM primer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlReligion1, (id, ))
    religion1 = cursor.fetchone()[0]
    
    sqlReligion2 = "SELECT Religion FROM segundo_lapso_a WHERE Nro = %s"
    cursor.execute(sqlReligion2, (id, ))
    religion2 = cursor.fetchone()[0]
    
    sqlReligion3 = "SELECT Religion FROM tercer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlReligion3, (id, ))
    religion3 = cursor.fetchone()[0]
    
    if isinstance(religion1, tuple): 
        religion1 = religion1[0] 
    if isinstance(religion2, tuple): 
        religion2 = religion2[0] 
    if isinstance(religion3, tuple): 
        religion3 = religion3[0]
    
    if religion1 and religion2 and religion3:
        notaReligion = (religion1 + religion2 + religion3) / 3
        sqlReligion= "UPDATE seccion_a SET Religion = %s WHERE Nro = %s"
        cursor.execute(sqlReligion, (notaReligion, id))
        db.database.commit()
        
    #Biologia
    sqlBiologia1 = "SELECT Biologia FROM primer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlBiologia1, (id, ))
    biologia1 = cursor.fetchone()
    
    sqlBiologia2 = "SELECT Biologia FROM segundo_lapso_a WHERE Nro = %s"
    cursor.execute(sqlBiologia2, (id, ))
    biologia2 = cursor.fetchone()[0]
    
    sqlBiologia3 = "SELECT Biologia FROM tercer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlBiologia3, (id, ))
    biologia3 = cursor.fetchone()[0]
    
    if isinstance(biologia1, tuple): 
        biologia1 = biologia1[0] 
    if isinstance(biologia2, tuple): 
        biologia2 = biologia2[0] 
    if isinstance(biologia3, tuple): 
        biologia3 = biologia3[0]
    
    if biologia1 and biologia2 and biologia3:
        notaBiologia = (biologia1 + biologia2 + biologia3) / 3
        sqlBiologia= "UPDATE seccion_a SET Biologia = %s WHERE Nro = %s"
        cursor.execute(sqlBiologia, (notaBiologia, id))
        db.database.commit()
        
    #Computacion
    sqlComputacion1 = "SELECT Computacion FROM primer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlComputacion1, (id, ))
    computacion1 = cursor.fetchone()[0]
    
    sqlComputacion2 = "SELECT Computacion FROM segundo_lapso_a WHERE Nro = %s"
    cursor.execute(sqlComputacion2, (id, ))
    computacion2 = cursor.fetchone()[0]
    
    sqlComputacion3 = "SELECT Computacion FROM tercer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlComputacion3, (id, ))
    computacion3 = cursor.fetchone()[0]
    
    if isinstance(computacion1, tuple): 
        computacion1 = computacion1[0] 
    if isinstance(computacion2, tuple): 
        computacion2 = computacion2[0] 
    if isinstance(computacion3, tuple): 
        computacion3 = computacion3[0]
    
    if computacion1 and computacion2 and computacion3:
        notaComputacion = (computacion1 + computacion2 + computacion3) / 3
        sqlComputacion= "UPDATE seccion_a SET Computacion = %s WHERE Nro = %s"
        cursor.execute(sqlComputacion, (notaComputacion, id))
        db.database.commit()
        
    #Ingles
    sqlIngles1 = "SELECT Ingles FROM primer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlIngles1, (id, ))
    ingles1 = cursor.fetchone()[0]
    
    sqlIngles2 = "SELECT Ingles FROM segundo_lapso_a WHERE Nro = %s"
    cursor.execute(sqlIngles2, (id, ))
    ingles2 = cursor.fetchone()[0]
    
    sqlIngles3 = "SELECT Ingles FROM tercer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlIngles3, (id, ))
    ingles3 = cursor.fetchone()[0]
    
    if isinstance(ingles1, tuple): 
        ingles1 = ingles1[0] 
    if isinstance(ingles2, tuple): 
        ingles2 = ingles2[0] 
    if isinstance(ingles3, tuple): 
        ingles3 = ingles3[0]
    
    if ingles1 and ingles2 and ingles3:
        notaIngles = (ingles1 + ingles2 + ingles3) / 3
        sqlIngles= "UPDATE seccion_a SET Ingles = %s WHERE Nro = %s"
        cursor.execute(sqlIngles, (notaIngles, id))
        db.database.commit()
        
    #Arte
    sqlArte1 = "SELECT Arte FROM primer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlArte1, (id, ))
    arte1 = cursor.fetchone()[0]
    
    sqlArte2 = "SELECT Arte FROM segundo_lapso_a WHERE Nro = %s"
    cursor.execute(sqlArte2, (id, ))
    arte2 = cursor.fetchone()[0]
    
    sqlArte3 = "SELECT Arte FROM tercer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlArte3, (id, ))
    arte3 = cursor.fetchone()[0]
    
    if isinstance(arte1, tuple): 
        arte1 = arte1[0] 
    if isinstance(arte2, tuple): 
        arte2 = arte2[0] 
    if isinstance(arte3, tuple): 
        arte3 = arte3[0]
    
    if arte1 and arte2 and arte3:
        notaArte = (arte1 + arte2 + arte3) / 3
        sqlArte= "UPDATE seccion_a SET Arte = %s WHERE Nro = %s"
        cursor.execute(sqlArte, (notaArte, id))
        db.database.commit()
        
    #Educacion Fisica
    sqlEducacion_fisica1 = "SELECT Educacion_fisica FROM primer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlEducacion_fisica1, (id, ))
    educacion_fisica1 = cursor.fetchone()[0]
    
    sqlEducacion_fisica2 = "SELECT Educacion_fisica FROM segundo_lapso_a WHERE Nro = %s"
    cursor.execute(sqlEducacion_fisica2, (id, ))
    educacion_fisica2 = cursor.fetchone()[0]
    
    sqlEducacion_fisica3 = "SELECT Educacion_fisica FROM tercer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlEducacion_fisica3, (id, ))
    educacion_fisica3 = cursor.fetchone()[0]
    
    if isinstance(educacion_fisica1, tuple): 
        educacion_fisica1 = educacion_fisica1[0] 
    if isinstance(educacion_fisica2, tuple): 
        educacion_fisica2 = educacion_fisica2[0] 
    if isinstance(educacion_fisica3, tuple): 
        educacion_fisica3 = educacion_fisica3[0]
    
    if educacion_fisica1 and educacion_fisica2 and educacion_fisica3:
        notaEducacion_fisica = (educacion_fisica1 + educacion_fisica2 + educacion_fisica3) / 3
        sqlEducacion_fisica= "UPDATE seccion_a SET Educacion_fisica = %s WHERE Nro = %s"
        cursor.execute(sqlEducacion_fisica, (notaEducacion_fisica, id))
        db.database.commit()
        
    cursor.close()
    return redirect(url_for('sistemaT'))

#Ruta de Cargar Notas Finales B
@app.route('/cargarB/<string:id>', methods=['POST', 'GET'])
def cargarB(id):
    
    #Castellano
    cursor = db.database.cursor()
    sqlCastellano1 = "SELECT Castellano FROM primer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlCastellano1, (id, ))
    castellano1 = cursor.fetchone()[0]
    
    sqlCastellano2 = "SELECT Castellano FROM segundo_lapso_b WHERE Nro = %s"
    cursor.execute(sqlCastellano2, (id, ))
    castellano2 = cursor.fetchone()[0]
    
    sqlCastellano3 = "SELECT Castellano FROM tercer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlCastellano3, (id, ))
    castellano3 = cursor.fetchone()[0]
    
    if isinstance(castellano1, tuple): 
        castellano1 = castellano1[0] 
    if isinstance(castellano2, tuple): 
        castellano2 = castellano2[0] 
    if isinstance(castellano3, tuple): 
        castellano3 = castellano3[0]
    
    if castellano1 and castellano2 and castellano3:
        notaCastellano = (castellano1 + castellano2 + castellano3) / 3
        sqlCastellano= "UPDATE seccion_b SET Castellano = %s WHERE Nro = %s"
        cursor.execute(sqlCastellano, (notaCastellano, id))
        db.database.commit()
        
    #Matematica
    sqlMatematica1 = "SELECT Matematica FROM primer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlMatematica1, (id, ))
    matematica1 = cursor.fetchone()[0]
    
    sqlMatematica2 = "SELECT Matematica FROM segundo_lapso_b WHERE Nro = %s"
    cursor.execute(sqlMatematica2, (id, ))
    matematica2 = cursor.fetchone()[0]
    
    sqlMatematica3 = "SELECT Matematica FROM tercer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlMatematica3, (id, ))
    matematica3 = cursor.fetchone()[0]
    
    if isinstance(matematica1, tuple): 
        matematica1 = matematica1[0] 
    if isinstance(matematica2, tuple): 
        matematica2 = matematica2[0] 
    if isinstance(matematica3, tuple): 
        matematica3 = matematica3[0]
    
    if matematica1 and matematica2 and matematica3:
        notaMatematica = (matematica1 + matematica2 + matematica3) / 3
        sqlMatematica= "UPDATE seccion_b SET Matematica = %s WHERE Nro = %s"
        cursor.execute(sqlMatematica, (notaMatematica, id))
        db.database.commit()
        
    #GHC
    sqlGHC1 = "SELECT GHC FROM primer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlGHC1, (id, ))
    GHC1 = cursor.fetchone()[0]
    
    sqlGHC2 = "SELECT GHC FROM segundo_lapso_b WHERE Nro = %s"
    cursor.execute(sqlGHC2, (id, ))
    GHC2 = cursor.fetchone()[0]
    
    sqlGHC3 = "SELECT GHC FROM tercer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlGHC3, (id, ))
    GHC3 = cursor.fetchone()[0]
    
    if isinstance(GHC1, tuple): 
        GHC1 = GHC1[0] 
    if isinstance(GHC2, tuple): 
        GHC2 = GHC2[0] 
    if isinstance(GHC3, tuple): 
        GHC3 = GHC3[0]
    
    if GHC1 and GHC2 and GHC3:
        notaGHC = (GHC1 + GHC2 + GHC3) / 3
        sqlGHC= "UPDATE seccion_b SET GHC = %s WHERE Nro = %s"
        cursor.execute(sqlGHC, (notaGHC, id))
        db.database.commit()
    
    #Religion
    sqlReligion1 = "SELECT Religion FROM primer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlReligion1, (id, ))
    religion1 = cursor.fetchone()[0]
    
    sqlReligion2 = "SELECT Religion FROM segundo_lapso_b WHERE Nro = %s"
    cursor.execute(sqlReligion2, (id, ))
    religion2 = cursor.fetchone()[0]
    
    sqlReligion3 = "SELECT Religion FROM tercer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlReligion3, (id, ))
    religion3 = cursor.fetchone()[0]
    
    if isinstance(religion1, tuple): 
        religion1 = religion1[0] 
    if isinstance(religion2, tuple): 
        religion2 = religion2[0] 
    if isinstance(religion3, tuple): 
        religion3 = religion3[0]
    
    if religion1 and religion2 and religion3:
        notaReligion = (religion1 + religion2 + religion3) / 3
        sqlReligion= "UPDATE seccion_b SET Religion = %s WHERE Nro = %s"
        cursor.execute(sqlReligion, (notaReligion, id))
        db.database.commit()
        
    #Biologia
    sqlBiologia1 = "SELECT Biologia FROM primer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlBiologia1, (id, ))
    biologia1 = cursor.fetchone()
    
    sqlBiologia2 = "SELECT Biologia FROM segundo_lapso_b WHERE Nro = %s"
    cursor.execute(sqlBiologia2, (id, ))
    biologia2 = cursor.fetchone()[0]
    
    sqlBiologia3 = "SELECT Biologia FROM tercer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlBiologia3, (id, ))
    biologia3 = cursor.fetchone()[0]
    
    if isinstance(biologia1, tuple): 
        biologia1 = biologia1[0] 
    if isinstance(biologia2, tuple): 
        biologia2 = biologia2[0] 
    if isinstance(biologia3, tuple): 
        biologia3 = biologia3[0]
    
    if biologia1 and biologia2 and biologia3:
        notaBiologia = (biologia1 + biologia2 + biologia3) / 3
        sqlBiologia= "UPDATE seccion_b SET Biologia = %s WHERE Nro = %s"
        cursor.execute(sqlBiologia, (notaBiologia, id))
        db.database.commit()
        
    #Computacion
    sqlComputacion1 = "SELECT Computacion FROM primer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlComputacion1, (id, ))
    computacion1 = cursor.fetchone()[0]
    
    sqlComputacion2 = "SELECT Computacion FROM segundo_lapso_b WHERE Nro = %s"
    cursor.execute(sqlComputacion2, (id, ))
    computacion2 = cursor.fetchone()[0]
    
    sqlComputacion3 = "SELECT Computacion FROM tercer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlComputacion3, (id, ))
    computacion3 = cursor.fetchone()[0]
    
    if isinstance(computacion1, tuple): 
        computacion1 = computacion1[0] 
    if isinstance(computacion2, tuple): 
        computacion2 = computacion2[0] 
    if isinstance(computacion3, tuple): 
        computacion3 = computacion3[0]
    
    if computacion1 and computacion2 and computacion3:
        notaComputacion = (computacion1 + computacion2 + computacion3) / 3
        sqlComputacion= "UPDATE seccion_b SET Computacion = %s WHERE Nro = %s"
        cursor.execute(sqlComputacion, (notaComputacion, id))
        db.database.commit()
        
    #Ingles
    sqlIngles1 = "SELECT Ingles FROM primer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlIngles1, (id, ))
    ingles1 = cursor.fetchone()[0]
    
    sqlIngles2 = "SELECT Ingles FROM segundo_lapso_b WHERE Nro = %s"
    cursor.execute(sqlIngles2, (id, ))
    ingles2 = cursor.fetchone()[0]
    
    sqlIngles3 = "SELECT Ingles FROM tercer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlIngles3, (id, ))
    ingles3 = cursor.fetchone()[0]
    
    if isinstance(ingles1, tuple): 
        ingles1 = ingles1[0] 
    if isinstance(ingles2, tuple): 
        ingles2 = ingles2[0] 
    if isinstance(ingles3, tuple): 
        ingles3 = ingles3[0]
    
    if ingles1 and ingles2 and ingles3:
        notaIngles = (ingles1 + ingles2 + ingles3) / 3
        sqlIngles= "UPDATE seccion_b SET Ingles = %s WHERE Nro = %s"
        cursor.execute(sqlIngles, (notaIngles, id))
        db.database.commit()
        
    #Arte
    sqlArte1 = "SELECT Arte FROM primer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlArte1, (id, ))
    arte1 = cursor.fetchone()[0]
    
    sqlArte2 = "SELECT Arte FROM segundo_lapso_b WHERE Nro = %s"
    cursor.execute(sqlArte2, (id, ))
    arte2 = cursor.fetchone()[0]
    
    sqlArte3 = "SELECT Arte FROM tercer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlArte3, (id, ))
    arte3 = cursor.fetchone()[0]
    
    if isinstance(arte1, tuple): 
        arte1 = arte1[0] 
    if isinstance(arte2, tuple): 
        arte2 = arte2[0] 
    if isinstance(arte3, tuple): 
        arte3 = arte3[0]
    
    if arte1 and arte2 and arte3:
        notaArte = (arte1 + arte2 + arte3) / 3
        sqlArte= "UPDATE seccion_b SET Arte = %s WHERE Nro = %s"
        cursor.execute(sqlArte, (notaArte, id))
        db.database.commit()
        
    #Educacion Fisica
    sqlEducacion_fisica1 = "SELECT Educacion_fisica FROM primer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlEducacion_fisica1, (id, ))
    educacion_fisica1 = cursor.fetchone()[0]
    
    sqlEducacion_fisica2 = "SELECT Educacion_fisica FROM segundo_lapso_b WHERE Nro = %s"
    cursor.execute(sqlEducacion_fisica2, (id, ))
    educacion_fisica2 = cursor.fetchone()[0]
    
    sqlEducacion_fisica3 = "SELECT Educacion_fisica FROM tercer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlEducacion_fisica3, (id, ))
    educacion_fisica3 = cursor.fetchone()[0]
    
    if isinstance(educacion_fisica1, tuple): 
        educacion_fisica1 = educacion_fisica1[0] 
    if isinstance(educacion_fisica2, tuple): 
        educacion_fisica2 = educacion_fisica2[0] 
    if isinstance(educacion_fisica3, tuple): 
        educacion_fisica3 = educacion_fisica3[0]
    
    if educacion_fisica1 and educacion_fisica2 and educacion_fisica3:
        notaEducacion_fisica = (educacion_fisica1 + educacion_fisica2 + educacion_fisica3) / 3
        sqlEducacion_fisica= "UPDATE seccion_b SET Educacion_fisica = %s WHERE Nro = %s"
        cursor.execute(sqlEducacion_fisica, (notaEducacion_fisica, id))
        db.database.commit()
        
    cursor.close()
    return redirect(url_for('sistemaT'))

#Ruta para calcular Promedio Final del Año Seccion A
@app.route('/promedio_finalA/<string:id>')
def promedio_finalA(id):
    
    cursor = db.database.cursor()
    sqlNotas = "SELECT Castellano, Matematica, GHC, Religion, Biologia, Computacion, Ingles, Arte, Educacion_fisica FROM seccion_a WHERE Nro = %s"
    cursor.execute(sqlNotas, (id, ))
    resultado = cursor.fetchone()
    
    if resultado:
        promedio = sum(resultado) / len(resultado)
        sql= "UPDATE seccion_a SET Promedio = %s WHERE Nro = %s"
        cursor.execute(sql, (promedio, id))
        db.database.commit()
    cursor.close()
    return redirect(url_for('sistemaT'))

#Ruta para calcular Promedio Final del Año Seccion B
@app.route('/promedio_finalB/<string:id>')
def promedio_finalB(id):
    
    cursor = db.database.cursor()
    sqlNotas = "SELECT Castellano, Matematica, GHC, Religion, Biologia, Computacion, Ingles, Arte, Educacion_fisica FROM seccion_b WHERE Nro = %s"
    cursor.execute(sqlNotas, (id, ))
    resultado = cursor.fetchone()
    
    if resultado:
        promedio = sum(resultado) / len(resultado)
        sql= "UPDATE seccion_b SET Promedio = %s WHERE Nro = %s"
        cursor.execute(sql, (promedio, id))
        db.database.commit()
    cursor.close()
    return redirect(url_for('sistemaT'))

#Ruta para guardar estudiantes Seccion A
@app.route('/agregar-estudiante-A', methods=['POST'])
def addEstudianteA():
    
    cursor = db.database.cursor()
    sqlVerificacion = "SELECT Cedula FROM registro_estudiantes_a"
    cursor.execute(sqlVerificacion)
    cedulaConfirm = cursor.fetchall()
    cursor.close()
    
    lista_cedulas = [tupla[0] for tupla in cedulaConfirm]
        
    nombre_completo = request.form['nombre_completo_A']
    sexo = request.form['sexo_A']
    cedula = request.form['cedula_A']
    
    if nombre_completo and sexo and cedula:
        
        if cedula in lista_cedulas:
            mensajeCedula = "Cédula ya existente, introduzca otra"
            
            return redirect(url_for('pestaña1'))
        else:
            cursor = db.database.cursor()
            sql1= "INSERT INTO registro_estudiantes_a (Nombre_completo, Sexo, Cedula) VALUES (%s, %s, %s)"
            data1= (nombre_completo, sexo, cedula)
            cursor.execute(sql1, data1)
            db.database.commit()
            
            sql2= "INSERT INTO seccion_a (Nombre_completo, Sexo, Cedula) VALUES (%s, %s, %s)"
            data2= (nombre_completo, sexo, cedula)
            cursor.execute(sql2, data2)
            db.database.commit()
            
            sql3= "INSERT INTO primer_lapso_a (Nombre_completo, Sexo, Cedula) VALUES (%s, %s, %s)"
            data3= (nombre_completo, sexo, cedula)
            cursor.execute(sql3, data3)
            db.database.commit()
            
            sql4= "INSERT INTO segundo_lapso_a (Nombre_completo, Sexo, Cedula) VALUES (%s, %s, %s)"
            data4= (nombre_completo, sexo, cedula)
            cursor.execute(sql4, data4)
            db.database.commit()
            
            sql5= "INSERT INTO tercer_lapso_a (Nombre_completo, Sexo, Cedula) VALUES (%s, %s, %s)"
            data5= (nombre_completo, sexo, cedula)
            cursor.execute(sql5, data5)
            db.database.commit() 
        
    return redirect(url_for('pestaña1'))

#Ruta para guardar estudiantes Seccion B
@app.route('/agregar-estudiante-B', methods=['POST'])
def addEstudianteB():
    
    cursor = db.database.cursor()
    sqlVerificacion = "SELECT Cedula FROM registro_estudiantes_b"
    cursor.execute(sqlVerificacion)
    cedulaConfirm = cursor.fetchall()
    cursor.close()
    
    lista_cedulas = [tupla[0] for tupla in cedulaConfirm]
    
    nombre_completoB = request.form['nombre_completo_B']
    sexoB = request.form['sexo_B']
    cedulaB = request.form['cedula_B']
    
    if nombre_completoB and sexoB and cedulaB:
        
        if cedulaB in lista_cedulas:
            mensajeCedula = "Cédula ya existente, introduzca otra"
            
            return redirect(url_for('pestaña1'))
        else:
            cursor = db.database.cursor()
            sql1B= "INSERT INTO registro_estudiantes_b (Nombre_completo, Sexo, Cedula) VALUES (%s, %s, %s)"
            data1B= (nombre_completoB, sexoB, cedulaB)
            cursor.execute(sql1B, data1B)
            db.database.commit()
            
            sql2B= "INSERT INTO seccion_b (Nombre_completo, Sexo, Cedula) VALUES (%s, %s, %s)"
            data2B= (nombre_completoB, sexoB, cedulaB)
            cursor.execute(sql2B, data2B)
            db.database.commit()
            
            sql3B= "INSERT INTO primer_lapso_b (Nombre_completo, Sexo, Cedula) VALUES (%s, %s, %s)"
            data3B= (nombre_completoB, sexoB, cedulaB)
            cursor.execute(sql3B, data3B)
            db.database.commit()
            
            sql4B= "INSERT INTO segundo_lapso_b (Nombre_completo, Sexo, Cedula) VALUES (%s, %s, %s)"
            data4B= (nombre_completoB, sexoB, cedulaB)
            cursor.execute(sql4B, data4B)
            db.database.commit()
            
            sql5B= "INSERT INTO tercer_lapso_b (Nombre_completo, Sexo, Cedula) VALUES (%s, %s, %s)"
            data5B= (nombre_completoB, sexoB, cedulaB)
            cursor.execute(sql5B, data5B)
            db.database.commit()
            
    return redirect(url_for('pestaña1'))

#Ruta para editar registro general estudiantes Seccion A
@app.route('/editarA/<string:id>', methods=['POST'])
def editA(id):
    
    nombre_completo = request.form['nombre_completo']
    sexo = request.form['sexo']
    cedula = request.form['cedula']
    
    if nombre_completo and sexo and cedula:
        cursor = db.database.cursor()
        sql1= "UPDATE registro_estudiantes_a SET Nombre_completo = %s, Sexo = %s, Cedula = %s WHERE Nro = %s"
        data1= (nombre_completo, sexo, cedula, id)
        cursor.execute(sql1, data1)
        db.database.commit()
        
        sql2= "UPDATE seccion_a SET Nombre_completo = %s, Sexo = %s, Cedula = %s WHERE Nro = %s"
        data2= (nombre_completo, sexo, cedula, id)
        cursor.execute(sql2, data2)
        db.database.commit()
        
        sql3= "UPDATE primer_lapso_a SET Nombre_completo = %s, Sexo = %s, Cedula = %s WHERE Nro = %s"
        data3= (nombre_completo, sexo, cedula, id)
        cursor.execute(sql3, data3)
        db.database.commit()
        
        sql4= "UPDATE segundo_lapso_a SET Nombre_completo = %s, Sexo = %s, Cedula = %s WHERE Nro = %s"
        data4= (nombre_completo, sexo, cedula, id)
        cursor.execute(sql4, data4)
        db.database.commit()
        
        sql5= "UPDATE tercer_lapso_a SET Nombre_completo = %s, Sexo = %s, Cedula = %s WHERE Nro = %s"
        data5= (nombre_completo, sexo, cedula, id)
        cursor.execute(sql5, data5)
        db.database.commit()
    return redirect(url_for('pestaña1'))

#Ruta para editar registro general estudiantes Seccion B
@app.route('/editarB/<string:id>', methods=['POST'])
def editB(id):
    
    nombre_completo = request.form['nombre_completo']
    sexo = request.form['sexo']
    cedula = request.form['cedula']
    
    if nombre_completo and sexo and cedula:
        cursor = db.database.cursor()
        sql1= "UPDATE registro_estudiantes_b SET Nombre_completo = %s, Sexo = %s, Cedula = %s WHERE Nro = %s"
        data1= (nombre_completo, sexo, cedula, id)
        cursor.execute(sql1, data1)
        db.database.commit()
        
        sql2= "UPDATE seccion_b SET Nombre_completo = %s, Sexo = %s, Cedula = %s WHERE Nro = %s"
        data2= (nombre_completo, sexo, cedula, id)
        cursor.execute(sql2, data2)
        db.database.commit()
        
        sql3= "UPDATE primer_lapso_b SET Nombre_completo = %s, Sexo = %s, Cedula = %s WHERE Nro = %s"
        data3= (nombre_completo, sexo, cedula, id)
        cursor.execute(sql3, data3)
        db.database.commit()
        
        sql4= "UPDATE segundo_lapso_b SET Nombre_completo = %s, Sexo = %s, Cedula = %s WHERE Nro = %s"
        data4= (nombre_completo, sexo, cedula, id)
        cursor.execute(sql4, data4)
        db.database.commit()
        
        sql5= "UPDATE tercer_lapso_b SET Nombre_completo = %s, Sexo = %s, Cedula = %s WHERE Nro = %s"
        data5= (nombre_completo, sexo, cedula, id)
        cursor.execute(sql5, data5)
        db.database.commit()
    return redirect(url_for('pestaña1'))

#Ruta para eliminar estudiantes de la Seccion A
@app.route('/eliminar/<string:id>')
def eliminarA(id):
    
    cursor = db.database.cursor()
    sql1= "DELETE FROM registro_estudiantes_a WHERE Nro = %s"
    data1= (id,)
    cursor.execute(sql1, data1)
    db.database.commit()
    
    sql2= "DELETE FROM seccion_a WHERE Nro = %s"
    data2= (id,)
    cursor.execute(sql2, data2)
    db.database.commit()
    
    sql3= "DELETE FROM primer_lapso_a WHERE Nro = %s"
    data3= (id,)
    cursor.execute(sql3, data3)
    db.database.commit()
    
    sql4= "DELETE FROM segundo_lapso_a WHERE Nro = %s"
    data4= (id,)
    cursor.execute(sql4, data4)
    db.database.commit()
    
    sql5= "DELETE FROM tercer_lapso_a WHERE Nro = %s"
    data5= (id,)
    cursor.execute(sql5, data5)
    db.database.commit()
    
    cursor.close()
    return redirect(url_for('pestaña2'))

#Ruta para eliminar estudiantes de la Seccion B
@app.route('/eliminarB/<string:id>')
def eliminarB(id):
    
    cursor = db.database.cursor()
    sql1= "DELETE FROM registro_estudiantes_b WHERE Nro = %s"
    data1= (id,)
    cursor.execute(sql1, data1)
    db.database.commit()
    
    sql2= "DELETE FROM seccion_b WHERE Nro = %s"
    data2= (id,)
    cursor.execute(sql2, data2)
    db.database.commit()
    
    sql3= "DELETE FROM primer_lapso_b WHERE Nro = %s"
    data3= (id,)
    cursor.execute(sql3, data3)
    db.database.commit()
    
    sql4= "DELETE FROM segundo_lapso_b WHERE Nro = %s"
    data4= (id,)
    cursor.execute(sql4, data4)
    db.database.commit()
    
    sql5= "DELETE FROM tercer_lapso_b WHERE Nro = %s"
    data5= (id,)
    cursor.execute(sql5, data5)
    db.database.commit()
    
    cursor.close()
    return redirect(url_for('pestaña2'))

#Ruta para editar estudiantes Primer Lapso A
@app.route('/editar1A/<string:id>', methods=['POST'])
def edit1A(id):
    
    if request.method == 'POST':
        session['opcion_seleccionada'] = '1'
        
        castellano = request.form['castellano']
        matematica = request.form['matematica']
        GHC = request.form['GHC']
        religion = request.form['religion']
        biologia = request.form['biologia']
        computacion = request.form['computacion']
        ingles = request.form['ingles']
        arte = request.form['arte']
        ed_fisica = request.form['educacion-fisica']
        
        if castellano and matematica and GHC and religion and biologia and computacion and ingles and arte and ed_fisica:
            cursor = db.database.cursor()
            sql= "UPDATE primer_lapso_a SET Castellano = %s, Matematica = %s, GHC = %s, Religion = %s, Biologia = %s, Computacion = %s, Ingles = %s, Arte = %s, Educacion_fisica = %s WHERE Nro = %s"
            data= (castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica, id)
            cursor.execute(sql, data)
            db.database.commit()
        return redirect(url_for('pestaña3'))

#Ruta para editar estudiantes Primer Lapso B
@app.route('/editar1B/<string:id>', methods=['POST'])
def edit1B(id):
    
    if request.method == 'POST':
        session['opcion_seleccionada'] = '1'
        
        castellano = request.form['castellano']
        matematica = request.form['matematica']
        GHC = request.form['GHC']
        religion = request.form['religion']
        biologia = request.form['biologia']
        computacion = request.form['computacion']
        ingles = request.form['ingles']
        arte = request.form['arte']
        ed_fisica = request.form['educacion-fisica']
        
        if castellano and matematica and GHC and religion and biologia and computacion and ingles and arte and ed_fisica:
            cursor = db.database.cursor()
            sql= "UPDATE primer_lapso_b SET Castellano = %s, Matematica = %s, GHC = %s, Religion = %s, Biologia = %s, Computacion = %s, Ingles = %s, Arte = %s, Educacion_fisica = %s WHERE Nro = %s"
            data= (castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica, id)
            cursor.execute(sql, data)
            db.database.commit()
        return redirect(url_for('pestaña3'))

#Ruta para editar estudiantes Segundo Lapso A
@app.route('/editar2A/<string:id>', methods=['POST'])
def edit2A(id):
    
    if request.method == 'POST':
        session['opcion_seleccionada'] = '2'
         
        castellano = request.form['castellano']
        matematica = request.form['matematica']
        GHC = request.form['GHC']
        religion = request.form['religion']
        biologia = request.form['biologia']
        computacion = request.form['computacion']
        ingles = request.form['ingles']
        arte = request.form['arte']
        ed_fisica = request.form['educacion-fisica']
        
        if castellano and matematica and GHC and religion and biologia and computacion and ingles and arte and ed_fisica:
            cursor = db.database.cursor()
            sql= "UPDATE segundo_lapso_a SET Castellano = %s, Matematica = %s, GHC = %s, Religion = %s, Biologia = %s, Computacion = %s, Ingles = %s, Arte = %s, Educacion_fisica = %s WHERE Nro = %s"
            data= (castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica, id)
            cursor.execute(sql, data)
            db.database.commit()
        return redirect(url_for('pestaña3'))

#Ruta para editar estudiantes Segundo Lapso B
@app.route('/editar2B/<string:id>', methods=['POST'])
def edit2B(id):
    
    if request.method == 'POST':
        session['opcion_seleccionada'] = '2'
    
        castellano = request.form['castellano']
        matematica = request.form['matematica']
        GHC = request.form['GHC']
        religion = request.form['religion']
        biologia = request.form['biologia']
        computacion = request.form['computacion']
        ingles = request.form['ingles']
        arte = request.form['arte']
        ed_fisica = request.form['educacion-fisica']
        
        if castellano and matematica and GHC and religion and biologia and computacion and ingles and arte and ed_fisica:
            cursor = db.database.cursor()
            sql= "UPDATE segundo_lapso_b SET Castellano = %s, Matematica = %s, GHC = %s, Religion = %s, Biologia = %s, Computacion = %s, Ingles = %s, Arte = %s, Educacion_fisica = %s WHERE Nro = %s"
            data= (castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica, id)
            cursor.execute(sql, data)
            db.database.commit()
        return redirect(url_for('pestaña3'))

#Ruta para editar estudiantes Tercer Lapso A
@app.route('/editar3A/<string:id>', methods=['POST'])
def edit3A(id):
    
    if request.method == 'POST':
        session['opcion_seleccionada'] = '3'
        
        castellano = request.form['castellano']
        matematica = request.form['matematica']
        GHC = request.form['GHC']
        religion = request.form['religion']
        biologia = request.form['biologia']
        computacion = request.form['computacion']
        ingles = request.form['ingles']
        arte = request.form['arte']
        ed_fisica = request.form['educacion-fisica']
        
        if castellano and matematica and GHC and religion and biologia and computacion and ingles and arte and ed_fisica:
            cursor = db.database.cursor()
            sql= "UPDATE tercer_lapso_a SET Castellano = %s, Matematica = %s, GHC = %s, Religion = %s, Biologia = %s, Computacion = %s, Ingles = %s, Arte = %s, Educacion_fisica = %s WHERE Nro = %s"
            data= (castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica, id)
            cursor.execute(sql, data)
            db.database.commit()
        return redirect(url_for('pestaña3'))

#Ruta para editar estudiantes Tercer Lapso B
@app.route('/editar3B/<string:id>', methods=['POST'])
def edit3B(id):
    
    if request.method == 'POST':
        session['opcion_seleccionada'] = '3'
    
        castellano = request.form['castellano']
        matematica = request.form['matematica']
        GHC = request.form['GHC']
        religion = request.form['religion']
        biologia = request.form['biologia']
        computacion = request.form['computacion']
        ingles = request.form['ingles']
        arte = request.form['arte']
        ed_fisica = request.form['educacion-fisica']
        
        if castellano and matematica and GHC and religion and biologia and computacion and ingles and arte and ed_fisica:
            cursor = db.database.cursor()
            sql= "UPDATE tercer_lapso_b SET Castellano = %s, Matematica = %s, GHC = %s, Religion = %s, Biologia = %s, Computacion = %s, Ingles = %s, Arte = %s, Educacion_fisica = %s WHERE Nro = %s"
            data= (castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica, id)
            cursor.execute(sql, data)
            db.database.commit()
        return redirect(url_for('pestaña3'))

#Ruta para calcular Promedio Primer lapso A
@app.route('/promedio1A/<string:id>')
def promedio1A(id):
    
    session['opcion_seleccionada'] = '1'
    
    cursor = db.database.cursor()
    sqlNotas = "SELECT Castellano, Matematica, GHC, Religion, Biologia, Computacion, Ingles, Arte, Educacion_fisica FROM primer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlNotas, (id, ))
    resultado = cursor.fetchone()
    
    if resultado:
        promedio = sum(resultado) / len(resultado)
        sql= "UPDATE primer_lapso_a SET Promedio = %s WHERE Nro = %s"
        cursor.execute(sql, (promedio, id))
        db.database.commit()
    cursor.close()
    return redirect(url_for('pestaña3'))

#Ruta para calcular Promedio Primer lapso B
@app.route('/promedio1B/<string:id>')
def promedio1B(id):
    
    session['opcion_seleccionada'] = '1'
    
    cursor = db.database.cursor()
    sqlNotas = "SELECT Castellano, Matematica, GHC, Religion, Biologia, Computacion, Ingles, Arte, Educacion_fisica FROM primer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlNotas, (id, ))
    resultado = cursor.fetchone()
    
    if resultado:
        promedio = sum(resultado) / len(resultado)
        sql= "UPDATE primer_lapso_b SET Promedio = %s WHERE Nro = %s"
        cursor.execute(sql, (promedio, id))
        db.database.commit()
    cursor.close()
    return redirect(url_for('pestaña3'))

#Ruta para calcular Promedio Segundo lapso A
@app.route('/promedio2A/<string:id>')
def promedio2A(id):
    
    session['opcion_seleccionada'] = '2'
    
    cursor = db.database.cursor()
    sqlNotas = "SELECT Castellano, Matematica, GHC, Religion, Biologia, Computacion, Ingles, Arte, Educacion_fisica FROM segundo_lapso_a WHERE Nro = %s"
    cursor.execute(sqlNotas, (id, ))
    resultado = cursor.fetchone()
    
    if resultado:
        promedio = sum(resultado) / len(resultado)
        sql= "UPDATE segundo_lapso_a SET Promedio = %s WHERE Nro = %s"
        cursor.execute(sql, (promedio, id))
        db.database.commit()
    cursor.close()
    return redirect(url_for('pestaña3'))

#Ruta para calcular Promedio Segundo lapso B
@app.route('/promedio2B/<string:id>')
def promedio2B(id):
    
    session['opcion_seleccionada'] = '2'
    
    cursor = db.database.cursor()
    sqlNotas = "SELECT Castellano, Matematica, GHC, Religion, Biologia, Computacion, Ingles, Arte, Educacion_fisica FROM segundo_lapso_b WHERE Nro = %s"
    cursor.execute(sqlNotas, (id, ))
    resultado = cursor.fetchone()
    
    if resultado:
        promedio = sum(resultado) / len(resultado)
        sql= "UPDATE segundo_lapso_b SET Promedio = %s WHERE Nro = %s"
        cursor.execute(sql, (promedio, id))
        db.database.commit()
    cursor.close()
    return redirect(url_for('pestaña3'))

#Ruta para calcular Promedio Tercer lapso A
@app.route('/promedio3A/<string:id>')
def promedio3A(id):
    
    session['opcion_seleccionada'] = '3'
    
    cursor = db.database.cursor()
    sqlNotas = "SELECT Castellano, Matematica, GHC, Religion, Biologia, Computacion, Ingles, Arte, Educacion_fisica FROM tercer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlNotas, (id, ))
    resultado = cursor.fetchone()
    
    if resultado:
        promedio = sum(resultado) / len(resultado)
        sql= "UPDATE tercer_lapso_a SET Promedio = %s WHERE Nro = %s"
        cursor.execute(sql, (promedio, id))
        db.database.commit()
    cursor.close()
    return redirect(url_for('pestaña3'))

#Ruta para calcular Promedio Tercer lapso B
@app.route('/promedio3B/<string:id>')
def promedio3B(id):
    
    session['opcion_seleccionada'] = '3'
    
    cursor = db.database.cursor()
    sqlNotas = "SELECT Castellano, Matematica, GHC, Religion, Biologia, Computacion, Ingles, Arte, Educacion_fisica FROM tercer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlNotas, (id, ))
    resultado = cursor.fetchone()
    
    if resultado:
        promedio = sum(resultado) / len(resultado)
        sql= "UPDATE tercer_lapso_b SET Promedio = %s WHERE Nro = %s"
        cursor.execute(sql, (promedio, id))
        db.database.commit()
    cursor.close()
    return redirect(url_for('pestaña3'))

#Ruta de Acceso y Listado a pestaña Agregar
@app.route('/pestaña-agregar', methods=['POST', 'GET'])
@login_required
def pestaña1():
        
    #Tabla A
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM registro_estudiantes_a")
    resultadoRegistro = cursor.fetchall()
    #Datos a diccionario
    insertObjectRegistro=[]
    columnNamesRegistro = [column[0] for column in cursor.description]
    for recordRegistro in resultadoRegistro:
        insertObjectRegistro.append(dict(zip(columnNamesRegistro, recordRegistro)))
        
    #Tabla B
    cursor.execute("SELECT * FROM registro_estudiantes_b")
    resultadoRegistroB = cursor.fetchall()
    #Datos a diccionario
    insertObjectRegistroB=[]
    columnNamesRegistroB = [column[0] for column in cursor.description]
    for recordRegistroB in resultadoRegistroB:
        insertObjectRegistroB.append(dict(zip(columnNamesRegistroB, recordRegistroB)))
        
    #Recuperacion de Datos de logueado
    val_admin = session['rol']
    id_admin = session['id']
    sqlAdmin = "SELECT Nombre_apellido, Rol FROM administradores WHERE ID = %s"
    cursor.execute(sqlAdmin, (id_admin,))
    name_admin = cursor.fetchone()
    nombre_admin = name_admin[0]
    rol_admin = name_admin[1]
    
    cursor.close()
    return render_template('agregar.html', dataRegistro=insertObjectRegistro, dataRegistroB=insertObjectRegistroB, nombre_admin=nombre_admin, rol_admin=rol_admin, val_admin=val_admin)

#Ruta de Acceso y Listado a pestaña Eliminar
@app.route('/pestaña-eliminar', methods=['POST', 'GET'])
@login_required
def pestaña2():
    
    #Tabla A
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM registro_estudiantes_a")
    resultadoRegistro = cursor.fetchall()
    #Datos a diccionario
    insertObjectRegistro=[]
    columnNamesRegistro = [column[0] for column in cursor.description]
    for recordRegistro in resultadoRegistro:
        insertObjectRegistro.append(dict(zip(columnNamesRegistro, recordRegistro)))
        
    #Tabla B
    cursor.execute("SELECT * FROM registro_estudiantes_b")
    resultadoRegistroB = cursor.fetchall()
    #Datos a diccionario
    insertObjectRegistroB=[]
    columnNamesRegistroB = [column[0] for column in cursor.description]
    for recordRegistroB in resultadoRegistroB:
        insertObjectRegistroB.append(dict(zip(columnNamesRegistroB, recordRegistroB)))
        
    #Recuperacion de Datos de logueado
    val_admin = session['rol']
    id_admin = session['id']
    sqlAdmin = "SELECT Nombre_apellido, Rol FROM administradores WHERE ID = %s"
    cursor.execute(sqlAdmin, (id_admin,))
    name_admin = cursor.fetchone()
    nombre_admin = name_admin[0]
    rol_admin = name_admin[1]
    
    cursor.close()
    return render_template('eliminar.html', dataRegistro=insertObjectRegistro, dataRegistroB=insertObjectRegistroB, nombre_admin=nombre_admin, rol_admin=rol_admin, val_admin=val_admin)

#Ruta de Acceso y Listado a pestaña Lapsos
@app.route('/pestaña-lapsos', methods=['POST', 'GET'])
@login_required
def pestaña3():
    
    opcion_seleccionada = session.get('opcion_seleccionada')
    
    #--Primer Lapso--
    
    #Tabla A
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM primer_lapso_a")
    datosPrimerLapsoA = cursor.fetchall()
    #Datos a diccionario
    insertObjectPrimerLapsoA=[]
    columnNamesPrimerLapsoA = [column[0] for column in cursor.description]
    for recordPrimerLapsoA in datosPrimerLapsoA:
        insertObjectPrimerLapsoA.append(dict(zip(columnNamesPrimerLapsoA, recordPrimerLapsoA)))
        
    #Tabla B
    cursor.execute("SELECT * FROM primer_lapso_b")
    datosPrimerLapsoB = cursor.fetchall()
    #Datos a diccionario
    insertObjectPrimerLapsoB=[]
    columnNamesPrimerLapsoB = [column[0] for column in cursor.description]
    for recordPrimerLapsoB in datosPrimerLapsoB:
        insertObjectPrimerLapsoB.append(dict(zip(columnNamesPrimerLapsoB, recordPrimerLapsoB)))
        
    #--Segundo Lapso--
    
    #Tabla A
    cursor.execute("SELECT * FROM segundo_lapso_a")
    datosSegundoLapsoA = cursor.fetchall()
    #Datos a diccionario
    insertObjectSegundoLapsoA=[]
    columnNamesSegundoLapsoA = [column[0] for column in cursor.description]
    for recordSegundoLapsoA in datosSegundoLapsoA:
        insertObjectSegundoLapsoA.append(dict(zip(columnNamesSegundoLapsoA, recordSegundoLapsoA)))
        
    #Tabla B
    cursor.execute("SELECT * FROM segundo_lapso_b")
    datosSegundoLapsoB = cursor.fetchall()
    #Datos a diccionario
    insertObjectSegundoLapsoB=[]
    columnNamesSegundoLapsoB = [column[0] for column in cursor.description]
    for recordSegundoLapsoB in datosSegundoLapsoB:
        insertObjectSegundoLapsoB.append(dict(zip(columnNamesSegundoLapsoB, recordSegundoLapsoB)))
    
    #--Tercer Lapso--
    
    #Tabla A
    cursor.execute("SELECT * FROM tercer_lapso_a")
    datosTercerLapsoA = cursor.fetchall()
    #Datos a diccionario
    insertObjectTercerLapsoA=[]
    columnNamesTercerLapsoA = [column[0] for column in cursor.description]
    for recordTercerLapsoA in datosTercerLapsoA:
        insertObjectTercerLapsoA.append(dict(zip(columnNamesTercerLapsoA, recordTercerLapsoA)))
        
    #Tabla B
    cursor.execute("SELECT * FROM tercer_lapso_b")
    datosTercerLapsoB = cursor.fetchall()
    #Datos a diccionario
    insertObjectTercerLapsoB=[]
    columnNamesTercerLapsoB = [column[0] for column in cursor.description]
    for recordTercerLapsoB in datosTercerLapsoB:
        insertObjectTercerLapsoB.append(dict(zip(columnNamesTercerLapsoB, recordTercerLapsoB)))
        
    #Recuperacion de Datos de logueado
    val_admin = session['rol']
    materia_docente = session['materia']
    id_admin = session['id']
    sqlAdmin = "SELECT Nombre_apellido, Rol FROM administradores WHERE ID = %s"
    cursor.execute(sqlAdmin, (id_admin,))
    name_admin = cursor.fetchone()
    nombre_admin = name_admin[0]
    rol_admin = name_admin[1]
    
    cursor.close()
    return render_template('lapsos.html', dataPrimerLapsoA=insertObjectPrimerLapsoA, dataPrimerLapsoB=insertObjectPrimerLapsoB, dataSegundoLapsoA=insertObjectSegundoLapsoA, dataSegundoLapsoB=insertObjectSegundoLapsoB, dataTercerLapsoA=insertObjectTercerLapsoA, dataTercerLapsoB=insertObjectTercerLapsoB, opcion_seleccionada=opcion_seleccionada, nombre_admin=nombre_admin, rol_admin=rol_admin, val_admin=val_admin, materia_docente=materia_docente)

#Ruta de Acceso y Listado a pestaña Users
@app.route('/pestaña-users', methods=['POST', 'GET'])
@login_required
def users():
    
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM administradores")
    admins = cursor.fetchall()
    insertObjectAdmins=[]
    columnNamesAdmins = [column[0] for column in cursor.description]
    for recordAdmins in admins:
        insertObjectAdmins.append(dict(zip(columnNamesAdmins, recordAdmins)))
        
    #Recuperacion de Datos de logueado
    val_admin = session['rol']
    id_admin = session['id']
    sqlAdmin = "SELECT Nombre_apellido, Rol FROM administradores WHERE ID = %s"
    cursor.execute(sqlAdmin, (id_admin,))
    name_admin = cursor.fetchone()
    nombre_admin = name_admin[0]
    rol_admin = name_admin[1]
    
    cursor.close()
    return render_template('users.html', dataAdmins=insertObjectAdmins, nombre_admin=nombre_admin, rol_admin=rol_admin, val_admin=val_admin)

#Ruta para agregar Admins      
@app.route('/agregar-administrador', methods=['POST'])
def addAdmin():
    
    nombre = request.form['nombre']
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']
    rol = request.form['rol']
    materia = request.form['materia']
    
    if nombre and usuario and contraseña and rol and materia:
        cursor = db.database.cursor()
        sql= "INSERT INTO administradores (Nombre_apellido, Usuario, Contraseña, Rol, Materia) VALUES (%s, %s, %s, %s, %s)"
        data= (nombre, usuario, contraseña, rol, materia)
        cursor.execute(sql, data)
        db.database.commit()
        
    return redirect(url_for('users'))

#Ruta para editar Admins
@app.route('/editarAdmins/<string:id>', methods=['POST'])
def editAdmins(id):
    
    nombre = request.form['edit_nombre']
    usuario = request.form['edit_usuario']
    contraseña = request.form['edit_contraseña']
    rol = request.form['edit_rol']
    materia = request.form['edit_materia']
    
    if nombre and usuario and contraseña and rol and materia:
        cursor = db.database.cursor()
        sql= "UPDATE administradores SET Nombre_apellido = %s, Usuario = %s, Contraseña = %s, Rol = %s, Materia = %s WHERE ID = %s"
        data= (nombre, usuario, contraseña, rol, materia, id)
        cursor.execute(sql, data)
        db.database.commit()
        
    return redirect(url_for('users'))

#Ruta para eliminar Admins
@app.route('/eliminarAdmins/<string:id>')
def eliminarAdmins(id):
    
    cursor = db.database.cursor()
    sql= "DELETE FROM administradores WHERE ID = %s"
    data= (id,)
    cursor.execute(sql, data)
    db.database.commit()
    
    cursor.close()
    return redirect(url_for('users'))

#Ruta de acceso a Login
@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

#Funcion de Login
@app.route('/acceso-login', methods=['GET', 'POST'])
def validacion():
    
    if request.method == 'POST' and 'txtUsuario' in request.form and 'txtContraseña':
        usuario = request.form['txtUsuario']
        contra = request.form['txtContraseña']
        
        cursor = db.database.cursor()
        cursor.execute("SELECT * FROM administradores WHERE Usuario = %s AND Contraseña = %s",(usuario,contra,))
        account = cursor.fetchone()
        
        if account:
            session['logueado'] = True    
            session['id'] = account[0] 
            session['rol'] = account[4]
            session['materia'] = account[5]
            
            user = User(request.form['txtUsuario'])
            login_user(user)
            
            rol_usuario = session['rol']
            
            if rol_usuario == 'Docente':
                return redirect(url_for('pestaña3'))
            else: 
                return redirect(url_for('sistemaT'))
        else:
            mensaje_html = 'Usuario o Contraseña Incorrectos!'
            return render_template('login.html', mensaje=mensaje_html)
        
#Ruta de Acceso y Listado a pestaña Reportes
@app.route('/pestañaReportes', methods=['POST', 'GET'])
@login_required
def pestañaReportes():
    
    #Tabla A
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM registro_estudiantes_a")
    resultadoRegistro = cursor.fetchall()
    #Datos a diccionario
    insertObjectRegistro=[]
    columnNamesRegistro = [column[0] for column in cursor.description]
    for recordRegistro in resultadoRegistro:
        insertObjectRegistro.append(dict(zip(columnNamesRegistro, recordRegistro)))
        
    #Tabla B
    cursor.execute("SELECT * FROM registro_estudiantes_b")
    resultadoRegistroB = cursor.fetchall()
    #Datos a diccionario
    insertObjectRegistroB=[]
    columnNamesRegistroB = [column[0] for column in cursor.description]
    for recordRegistroB in resultadoRegistroB:
        insertObjectRegistroB.append(dict(zip(columnNamesRegistroB, recordRegistroB)))
        
    #Recuperacion de Datos de logueado
    val_admin = session['rol']
    id_admin = session['id']
    sqlAdmin = "SELECT Nombre_apellido, Rol FROM administradores WHERE ID = %s"
    cursor.execute(sqlAdmin, (id_admin,))
    name_admin = cursor.fetchone()
    nombre_admin = name_admin[0]
    rol_admin = name_admin[1]
    
    cursor.close()
    return render_template('reportes.html', dataRegistro=insertObjectRegistro, dataRegistroB=insertObjectRegistroB, nombre_admin=nombre_admin, rol_admin=rol_admin, val_admin=val_admin)

#---Creacion de PDFs---

#--Seccion A--

#Ruta para generar reporte 1er Lapso A
@app.route('/reportLapso1/<string:id>', methods=['GET', 'POST'])
def reportLapso1(id):
    
    #Notas
    cursor = db.database.cursor()
    sqlNotas = "SELECT * FROM primer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlNotas, (id,))
    datos = cursor.fetchone()
    
    nombre = datos[1]
    cedula = datos[3]
    castellano = datos[4]
    matematica = datos[5]
    GHC = datos[6]
    religion = datos[7]
    biologia = datos[8]
    computacion = datos[9]
    ingles = datos[10]
    arte = datos[11]
    ed_fisica = datos[12]
    promedio = str(datos[13])
    
    #Promedios Seccion
    sqlPromCastellano = "SELECT Castellano FROM primer_lapso_a"
    cursor.execute(sqlPromCastellano)
    resCastellano = cursor.fetchall()
    rowCastellano = [row[0] for row in resCastellano]
    promCastellano = round(sum(rowCastellano) / len(rowCastellano))
    
    sqlPromMatematica = "SELECT Matematica FROM primer_lapso_a"
    cursor.execute(sqlPromMatematica)
    resMatematica = cursor.fetchall()
    rowMatematica = [row[0] for row in resMatematica]
    promMatematica = round(sum(rowMatematica) / len(rowMatematica))
    
    sqlPromGHC = "SELECT GHC FROM primer_lapso_a"
    cursor.execute(sqlPromGHC)
    resGHC = cursor.fetchall()
    rowGHC = [row[0] for row in resGHC]
    promGHC = round(sum(rowGHC) / len(rowGHC))
    
    sqlPromReligion = "SELECT Religion FROM primer_lapso_a"
    cursor.execute(sqlPromReligion)
    resReligion = cursor.fetchall()
    rowReligion = [row[0] for row in resReligion]
    promReligion = round(sum(rowReligion) / len(rowReligion))
    
    sqlPromBiologia = "SELECT Biologia FROM primer_lapso_a"
    cursor.execute(sqlPromBiologia)
    resBiologia = cursor.fetchall()
    rowBiologia = [row[0] for row in resBiologia]
    promBiologia = round(sum(rowBiologia) / len(rowBiologia))
    
    sqlPromComputacion = "SELECT Computacion FROM primer_lapso_a"
    cursor.execute(sqlPromComputacion)
    resComputacion = cursor.fetchall()
    rowComputacion = [row[0] for row in resComputacion]
    promComputacion = round(sum(rowComputacion) / len(rowComputacion))
    
    sqlPromIngles = "SELECT Ingles FROM primer_lapso_a"
    cursor.execute(sqlPromIngles)
    resIngles = cursor.fetchall()
    rowIngles = [row[0] for row in resIngles]
    promIngles = round(sum(rowIngles) / len(rowIngles))
    
    sqlPromArte = "SELECT Arte FROM primer_lapso_a"
    cursor.execute(sqlPromArte)
    resArte = cursor.fetchall()
    rowArte = [row[0] for row in resArte]
    promArte = round(sum(rowArte) / len(rowArte))
    
    sqlPromEd_fisica = "SELECT Educacion_fisica FROM primer_lapso_a"
    cursor.execute(sqlPromEd_fisica)
    resEd_fisica = cursor.fetchall()
    rowEd_fisica = [row[0] for row in resEd_fisica]
    promEd_fisica = round(sum(rowEd_fisica) / len(rowEd_fisica))
    
    #Promedio General Seccion
    promedioGeneralLapsoSeccion = str(round((promCastellano + promMatematica + promGHC + promReligion + promBiologia + promComputacion + promIngles + promArte + promEd_fisica) / 9 , 2))
    
    #Grafico
    bar_width = 0.35
    separacion = 0.5
    x = np.arange(9) * (bar_width * 2 + separacion)
    y1 = [castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica]
    y2 = [promCastellano, promMatematica, promGHC, promReligion, promBiologia, promComputacion, promIngles, promArte, promEd_fisica]

    fig, ax = plt.subplots(figsize=(6, 2))
    bar1 = ax.bar(x - bar_width/2, y1, bar_width, label='Nota', color='black')
    bar2 = ax.bar(x + bar_width/2, y2, bar_width, label='Prom. Sec.', color='gray')

    ax.set_ylabel('Notas')
    ax.set_xticks(x)
    ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig('static/graficos/graficoIndividual1A.png')
     
    #Fecha
    fecha = datetime.datetime.now()
    fechaBuena = fecha.strftime('%d/%m/%Y')
    
    #--PDF--
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    #Cuadro Datos colegio
    pdf.set_font('Arial', '', 12)
    pdf.rect(x=10, y=10, w=190, h=130)
    pdf.text(x=50, y=15, txt='Unidad Educativa')
    pdf.text(x=50, y=21, txt='Padre José Cueto')
    pdf.line(50, 23, 84, 23)
    pdf.text(x=53, y=28, txt='Código Plantel:')
    pdf.text(x=55, y=34, txt='PD04022317')
    pdf.line(50, 36, 84, 36)
    pdf.text(x=49, y=41, txt='RIF: J-31435772-7')
    pdf.line(50, 43, 84, 43)
    pdf.line(10, 46, 200, 46)
    pdf.line(88, 10, 88, 46)
    pdf.image('static/imagenes/cueto2.jpeg', x=17, y=13, w=25, h=30)
    
    #Cuadro datos estudiante
    pdf.set_font('Arial', 'B', 12)
    pdf.text(x=100, y=14, txt='' + nombre)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.text(x=130, y=19, txt='Educación Media')
    
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=105, y=24, txt='N° CÉDULA: ' + cedula)
    pdf.text(x=99, y=29, txt='AÑO / SECCIÓN: 1ero / "A"')
    pdf.text(x=92, y=34, txt='PERIODO ESCOLAR: 2020-2021')
    pdf.text(x=112, y=38, txt='LAPSO: Primero')
    pdf.text(x=91, y=43, txt='FECHA DE ENTREGA: ' + fechaBuena)
    
    #Titulo boletines
    pdf.set_font('Arial', 'B', 12)
    pdf.text(x=78, y=51, txt='BOLETÍN DE CALIFICACIONES')
    pdf.line(10, 53, 200, 53)

    #Contenido General
    pdf.line(10, 68, 200, 68)
    pdf.line(16, 68, 16, 134)
    pdf.line(10, 134, 200, 134)
    pdf.set_font('Arial', '', 11)
    pdf.text(x=11, y=72, txt='01')
    pdf.text(x=11, y=78, txt='02')
    pdf.text(x=11, y=84, txt='03')
    pdf.text(x=11, y=90, txt='04')
    pdf.text(x=11, y=96, txt='05')
    pdf.text(x=11, y=102, txt='06')
    pdf.text(x=11, y=108, txt='07')
    pdf.text(x=11, y=114, txt='08')
    pdf.text(x=11, y=120, txt='09')
    pdf.text(x=11, y=126, txt='10')
    pdf.text(x=11, y=132, txt='11')
    pdf.text(x=19, y=72, txt='Castellano')
    pdf.text(x=19, y=78, txt='Matemática')
    pdf.text(x=19, y=84, txt='GHC')
    pdf.text(x=19, y=90, txt='Religión')
    pdf.text(x=19, y=96, txt='Biología')
    pdf.text(x=19, y=102, txt='Computación')
    pdf.text(x=19, y=108, txt='Inglés')
    pdf.text(x=19, y=114, txt='Arte')
    pdf.text(x=19, y=120, txt='Educación Física')
    pdf.line(65, 53, 65, 140)
    pdf.line(104, 53, 104, 140)
    pdf.line(65, 60, 200, 60)
    pdf.line(152, 68, 152, 140)
    pdf.set_font('Arial', 'B', 11)
    pdf.text(x=24, y=62, txt='ASIGNATURAS')
    pdf.text(x=75, y=58, txt='1° LAPSO')
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=67, y=65, txt='DEFINITIVA DE LAPSO')
    pdf.set_font('Arial', '', 9)
    pdf.text(x=83, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=83, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=83, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=83, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=83, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=83, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=83, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=83, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=83, y=120, txt='' + f"{ed_fisica:02d}")
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=19, y=138, txt='Promedios Comparativos:')
    pdf.text(x=81, y=138, txt='' + promedio)
    pdf.text(x=108, y=138, txt='' + promedio)
    pdf.text(x=128, y=138, txt='--')
    pdf.text(x=144, y=138, txt='--')
    pdf.text(x=162, y=138, txt='' + promedio)
    pdf.text(x=185, y=138, txt='' + promedioGeneralLapsoSeccion)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=130, y=58, txt='RESUMEN DE EVALUACIÓN')
    
    pdf.set_font('Arial', '', 8)
    pdf.text(x=106, y=63, txt='PRIMER')
    pdf.text(x=107, y=67, txt='LAPSO')
    pdf.text(x=121, y=63, txt='SEGUNDO')
    pdf.text(x=123, y=67, txt='LAPSO')
    pdf.text(x=139, y=63, txt='TERCER')
    pdf.text(x=140, y=67, txt='LAPSO')
    pdf.text(x=162, y=63, txt='NOTA')
    pdf.text(x=158, y=67, txt='DEFINITIVA')
    pdf.text(x=185, y=63, txt='PROM.')
    pdf.text(x=186, y=67, txt='SEC.')
    
    pdf.set_font('Arial', '', 9)
    pdf.text(x=110, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=110, y=78, txt='' +  f"{matematica:02d}")
    pdf.text(x=110, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=110, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=110, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=110, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=110, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=110, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=110, y=120, txt='' + f"{ed_fisica:02d}")
    
    pdf.text(x=128, y=72, txt='-')
    pdf.text(x=128, y=78, txt='-')
    pdf.text(x=128, y=84, txt='-')
    pdf.text(x=128, y=90, txt='-')
    pdf.text(x=128, y=96, txt='-')
    pdf.text(x=128, y=102, txt='-')
    pdf.text(x=128, y=108, txt='-')
    pdf.text(x=128, y=114, txt='-')
    pdf.text(x=128, y=120, txt='-')
    
    pdf.text(x=145, y=72, txt='-')
    pdf.text(x=145, y=78, txt='-')
    pdf.text(x=145, y=84, txt='-')
    pdf.text(x=145, y=90, txt='-')
    pdf.text(x=145, y=96, txt='-')
    pdf.text(x=145, y=102, txt='-')
    pdf.text(x=145, y=108, txt='-')
    pdf.text(x=145, y=114, txt='-')
    pdf.text(x=145, y=120, txt='-')
    
    pdf.text(x=164, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=164, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=164, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=164, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=164, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=164, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=164, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=164, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=164, y=120, txt='' + f"{ed_fisica:02d}")
    
    pdf.text(x=187, y=72, txt='' + f"{promCastellano:02d}")
    pdf.text(x=187, y=78, txt='' + f"{promMatematica:02d}")
    pdf.text(x=187, y=84, txt='' + f"{promGHC:02d}")
    pdf.text(x=187, y=90, txt='' + f"{promReligion:02d}")
    pdf.text(x=187, y=96, txt='' + f"{promBiologia:02d}")
    pdf.text(x=187, y=102, txt='' + f"{promComputacion:02d}")
    pdf.text(x=187, y=108, txt='' + f"{promIngles:02d}")
    pdf.text(x=187, y=114, txt='' + f"{promArte:02d}")
    pdf.text(x=187, y=120, txt='' + f"{promEd_fisica:02d}")
    
    #Grafico, Observaciones, Sello y Firmas
    pdf.rect(x=10, y=146, w=142, h=50)
    pdf.rect(x=10, y=197, w=190, h=57)
    pdf.line(153, 146, 200, 146)
    pdf.line(153, 146, 153, 197)
    pdf.line(200, 146, 200, 197)
    pdf.line(10, 204, 200, 204)
    pdf.line(10, 238, 200, 238)
    pdf.line(73, 238, 73, 254)
    pdf.line(136, 238, 136, 254)
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=52, y=144, txt='GRÁFICO DEL PROGRESO ESCOLAR')
    pdf.text(x=60, y=202, txt='OBSERVACIONES SOBRE LA ACTUACIÓN DEL ESTUDIANTE')
    pdf.set_font('Arial', 'B', 8)
    pdf.text(x=163, y=172, txt='SELLO DEL PLANTEL')
    pdf.text(x=20, y=253, txt='DIRECTOR/A: YULEIDA ROJAS')
    pdf.text(x=85, y=253, txt='SUBDIRECTOR: ??????')
    pdf.text(x=144, y=253, txt='COORD. ACAD: CARMELO BOSCÁN')
    pdf.image('static/graficos/graficoIndividual1A.png', x=11, y=147, w=140, h=48)
    
    #Guardado y descarga
    pdf_path = os.path.join('pdfs', f'{nombre}-PrimerLapso.pdf')
    pdf.output(pdf_path)
    cursor.close()
    return redirect(url_for('descargarPdf1A', nombre=nombre))

#Ruta para generar reporte 2do Lapso A
@app.route('/reportLapso2/<string:id>', methods=['GET', 'POST'])
def reportLapso2(id):
    
    #Notas
    cursor = db.database.cursor()
    sqlNotas = "SELECT * FROM segundo_lapso_a WHERE Nro = %s"
    cursor.execute(sqlNotas, (id,))
    datos = cursor.fetchone()
    
    nombre = datos[1]
    cedula = datos[3]
    castellano = datos[4]
    matematica = datos[5]
    GHC = datos[6]
    religion = datos[7]
    biologia = datos[8]
    computacion = datos[9]
    ingles = datos[10]
    arte = datos[11]
    ed_fisica = datos[12]
    promedio = str(datos[13])
    
    #Promedios Seccion
    sqlPromCastellano = "SELECT Castellano FROM segundo_lapso_a"
    cursor.execute(sqlPromCastellano)
    resCastellano = cursor.fetchall()
    rowCastellano = [row[0] for row in resCastellano]
    promCastellano = round(sum(rowCastellano) / len(rowCastellano))
    
    sqlPromMatematica = "SELECT Matematica FROM segundo_lapso_a"
    cursor.execute(sqlPromMatematica)
    resMatematica = cursor.fetchall()
    rowMatematica = [row[0] for row in resMatematica]
    promMatematica = round(sum(rowMatematica) / len(rowMatematica))
    
    sqlPromGHC = "SELECT GHC FROM segundo_lapso_a"
    cursor.execute(sqlPromGHC)
    resGHC = cursor.fetchall()
    rowGHC = [row[0] for row in resGHC]
    promGHC = round(sum(rowGHC) / len(rowGHC))
    
    sqlPromReligion = "SELECT Religion FROM segundo_lapso_a"
    cursor.execute(sqlPromReligion)
    resReligion = cursor.fetchall()
    rowReligion = [row[0] for row in resReligion]
    promReligion = round(sum(rowReligion) / len(rowReligion))
    
    sqlPromBiologia = "SELECT Biologia FROM segundo_lapso_a"
    cursor.execute(sqlPromBiologia)
    resBiologia = cursor.fetchall()
    rowBiologia = [row[0] for row in resBiologia]
    promBiologia = round(sum(rowBiologia) / len(rowBiologia))
    
    sqlPromComputacion = "SELECT Computacion FROM segundo_lapso_a"
    cursor.execute(sqlPromComputacion)
    resComputacion = cursor.fetchall()
    rowComputacion = [row[0] for row in resComputacion]
    promComputacion = round(sum(rowComputacion) / len(rowComputacion))
    
    sqlPromIngles = "SELECT Ingles FROM segundo_lapso_a"
    cursor.execute(sqlPromIngles)
    resIngles = cursor.fetchall()
    rowIngles = [row[0] for row in resIngles]
    promIngles = round(sum(rowIngles) / len(rowIngles))
    
    sqlPromArte = "SELECT Arte FROM segundo_lapso_a"
    cursor.execute(sqlPromArte)
    resArte = cursor.fetchall()
    rowArte = [row[0] for row in resArte]
    promArte = round(sum(rowArte) / len(rowArte))
    
    sqlPromEd_fisica = "SELECT Educacion_fisica FROM segundo_lapso_a"
    cursor.execute(sqlPromEd_fisica)
    resEd_fisica = cursor.fetchall()
    rowEd_fisica = [row[0] for row in resEd_fisica]
    promEd_fisica = round(sum(rowEd_fisica) / len(rowEd_fisica))
    
    #Promedio General Seccion
    promedioGeneralLapsoSeccion = str(round((promCastellano + promMatematica + promGHC + promReligion + promBiologia + promComputacion + promIngles + promArte + promEd_fisica) / 9 , 2))
    
    #Grafico
    bar_width = 0.35
    separacion = 0.5
    x = np.arange(9) * (bar_width * 2 + separacion)
    y1 = [castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica]
    y2 = [promCastellano, promMatematica, promGHC, promReligion, promBiologia, promComputacion, promIngles, promArte, promEd_fisica]

    fig, ax = plt.subplots(figsize=(6, 2))
    bar1 = ax.bar(x - bar_width/2, y1, bar_width, label='Nota', color='black')
    bar2 = ax.bar(x + bar_width/2, y2, bar_width, label='Prom. Sec.', color='gray')

    ax.set_ylabel('Notas')
    ax.set_xticks(x)
    ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig('static/graficos/graficoIndividual2A.png')
     
    #Fecha
    fecha = datetime.datetime.now()
    fechaBuena = fecha.strftime('%d/%m/%Y')
    
    #--PDF--
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    #Cuadro Datos colegio
    pdf.set_font('Arial', '', 12)
    pdf.rect(x=10, y=10, w=190, h=130)
    pdf.text(x=50, y=15, txt='Unidad Educativa')
    pdf.text(x=50, y=21, txt='Padre José Cueto')
    pdf.line(50, 23, 84, 23)
    pdf.text(x=53, y=28, txt='Código Plantel:')
    pdf.text(x=55, y=34, txt='PD04022317')
    pdf.line(50, 36, 84, 36)
    pdf.text(x=49, y=41, txt='RIF: J-31435772-7')
    pdf.line(50, 43, 84, 43)
    pdf.line(10, 46, 200, 46)
    pdf.line(88, 10, 88, 46)
    pdf.image('static/imagenes/cueto2.jpeg', x=17, y=13, w=25, h=30)
    
    #Cuadro datos estudiante
    pdf.set_font('Arial', 'B', 12)
    pdf.text(x=100, y=14, txt='' + nombre)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.text(x=130, y=19, txt='Educación Media')
    
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=105, y=24, txt='N° CÉDULA: ' + cedula)
    pdf.text(x=99, y=29, txt='AÑO / SECCIÓN: 1ero / "A"')
    pdf.text(x=92, y=34, txt='PERIODO ESCOLAR: 2020-2021')
    pdf.text(x=112, y=38, txt='LAPSO: Segundo')
    pdf.text(x=91, y=43, txt='FECHA DE ENTREGA: ' + fechaBuena)
    
    #Titulo boletines
    pdf.set_font('Arial', 'B', 12)
    pdf.text(x=78, y=51, txt='BOLETÍN DE CALIFICACIONES')
    pdf.line(10, 53, 200, 53)

    #Contenido General
    pdf.line(10, 68, 200, 68)
    pdf.line(16, 68, 16, 134)
    pdf.line(10, 134, 200, 134)
    pdf.set_font('Arial', '', 11)
    pdf.text(x=11, y=72, txt='01')
    pdf.text(x=11, y=78, txt='02')
    pdf.text(x=11, y=84, txt='03')
    pdf.text(x=11, y=90, txt='04')
    pdf.text(x=11, y=96, txt='05')
    pdf.text(x=11, y=102, txt='06')
    pdf.text(x=11, y=108, txt='07')
    pdf.text(x=11, y=114, txt='08')
    pdf.text(x=11, y=120, txt='09')
    pdf.text(x=11, y=126, txt='10')
    pdf.text(x=11, y=132, txt='11')
    pdf.text(x=19, y=72, txt='Castellano')
    pdf.text(x=19, y=78, txt='Matemática')
    pdf.text(x=19, y=84, txt='GHC')
    pdf.text(x=19, y=90, txt='Religión')
    pdf.text(x=19, y=96, txt='Biología')
    pdf.text(x=19, y=102, txt='Computación')
    pdf.text(x=19, y=108, txt='Inglés')
    pdf.text(x=19, y=114, txt='Arte')
    pdf.text(x=19, y=120, txt='Educación Física')
    pdf.line(65, 53, 65, 140)
    pdf.line(104, 53, 104, 140)
    pdf.line(65, 60, 200, 60)
    pdf.line(152, 68, 152, 140)
    pdf.set_font('Arial', 'B', 11)
    pdf.text(x=24, y=62, txt='ASIGNATURAS')
    pdf.text(x=75, y=58, txt='2° LAPSO')
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=67, y=65, txt='DEFINITIVA DE LAPSO')
    pdf.set_font('Arial', '', 9)
    pdf.text(x=83, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=83, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=83, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=83, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=83, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=83, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=83, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=83, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=83, y=120, txt='' + f"{ed_fisica:02d}")
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=19, y=138, txt='Promedios Comparativos:')
    pdf.text(x=81, y=138, txt='' + promedio)
    pdf.text(x=108, y=138, txt='--')
    pdf.text(x=124, y=138, txt='' + promedio)
    pdf.text(x=144, y=138, txt='--')
    pdf.text(x=162, y=138, txt='' + promedio)
    pdf.text(x=185, y=138, txt='' + promedioGeneralLapsoSeccion)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=130, y=58, txt='RESUMEN DE EVALUACIÓN')
    
    pdf.set_font('Arial', '', 8)
    pdf.text(x=106, y=63, txt='PRIMER')
    pdf.text(x=107, y=67, txt='LAPSO')
    pdf.text(x=121, y=63, txt='SEGUNDO')
    pdf.text(x=123, y=67, txt='LAPSO')
    pdf.text(x=139, y=63, txt='TERCER')
    pdf.text(x=140, y=67, txt='LAPSO')
    pdf.text(x=162, y=63, txt='NOTA')
    pdf.text(x=158, y=67, txt='DEFINITIVA')
    pdf.text(x=185, y=63, txt='PROM.')
    pdf.text(x=186, y=67, txt='SEC.')
    
    pdf.set_font('Arial', '', 9)
    pdf.text(x=110, y=72, txt='-')
    pdf.text(x=110, y=78, txt='-')
    pdf.text(x=110, y=84, txt='-')
    pdf.text(x=110, y=90, txt='-')
    pdf.text(x=110, y=96, txt='-')
    pdf.text(x=110, y=102, txt='-')
    pdf.text(x=110, y=108, txt='-')
    pdf.text(x=110, y=114, txt='-')
    pdf.text(x=110, y=120, txt='-')
    
    pdf.text(x=126, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=126, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=126, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=126, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=126, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=126, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=126, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=126, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=126, y=120, txt='' + f"{ed_fisica:02d}")
    
    pdf.text(x=145, y=72, txt='-')
    pdf.text(x=145, y=78, txt='-')
    pdf.text(x=145, y=84, txt='-')
    pdf.text(x=145, y=90, txt='-')
    pdf.text(x=145, y=96, txt='-')
    pdf.text(x=145, y=102, txt='-')
    pdf.text(x=145, y=108, txt='-')
    pdf.text(x=145, y=114, txt='-')
    pdf.text(x=145, y=120, txt='-')
    
    pdf.text(x=164, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=164, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=164, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=164, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=164, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=164, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=164, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=164, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=164, y=120, txt='' + f"{ed_fisica:02d}")
    
    pdf.text(x=187, y=72, txt='' + f"{promCastellano:02d}")
    pdf.text(x=187, y=78, txt='' + f"{promMatematica:02d}")
    pdf.text(x=187, y=84, txt='' + f"{promGHC:02d}")
    pdf.text(x=187, y=90, txt='' + f"{promReligion:02d}")
    pdf.text(x=187, y=96, txt='' + f"{promBiologia:02d}")
    pdf.text(x=187, y=102, txt='' + f"{promComputacion:02d}")
    pdf.text(x=187, y=108, txt='' + f"{promIngles:02d}")
    pdf.text(x=187, y=114, txt='' + f"{promArte:02d}")
    pdf.text(x=187, y=120, txt='' + f"{promEd_fisica:02d}")
    
    #Grafico, Observaciones, Sello y Firmas
    pdf.rect(x=10, y=146, w=142, h=50)
    pdf.rect(x=10, y=197, w=190, h=57)
    pdf.line(153, 146, 200, 146)
    pdf.line(153, 146, 153, 197)
    pdf.line(200, 146, 200, 197)
    pdf.line(10, 204, 200, 204)
    pdf.line(10, 238, 200, 238)
    pdf.line(73, 238, 73, 254)
    pdf.line(136, 238, 136, 254)
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=52, y=144, txt='GRÁFICO DEL PROGRESO ESCOLAR')
    pdf.text(x=60, y=202, txt='OBSERVACIONES SOBRE LA ACTUACIÓN DEL ESTUDIANTE')
    pdf.set_font('Arial', 'B', 8)
    pdf.text(x=163, y=172, txt='SELLO DEL PLANTEL')
    pdf.text(x=20, y=253, txt='DIRECTOR/A: YULEIDA ROJAS')
    pdf.text(x=85, y=253, txt='SUBDIRECTOR: ??????')
    pdf.text(x=144, y=253, txt='COORD. ACAD: CARMELO BOSCÁN')
    pdf.image('static/graficos/graficoIndividual2A.png', x=11, y=147, w=140, h=48)
    
    #Guardado y descarga
    pdf_path = os.path.join('pdfs', f'{nombre}-SegundoLapso.pdf')
    pdf.output(pdf_path)
    cursor.close()
    return redirect(url_for('descargarPdf2A', nombre=nombre))

#Ruta para generar reporte 3er Lapso A
@app.route('/reportLapso3/<string:id>', methods=['GET', 'POST'])
def reportLapso3(id):
    
    #Notas 3er Lapso
    cursor = db.database.cursor()
    sqlNotas = "SELECT * FROM tercer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlNotas, (id,))
    datos = cursor.fetchone()
    
    nombre = datos[1]
    cedula = datos[3]
    castellano = datos[4]
    matematica = datos[5]
    GHC = datos[6]
    religion = datos[7]
    biologia = datos[8]
    computacion = datos[9]
    ingles = datos[10]
    arte = datos[11]
    ed_fisica = datos[12]
    promedio = str(datos[13])
    
    #Notas 1er Lapso
    sqlNotas1erLapso = "SELECT * FROM primer_lapso_a WHERE Nro = %s"
    cursor.execute(sqlNotas1erLapso, (id,))
    datosLapso1 = cursor.fetchone()
    
    castellanoLapso1 = datosLapso1[4]
    matematicaLapso1 = datosLapso1[5]
    GHCLapso1 = datosLapso1[6]
    religionLapso1 = datosLapso1[7]
    biologiaLapso1 = datosLapso1[8]
    computacionLapso1 = datosLapso1[9]
    inglesLapso1 = datosLapso1[10]
    arteLapso1 = datosLapso1[11]
    ed_fisicaLapso1 = datosLapso1[12]
    promedioLapso1 = str(datosLapso1[13])
    
    #Notas 2do Lapso
    sqlNotas2doLapso = "SELECT * FROM segundo_lapso_a WHERE Nro = %s"
    cursor.execute(sqlNotas2doLapso, (id,))
    datosLapso2 = cursor.fetchone()
    
    castellanoLapso2 = datosLapso2[4]
    matematicaLapso2 = datosLapso2[5]
    GHCLapso2 = datosLapso2[6]
    religionLapso2 = datosLapso2[7]
    biologiaLapso2 = datosLapso2[8]
    computacionLapso2 = datosLapso2[9]
    inglesLapso2 = datosLapso2[10]
    arteLapso2 = datosLapso2[11]
    ed_fisicaLapso2 = datosLapso2[12]
    promedioLapso2 = str(datosLapso2[13])
    
    #Notas Definitivas y Promedio Final de Año
    sqlNotasFinales = "SELECT * FROM seccion_a WHERE Nro = %s"
    cursor.execute(sqlNotasFinales, (id,))
    datosFinales = cursor.fetchone()
    
    castellanoFinal = datosFinales[4]
    matematicaFinal = datosFinales[5]
    GHCFinal = datosFinales[6]
    religionFinal = datosFinales[7]
    biologiaFinal = datosFinales[8]
    computacionFinal = datosFinales[9]
    inglesFinal = datosFinales[10]
    arteFinal = datosFinales[11]
    ed_fisicaFinal = datosFinales[12]
    promedioFinal = str(datosFinales[13])
    
    #Promedios Seccion
    sqlPromCastellano = "SELECT Castellano FROM tercer_lapso_a"
    cursor.execute(sqlPromCastellano)
    resCastellano = cursor.fetchall()
    rowCastellano = [row[0] for row in resCastellano]
    promCastellano = round(sum(rowCastellano) / len(rowCastellano))
    
    sqlPromMatematica = "SELECT Matematica FROM tercer_lapso_a"
    cursor.execute(sqlPromMatematica)
    resMatematica = cursor.fetchall()
    rowMatematica = [row[0] for row in resMatematica]
    promMatematica = round(sum(rowMatematica) / len(rowMatematica))
    
    sqlPromGHC = "SELECT GHC FROM tercer_lapso_a"
    cursor.execute(sqlPromGHC)
    resGHC = cursor.fetchall()
    rowGHC = [row[0] for row in resGHC]
    promGHC = round(sum(rowGHC) / len(rowGHC))
    
    sqlPromReligion = "SELECT Religion FROM tercer_lapso_a"
    cursor.execute(sqlPromReligion)
    resReligion = cursor.fetchall()
    rowReligion = [row[0] for row in resReligion]
    promReligion = round(sum(rowReligion) / len(rowReligion))
    
    sqlPromBiologia = "SELECT Biologia FROM tercer_lapso_a"
    cursor.execute(sqlPromBiologia)
    resBiologia = cursor.fetchall()
    rowBiologia = [row[0] for row in resBiologia]
    promBiologia = round(sum(rowBiologia) / len(rowBiologia))
    
    sqlPromComputacion = "SELECT Computacion FROM tercer_lapso_a"
    cursor.execute(sqlPromComputacion)
    resComputacion = cursor.fetchall()
    rowComputacion = [row[0] for row in resComputacion]
    promComputacion = round(sum(rowComputacion) / len(rowComputacion))
    
    sqlPromIngles = "SELECT Ingles FROM tercer_lapso_a"
    cursor.execute(sqlPromIngles)
    resIngles = cursor.fetchall()
    rowIngles = [row[0] for row in resIngles]
    promIngles = round(sum(rowIngles) / len(rowIngles))
    
    sqlPromArte = "SELECT Arte FROM tercer_lapso_a"
    cursor.execute(sqlPromArte)
    resArte = cursor.fetchall()
    rowArte = [row[0] for row in resArte]
    promArte = round(sum(rowArte) / len(rowArte))
    
    sqlPromEd_fisica = "SELECT Educacion_fisica FROM tercer_lapso_a"
    cursor.execute(sqlPromEd_fisica)
    resEd_fisica = cursor.fetchall()
    rowEd_fisica = [row[0] for row in resEd_fisica]
    promEd_fisica = round(sum(rowEd_fisica) / len(rowEd_fisica))
    
    #Promedio General Seccion
    promedioGeneralLapsoSeccion = str(round((promCastellano + promMatematica + promGHC + promReligion + promBiologia + promComputacion + promIngles + promArte + promEd_fisica) / 9 , 2))
    
    #Grafico
    bar_width = 0.35
    separacion = 0.5
    x = np.arange(9) * (bar_width * 2 + separacion)
    y1 = [castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica]
    y2 = [promCastellano, promMatematica, promGHC, promReligion, promBiologia, promComputacion, promIngles, promArte, promEd_fisica]

    fig, ax = plt.subplots(figsize=(6, 2))
    bar1 = ax.bar(x - bar_width/2, y1, bar_width, label='Nota', color='black')
    bar2 = ax.bar(x + bar_width/2, y2, bar_width, label='Prom. Sec.', color='gray')

    ax.set_ylabel('Notas')
    ax.set_xticks(x)
    ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig('static/graficos/graficoIndividual3A.png')
     
    #Fecha
    fecha = datetime.datetime.now()
    fechaBuena = fecha.strftime('%d/%m/%Y')
    
    #--PDF--
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    #Cuadro Datos colegio
    pdf.set_font('Arial', '', 12)
    pdf.rect(x=10, y=10, w=190, h=130)
    pdf.text(x=50, y=15, txt='Unidad Educativa')
    pdf.text(x=50, y=21, txt='Padre José Cueto')
    pdf.line(50, 23, 84, 23)
    pdf.text(x=53, y=28, txt='Código Plantel:')
    pdf.text(x=55, y=34, txt='PD04022317')
    pdf.line(50, 36, 84, 36)
    pdf.text(x=49, y=41, txt='RIF: J-31435772-7')
    pdf.line(50, 43, 84, 43)
    pdf.line(10, 46, 200, 46)
    pdf.line(88, 10, 88, 46)
    pdf.image('static/imagenes/cueto2.jpeg', x=17, y=13, w=25, h=30)
    
    #Cuadro datos estudiante
    pdf.set_font('Arial', 'B', 12)
    pdf.text(x=100, y=14, txt='' + nombre)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.text(x=130, y=19, txt='Educación Media')
    
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=105, y=24, txt='N° CÉDULA: ' + cedula)
    pdf.text(x=99, y=29, txt='AÑO / SECCIÓN: 1ero / "A"')
    pdf.text(x=92, y=34, txt='PERIODO ESCOLAR: 2020-2021')
    pdf.text(x=112, y=38, txt='LAPSO: Tercero')
    pdf.text(x=91, y=43, txt='FECHA DE ENTREGA: ' + fechaBuena)
    
    #Titulo boletines
    pdf.set_font('Arial', 'B', 12)
    pdf.text(x=78, y=51, txt='BOLETÍN DE CALIFICACIONES')
    pdf.line(10, 53, 200, 53)

    #Contenido General
    pdf.line(10, 68, 200, 68)
    pdf.line(16, 68, 16, 134)
    pdf.line(10, 134, 200, 134)
    pdf.set_font('Arial', '', 11)
    pdf.text(x=11, y=72, txt='01')
    pdf.text(x=11, y=78, txt='02')
    pdf.text(x=11, y=84, txt='03')
    pdf.text(x=11, y=90, txt='04')
    pdf.text(x=11, y=96, txt='05')
    pdf.text(x=11, y=102, txt='06')
    pdf.text(x=11, y=108, txt='07')
    pdf.text(x=11, y=114, txt='08')
    pdf.text(x=11, y=120, txt='09')
    pdf.text(x=11, y=126, txt='10')
    pdf.text(x=11, y=132, txt='11')
    pdf.text(x=19, y=72, txt='Castellano')
    pdf.text(x=19, y=78, txt='Matemática')
    pdf.text(x=19, y=84, txt='GHC')
    pdf.text(x=19, y=90, txt='Religión')
    pdf.text(x=19, y=96, txt='Biología')
    pdf.text(x=19, y=102, txt='Computación')
    pdf.text(x=19, y=108, txt='Inglés')
    pdf.text(x=19, y=114, txt='Arte')
    pdf.text(x=19, y=120, txt='Educación Física')
    pdf.line(65, 53, 65, 140)
    pdf.line(104, 53, 104, 140)
    pdf.line(65, 60, 200, 60)
    pdf.line(152, 68, 152, 140)
    pdf.set_font('Arial', 'B', 11)
    pdf.text(x=24, y=62, txt='ASIGNATURAS')
    pdf.text(x=75, y=58, txt='3° LAPSO')
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=67, y=65, txt='DEFINITIVA DE LAPSO')
    pdf.set_font('Arial', '', 9)
    pdf.text(x=83, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=83, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=83, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=83, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=83, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=83, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=83, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=83, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=83, y=120, txt='' + f"{ed_fisica:02d}")
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=19, y=138, txt='Promedios Comparativos:')
    pdf.text(x=81, y=138, txt='' + promedio)
    pdf.text(x=108, y=138, txt='' + promedioLapso1)
    pdf.text(x=125, y=138, txt='' + promedioLapso2)
    pdf.text(x=141, y=138, txt='' + promedio)
    pdf.text(x=162, y=138, txt='' + promedioFinal)
    pdf.text(x=185, y=138, txt='' + promedioGeneralLapsoSeccion)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=130, y=58, txt='RESUMEN DE EVALUACIÓN')
    
    pdf.set_font('Arial', '', 8)
    pdf.text(x=106, y=63, txt='PRIMER')
    pdf.text(x=107, y=67, txt='LAPSO')
    pdf.text(x=121, y=63, txt='SEGUNDO')
    pdf.text(x=123, y=67, txt='LAPSO')
    pdf.text(x=139, y=63, txt='TERCER')
    pdf.text(x=140, y=67, txt='LAPSO')
    pdf.text(x=162, y=63, txt='NOTA')
    pdf.text(x=158, y=67, txt='DEFINITIVA')
    pdf.text(x=185, y=63, txt='PROM.')
    pdf.text(x=186, y=67, txt='SEC.')
    
    pdf.set_font('Arial', '', 9)
    pdf.text(x=110, y=72, txt='' + f"{castellanoLapso1:02d}")
    pdf.text(x=110, y=78, txt='' + f"{matematicaLapso1:02d}")
    pdf.text(x=110, y=84, txt='' + f"{GHCLapso1:02d}")
    pdf.text(x=110, y=90, txt='' + f"{religionLapso1:02d}")
    pdf.text(x=110, y=96, txt='' + f"{biologiaLapso1:02d}")
    pdf.text(x=110, y=102, txt='' + f"{computacionLapso1:02d}")
    pdf.text(x=110, y=108, txt='' + f"{inglesLapso1:02d}")
    pdf.text(x=110, y=114, txt='' + f"{arteLapso1:02d}")
    pdf.text(x=110, y=120, txt='' + f"{ed_fisicaLapso1:02d}")
    
    pdf.text(x=127, y=72, txt='' + f"{castellanoLapso2:02d}")
    pdf.text(x=127, y=78, txt='' + f"{matematicaLapso2:02d}")
    pdf.text(x=127, y=84, txt='' + f"{GHCLapso2:02d}")
    pdf.text(x=127, y=90, txt='' + f"{religionLapso2:02d}")
    pdf.text(x=127, y=96, txt='' + f"{biologiaLapso2:02d}")
    pdf.text(x=127, y=102, txt='' + f"{computacionLapso2:02d}")
    pdf.text(x=127, y=108, txt='' + f"{inglesLapso2:02d}")
    pdf.text(x=127, y=114, txt='' + f"{arteLapso2:02d}")
    pdf.text(x=127, y=120, txt='' + f"{ed_fisicaLapso2:02d}")
    
    pdf.text(x=143, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=143, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=143, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=143, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=143, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=143, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=143, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=143, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=143, y=120, txt='' + f"{ed_fisica:02d}")
    
    pdf.text(x=164, y=72, txt='' + f"{castellanoFinal:02d}")
    pdf.text(x=164, y=78, txt='' + f"{matematicaFinal:02d}")
    pdf.text(x=164, y=84, txt='' + f"{GHCFinal:02d}")
    pdf.text(x=164, y=90, txt='' + f"{religionFinal:02d}")
    pdf.text(x=164, y=96, txt='' + f"{biologiaFinal:02d}")
    pdf.text(x=164, y=102, txt='' + f"{computacionFinal:02d}")
    pdf.text(x=164, y=108, txt='' + f"{inglesFinal:02d}")
    pdf.text(x=164, y=114, txt='' + f"{arteFinal:02d}")
    pdf.text(x=164, y=120, txt='' + f"{ed_fisicaFinal:02d}")
    
    pdf.text(x=187, y=72, txt='' + f"{promCastellano:02d}")
    pdf.text(x=187, y=78, txt='' + f"{promMatematica:02d}")
    pdf.text(x=187, y=84, txt='' + f"{promGHC:02d}")
    pdf.text(x=187, y=90, txt='' + f"{promReligion:02d}")
    pdf.text(x=187, y=96, txt='' + f"{promBiologia:02d}")
    pdf.text(x=187, y=102, txt='' + f"{promComputacion:02d}")
    pdf.text(x=187, y=108, txt='' + f"{promIngles:02d}")
    pdf.text(x=187, y=114, txt='' + f"{promArte:02d}")
    pdf.text(x=187, y=120, txt='' + f"{promEd_fisica:02d}")
    
    #Grafico, Observaciones, Sello y Firmas
    pdf.rect(x=10, y=146, w=142, h=50)
    pdf.rect(x=10, y=197, w=190, h=57)
    pdf.line(153, 146, 200, 146)
    pdf.line(153, 146, 153, 197)
    pdf.line(200, 146, 200, 197)
    pdf.line(10, 204, 200, 204)
    pdf.line(10, 238, 200, 238)
    pdf.line(73, 238, 73, 254)
    pdf.line(136, 238, 136, 254)
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=52, y=144, txt='GRÁFICO DEL PROGRESO ESCOLAR')
    pdf.text(x=60, y=202, txt='OBSERVACIONES SOBRE LA ACTUACIÓN DEL ESTUDIANTE')
    pdf.set_font('Arial', 'B', 8)
    pdf.text(x=163, y=172, txt='SELLO DEL PLANTEL')
    pdf.text(x=20, y=253, txt='DIRECTOR/A: YULEIDA ROJAS')
    pdf.text(x=85, y=253, txt='SUBDIRECTOR: ??????')
    pdf.text(x=144, y=253, txt='COORD. ACAD: CARMELO BOSCÁN')
    pdf.image('static/graficos/graficoIndividual3A.png', x=11, y=147, w=140, h=48)
    
    #Guardado y descarga
    pdf_path = os.path.join('pdfs', f'{nombre}-TercerLapso.pdf')
    pdf.output(pdf_path)
    cursor.close()
    return redirect(url_for('descargarPdf3A', nombre=nombre))

#--Seccion B--

#Ruta para generar reporte 1er Lapso B
@app.route('/reportLapso1B/<string:id>', methods=['GET', 'POST'])
def reportLapso1B(id):
    
    #Notas
    cursor = db.database.cursor()
    sqlNotas = "SELECT * FROM primer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlNotas, (id,))
    datos = cursor.fetchone()
    
    nombre = datos[1]
    cedula = datos[3]
    castellano = datos[4]
    matematica = datos[5]
    GHC = datos[6]
    religion = datos[7]
    biologia = datos[8]
    computacion = datos[9]
    ingles = datos[10]
    arte = datos[11]
    ed_fisica = datos[12]
    promedio = str(datos[13])
    
    #Promedios Seccion
    sqlPromCastellano = "SELECT Castellano FROM primer_lapso_b"
    cursor.execute(sqlPromCastellano)
    resCastellano = cursor.fetchall()
    rowCastellano = [row[0] for row in resCastellano]
    promCastellano = round(sum(rowCastellano) / len(rowCastellano))
    
    sqlPromMatematica = "SELECT Matematica FROM primer_lapso_b"
    cursor.execute(sqlPromMatematica)
    resMatematica = cursor.fetchall()
    rowMatematica = [row[0] for row in resMatematica]
    promMatematica = round(sum(rowMatematica) / len(rowMatematica))
    
    sqlPromGHC = "SELECT GHC FROM primer_lapso_b"
    cursor.execute(sqlPromGHC)
    resGHC = cursor.fetchall()
    rowGHC = [row[0] for row in resGHC]
    promGHC = round(sum(rowGHC) / len(rowGHC))
    
    sqlPromReligion = "SELECT Religion FROM primer_lapso_b"
    cursor.execute(sqlPromReligion)
    resReligion = cursor.fetchall()
    rowReligion = [row[0] for row in resReligion]
    promReligion = round(sum(rowReligion) / len(rowReligion))
    
    sqlPromBiologia = "SELECT Biologia FROM primer_lapso_b"
    cursor.execute(sqlPromBiologia)
    resBiologia = cursor.fetchall()
    rowBiologia = [row[0] for row in resBiologia]
    promBiologia = round(sum(rowBiologia) / len(rowBiologia))
    
    sqlPromComputacion = "SELECT Computacion FROM primer_lapso_b"
    cursor.execute(sqlPromComputacion)
    resComputacion = cursor.fetchall()
    rowComputacion = [row[0] for row in resComputacion]
    promComputacion = round(sum(rowComputacion) / len(rowComputacion))
    
    sqlPromIngles = "SELECT Ingles FROM primer_lapso_b"
    cursor.execute(sqlPromIngles)
    resIngles = cursor.fetchall()
    rowIngles = [row[0] for row in resIngles]
    promIngles = round(sum(rowIngles) / len(rowIngles))
    
    sqlPromArte = "SELECT Arte FROM primer_lapso_b"
    cursor.execute(sqlPromArte)
    resArte = cursor.fetchall()
    rowArte = [row[0] for row in resArte]
    promArte = round(sum(rowArte) / len(rowArte))
    
    sqlPromEd_fisica = "SELECT Educacion_fisica FROM primer_lapso_b"
    cursor.execute(sqlPromEd_fisica)
    resEd_fisica = cursor.fetchall()
    rowEd_fisica = [row[0] for row in resEd_fisica]
    promEd_fisica = round(sum(rowEd_fisica) / len(rowEd_fisica))
    
    #Promedio General Seccion
    promedioGeneralLapsoSeccion = str(round((promCastellano + promMatematica + promGHC + promReligion + promBiologia + promComputacion + promIngles + promArte + promEd_fisica) / 9 , 2))
    
    #Grafico
    bar_width = 0.35
    separacion = 0.5
    x = np.arange(9) * (bar_width * 2 + separacion)
    y1 = [castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica]
    y2 = [promCastellano, promMatematica, promGHC, promReligion, promBiologia, promComputacion, promIngles, promArte, promEd_fisica]

    fig, ax = plt.subplots(figsize=(6, 2))
    bar1 = ax.bar(x - bar_width/2, y1, bar_width, label='Nota', color='black')
    bar2 = ax.bar(x + bar_width/2, y2, bar_width, label='Prom. Sec.', color='gray')

    ax.set_ylabel('Notas')
    ax.set_xticks(x)
    ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig('static/graficos/graficoIndividual1B.png')
     
    #Fecha
    fecha = datetime.datetime.now()
    fechaBuena = fecha.strftime('%d/%m/%Y')
    
    #--PDF--
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    #Cuadro Datos colegio
    pdf.set_font('Arial', '', 12)
    pdf.rect(x=10, y=10, w=190, h=130)
    pdf.text(x=50, y=15, txt='Unidad Educativa')
    pdf.text(x=50, y=21, txt='Padre José Cueto')
    pdf.line(50, 23, 84, 23)
    pdf.text(x=53, y=28, txt='Código Plantel:')
    pdf.text(x=55, y=34, txt='PD04022317')
    pdf.line(50, 36, 84, 36)
    pdf.text(x=49, y=41, txt='RIF: J-31435772-7')
    pdf.line(50, 43, 84, 43)
    pdf.line(10, 46, 200, 46)
    pdf.line(88, 10, 88, 46)
    pdf.image('static/imagenes/cueto2.jpeg', x=17, y=13, w=25, h=30)
    
    #Cuadro datos estudiante
    pdf.set_font('Arial', 'B', 12)
    pdf.text(x=100, y=14, txt='' + nombre)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.text(x=130, y=19, txt='Educación Media')
    
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=105, y=24, txt='N° CÉDULA: ' + cedula)
    pdf.text(x=99, y=29, txt='AÑO / SECCIÓN: 1ero / "B"')
    pdf.text(x=92, y=34, txt='PERIODO ESCOLAR: 2020-2021')
    pdf.text(x=112, y=38, txt='LAPSO: Primero')
    pdf.text(x=91, y=43, txt='FECHA DE ENTREGA: ' + fechaBuena)
    
    #Titulo boletines
    pdf.set_font('Arial', 'B', 12)
    pdf.text(x=78, y=51, txt='BOLETÍN DE CALIFICACIONES')
    pdf.line(10, 53, 200, 53)

    #Contenido General
    pdf.line(10, 68, 200, 68)
    pdf.line(16, 68, 16, 134)
    pdf.line(10, 134, 200, 134)
    pdf.set_font('Arial', '', 11)
    pdf.text(x=11, y=72, txt='01')
    pdf.text(x=11, y=78, txt='02')
    pdf.text(x=11, y=84, txt='03')
    pdf.text(x=11, y=90, txt='04')
    pdf.text(x=11, y=96, txt='05')
    pdf.text(x=11, y=102, txt='06')
    pdf.text(x=11, y=108, txt='07')
    pdf.text(x=11, y=114, txt='08')
    pdf.text(x=11, y=120, txt='09')
    pdf.text(x=11, y=126, txt='10')
    pdf.text(x=11, y=132, txt='11')
    pdf.text(x=19, y=72, txt='Castellano')
    pdf.text(x=19, y=78, txt='Matemática')
    pdf.text(x=19, y=84, txt='GHC')
    pdf.text(x=19, y=90, txt='Religión')
    pdf.text(x=19, y=96, txt='Biología')
    pdf.text(x=19, y=102, txt='Computación')
    pdf.text(x=19, y=108, txt='Inglés')
    pdf.text(x=19, y=114, txt='Arte')
    pdf.text(x=19, y=120, txt='Educación Física')
    pdf.line(65, 53, 65, 140)
    pdf.line(104, 53, 104, 140)
    pdf.line(65, 60, 200, 60)
    pdf.line(152, 68, 152, 140)
    pdf.set_font('Arial', 'B', 11)
    pdf.text(x=24, y=62, txt='ASIGNATURAS')
    pdf.text(x=75, y=58, txt='1° LAPSO')
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=67, y=65, txt='DEFINITIVA DE LAPSO')
    pdf.set_font('Arial', '', 9)
    pdf.text(x=83, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=83, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=83, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=83, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=83, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=83, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=83, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=83, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=83, y=120, txt='' + f"{ed_fisica:02d}")
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=19, y=138, txt='Promedios Comparativos:')
    pdf.text(x=81, y=138, txt='' + promedio)
    pdf.text(x=108, y=138, txt='' + promedio)
    pdf.text(x=128, y=138, txt='--')
    pdf.text(x=144, y=138, txt='--')
    pdf.text(x=162, y=138, txt='' + promedio)
    pdf.text(x=185, y=138, txt='' + promedioGeneralLapsoSeccion)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=130, y=58, txt='RESUMEN DE EVALUACIÓN')
    
    pdf.set_font('Arial', '', 8)
    pdf.text(x=106, y=63, txt='PRIMER')
    pdf.text(x=107, y=67, txt='LAPSO')
    pdf.text(x=121, y=63, txt='SEGUNDO')
    pdf.text(x=123, y=67, txt='LAPSO')
    pdf.text(x=139, y=63, txt='TERCER')
    pdf.text(x=140, y=67, txt='LAPSO')
    pdf.text(x=162, y=63, txt='NOTA')
    pdf.text(x=158, y=67, txt='DEFINITIVA')
    pdf.text(x=185, y=63, txt='PROM.')
    pdf.text(x=186, y=67, txt='SEC.')
    
    pdf.set_font('Arial', '', 9)
    pdf.text(x=110, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=110, y=78, txt='' +  f"{matematica:02d}")
    pdf.text(x=110, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=110, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=110, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=110, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=110, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=110, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=110, y=120, txt='' + f"{ed_fisica:02d}")
    
    pdf.text(x=128, y=72, txt='-')
    pdf.text(x=128, y=78, txt='-')
    pdf.text(x=128, y=84, txt='-')
    pdf.text(x=128, y=90, txt='-')
    pdf.text(x=128, y=96, txt='-')
    pdf.text(x=128, y=102, txt='-')
    pdf.text(x=128, y=108, txt='-')
    pdf.text(x=128, y=114, txt='-')
    pdf.text(x=128, y=120, txt='-')
    
    pdf.text(x=145, y=72, txt='-')
    pdf.text(x=145, y=78, txt='-')
    pdf.text(x=145, y=84, txt='-')
    pdf.text(x=145, y=90, txt='-')
    pdf.text(x=145, y=96, txt='-')
    pdf.text(x=145, y=102, txt='-')
    pdf.text(x=145, y=108, txt='-')
    pdf.text(x=145, y=114, txt='-')
    pdf.text(x=145, y=120, txt='-')
    
    pdf.text(x=164, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=164, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=164, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=164, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=164, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=164, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=164, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=164, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=164, y=120, txt='' + f"{ed_fisica:02d}")
    
    pdf.text(x=187, y=72, txt='' + f"{promCastellano:02d}")
    pdf.text(x=187, y=78, txt='' + f"{promMatematica:02d}")
    pdf.text(x=187, y=84, txt='' + f"{promGHC:02d}")
    pdf.text(x=187, y=90, txt='' + f"{promReligion:02d}")
    pdf.text(x=187, y=96, txt='' + f"{promBiologia:02d}")
    pdf.text(x=187, y=102, txt='' + f"{promComputacion:02d}")
    pdf.text(x=187, y=108, txt='' + f"{promIngles:02d}")
    pdf.text(x=187, y=114, txt='' + f"{promArte:02d}")
    pdf.text(x=187, y=120, txt='' + f"{promEd_fisica:02d}")
    
    #Grafico, Observaciones, Sello y Firmas
    pdf.rect(x=10, y=146, w=142, h=50)
    pdf.rect(x=10, y=197, w=190, h=57)
    pdf.line(153, 146, 200, 146)
    pdf.line(153, 146, 153, 197)
    pdf.line(200, 146, 200, 197)
    pdf.line(10, 204, 200, 204)
    pdf.line(10, 238, 200, 238)
    pdf.line(73, 238, 73, 254)
    pdf.line(136, 238, 136, 254)
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=52, y=144, txt='GRÁFICO DEL PROGRESO ESCOLAR')
    pdf.text(x=60, y=202, txt='OBSERVACIONES SOBRE LA ACTUACIÓN DEL ESTUDIANTE')
    pdf.set_font('Arial', 'B', 8)
    pdf.text(x=163, y=172, txt='SELLO DEL PLANTEL')
    pdf.text(x=20, y=253, txt='DIRECTOR/A: YULEIDA ROJAS')
    pdf.text(x=85, y=253, txt='SUBDIRECTOR: ??????')
    pdf.text(x=144, y=253, txt='COORD. ACAD: CARMELO BOSCÁN')
    pdf.image('static/graficos/graficoIndividual1B.png', x=11, y=147, w=140, h=48)
    
    #Guardado y descarga
    pdf_path = os.path.join('pdfs', f'{nombre}-PrimerLapso.pdf')
    pdf.output(pdf_path)
    cursor.close()
    return redirect(url_for('descargarPdf1B', nombre=nombre))

#Ruta para generar reporte 2do Lapso B
@app.route('/reportLapso2B/<string:id>', methods=['GET', 'POST'])
def reportLapso2B(id):
    
    #Notas
    cursor = db.database.cursor()
    sqlNotas = "SELECT * FROM segundo_lapso_b WHERE Nro = %s"
    cursor.execute(sqlNotas, (id,))
    datos = cursor.fetchone()
    
    nombre = datos[1]
    cedula = datos[3]
    castellano = datos[4]
    matematica = datos[5]
    GHC = datos[6]
    religion = datos[7]
    biologia = datos[8]
    computacion = datos[9]
    ingles = datos[10]
    arte = datos[11]
    ed_fisica = datos[12]
    promedio = str(datos[13])
    
    #Promedios Seccion
    sqlPromCastellano = "SELECT Castellano FROM segundo_lapso_b"
    cursor.execute(sqlPromCastellano)
    resCastellano = cursor.fetchall()
    rowCastellano = [row[0] for row in resCastellano]
    promCastellano = round(sum(rowCastellano) / len(rowCastellano))
    
    sqlPromMatematica = "SELECT Matematica FROM segundo_lapso_b"
    cursor.execute(sqlPromMatematica)
    resMatematica = cursor.fetchall()
    rowMatematica = [row[0] for row in resMatematica]
    promMatematica = round(sum(rowMatematica) / len(rowMatematica))
    
    sqlPromGHC = "SELECT GHC FROM segundo_lapso_b"
    cursor.execute(sqlPromGHC)
    resGHC = cursor.fetchall()
    rowGHC = [row[0] for row in resGHC]
    promGHC = round(sum(rowGHC) / len(rowGHC))
    
    sqlPromReligion = "SELECT Religion FROM segundo_lapso_b"
    cursor.execute(sqlPromReligion)
    resReligion = cursor.fetchall()
    rowReligion = [row[0] for row in resReligion]
    promReligion = round(sum(rowReligion) / len(rowReligion))
    
    sqlPromBiologia = "SELECT Biologia FROM segundo_lapso_b"
    cursor.execute(sqlPromBiologia)
    resBiologia = cursor.fetchall()
    rowBiologia = [row[0] for row in resBiologia]
    promBiologia = round(sum(rowBiologia) / len(rowBiologia))
    
    sqlPromComputacion = "SELECT Computacion FROM segundo_lapso_b"
    cursor.execute(sqlPromComputacion)
    resComputacion = cursor.fetchall()
    rowComputacion = [row[0] for row in resComputacion]
    promComputacion = round(sum(rowComputacion) / len(rowComputacion))
    
    sqlPromIngles = "SELECT Ingles FROM segundo_lapso_b"
    cursor.execute(sqlPromIngles)
    resIngles = cursor.fetchall()
    rowIngles = [row[0] for row in resIngles]
    promIngles = round(sum(rowIngles) / len(rowIngles))
    
    sqlPromArte = "SELECT Arte FROM segundo_lapso_b"
    cursor.execute(sqlPromArte)
    resArte = cursor.fetchall()
    rowArte = [row[0] for row in resArte]
    promArte = round(sum(rowArte) / len(rowArte))
    
    sqlPromEd_fisica = "SELECT Educacion_fisica FROM segundo_lapso_b"
    cursor.execute(sqlPromEd_fisica)
    resEd_fisica = cursor.fetchall()
    rowEd_fisica = [row[0] for row in resEd_fisica]
    promEd_fisica = round(sum(rowEd_fisica) / len(rowEd_fisica))
    
    #Promedio General Seccion
    promedioGeneralLapsoSeccion = str(round((promCastellano + promMatematica + promGHC + promReligion + promBiologia + promComputacion + promIngles + promArte + promEd_fisica) / 9 , 2))
    
    #Grafico
    bar_width = 0.35
    separacion = 0.5
    x = np.arange(9) * (bar_width * 2 + separacion)
    y1 = [castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica]
    y2 = [promCastellano, promMatematica, promGHC, promReligion, promBiologia, promComputacion, promIngles, promArte, promEd_fisica]

    fig, ax = plt.subplots(figsize=(6, 2))
    bar1 = ax.bar(x - bar_width/2, y1, bar_width, label='Nota', color='black')
    bar2 = ax.bar(x + bar_width/2, y2, bar_width, label='Prom. Sec.', color='gray')

    ax.set_ylabel('Notas')
    ax.set_xticks(x)
    ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig('static/graficos/graficoIndividual2B.png')
     
    #Fecha
    fecha = datetime.datetime.now()
    fechaBuena = fecha.strftime('%d/%m/%Y')
    
    #--PDF--
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    #Cuadro Datos colegio
    pdf.set_font('Arial', '', 12)
    pdf.rect(x=10, y=10, w=190, h=130)
    pdf.text(x=50, y=15, txt='Unidad Educativa')
    pdf.text(x=50, y=21, txt='Padre José Cueto')
    pdf.line(50, 23, 84, 23)
    pdf.text(x=53, y=28, txt='Código Plantel:')
    pdf.text(x=55, y=34, txt='PD04022317')
    pdf.line(50, 36, 84, 36)
    pdf.text(x=49, y=41, txt='RIF: J-31435772-7')
    pdf.line(50, 43, 84, 43)
    pdf.line(10, 46, 200, 46)
    pdf.line(88, 10, 88, 46)
    pdf.image('static/imagenes/cueto2.jpeg', x=17, y=13, w=25, h=30)
    
    #Cuadro datos estudiante
    pdf.set_font('Arial', 'B', 12)
    pdf.text(x=100, y=14, txt='' + nombre)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.text(x=130, y=19, txt='Educación Media')
    
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=105, y=24, txt='N° CÉDULA: ' + cedula)
    pdf.text(x=99, y=29, txt='AÑO / SECCIÓN: 1ero / "B"')
    pdf.text(x=92, y=34, txt='PERIODO ESCOLAR: 2020-2021')
    pdf.text(x=112, y=38, txt='LAPSO: Segundo')
    pdf.text(x=91, y=43, txt='FECHA DE ENTREGA: ' + fechaBuena)
    
    #Titulo boletines
    pdf.set_font('Arial', 'B', 12)
    pdf.text(x=78, y=51, txt='BOLETÍN DE CALIFICACIONES')
    pdf.line(10, 53, 200, 53)

    #Contenido General
    pdf.line(10, 68, 200, 68)
    pdf.line(16, 68, 16, 134)
    pdf.line(10, 134, 200, 134)
    pdf.set_font('Arial', '', 11)
    pdf.text(x=11, y=72, txt='01')
    pdf.text(x=11, y=78, txt='02')
    pdf.text(x=11, y=84, txt='03')
    pdf.text(x=11, y=90, txt='04')
    pdf.text(x=11, y=96, txt='05')
    pdf.text(x=11, y=102, txt='06')
    pdf.text(x=11, y=108, txt='07')
    pdf.text(x=11, y=114, txt='08')
    pdf.text(x=11, y=120, txt='09')
    pdf.text(x=11, y=126, txt='10')
    pdf.text(x=11, y=132, txt='11')
    pdf.text(x=19, y=72, txt='Castellano')
    pdf.text(x=19, y=78, txt='Matemática')
    pdf.text(x=19, y=84, txt='GHC')
    pdf.text(x=19, y=90, txt='Religión')
    pdf.text(x=19, y=96, txt='Biología')
    pdf.text(x=19, y=102, txt='Computación')
    pdf.text(x=19, y=108, txt='Inglés')
    pdf.text(x=19, y=114, txt='Arte')
    pdf.text(x=19, y=120, txt='Educación Física')
    pdf.line(65, 53, 65, 140)
    pdf.line(104, 53, 104, 140)
    pdf.line(65, 60, 200, 60)
    pdf.line(152, 68, 152, 140)
    pdf.set_font('Arial', 'B', 11)
    pdf.text(x=24, y=62, txt='ASIGNATURAS')
    pdf.text(x=75, y=58, txt='2° LAPSO')
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=67, y=65, txt='DEFINITIVA DE LAPSO')
    pdf.set_font('Arial', '', 9)
    pdf.text(x=83, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=83, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=83, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=83, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=83, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=83, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=83, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=83, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=83, y=120, txt='' + f"{ed_fisica:02d}")
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=19, y=138, txt='Promedios Comparativos:')
    pdf.text(x=81, y=138, txt='' + promedio)
    pdf.text(x=108, y=138, txt='--')
    pdf.text(x=124, y=138, txt='' + promedio)
    pdf.text(x=144, y=138, txt='--')
    pdf.text(x=162, y=138, txt='' + promedio)
    pdf.text(x=185, y=138, txt='' + promedioGeneralLapsoSeccion)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=130, y=58, txt='RESUMEN DE EVALUACIÓN')
    
    pdf.set_font('Arial', '', 8)
    pdf.text(x=106, y=63, txt='PRIMER')
    pdf.text(x=107, y=67, txt='LAPSO')
    pdf.text(x=121, y=63, txt='SEGUNDO')
    pdf.text(x=123, y=67, txt='LAPSO')
    pdf.text(x=139, y=63, txt='TERCER')
    pdf.text(x=140, y=67, txt='LAPSO')
    pdf.text(x=162, y=63, txt='NOTA')
    pdf.text(x=158, y=67, txt='DEFINITIVA')
    pdf.text(x=185, y=63, txt='PROM.')
    pdf.text(x=186, y=67, txt='SEC.')
    
    pdf.set_font('Arial', '', 9)
    pdf.text(x=110, y=72, txt='-')
    pdf.text(x=110, y=78, txt='-')
    pdf.text(x=110, y=84, txt='-')
    pdf.text(x=110, y=90, txt='-')
    pdf.text(x=110, y=96, txt='-')
    pdf.text(x=110, y=102, txt='-')
    pdf.text(x=110, y=108, txt='-')
    pdf.text(x=110, y=114, txt='-')
    pdf.text(x=110, y=120, txt='-')
    
    pdf.text(x=126, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=126, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=126, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=126, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=126, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=126, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=126, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=126, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=126, y=120, txt='' + f"{ed_fisica:02d}")
    
    pdf.text(x=145, y=72, txt='-')
    pdf.text(x=145, y=78, txt='-')
    pdf.text(x=145, y=84, txt='-')
    pdf.text(x=145, y=90, txt='-')
    pdf.text(x=145, y=96, txt='-')
    pdf.text(x=145, y=102, txt='-')
    pdf.text(x=145, y=108, txt='-')
    pdf.text(x=145, y=114, txt='-')
    pdf.text(x=145, y=120, txt='-')
    
    pdf.text(x=164, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=164, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=164, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=164, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=164, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=164, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=164, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=164, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=164, y=120, txt='' + f"{ed_fisica:02d}")
    
    pdf.text(x=187, y=72, txt='' + f"{promCastellano:02d}")
    pdf.text(x=187, y=78, txt='' + f"{promMatematica:02d}")
    pdf.text(x=187, y=84, txt='' + f"{promGHC:02d}")
    pdf.text(x=187, y=90, txt='' + f"{promReligion:02d}")
    pdf.text(x=187, y=96, txt='' + f"{promBiologia:02d}")
    pdf.text(x=187, y=102, txt='' + f"{promComputacion:02d}")
    pdf.text(x=187, y=108, txt='' + f"{promIngles:02d}")
    pdf.text(x=187, y=114, txt='' + f"{promArte:02d}")
    pdf.text(x=187, y=120, txt='' + f"{promEd_fisica:02d}")
    
    #Grafico, Observaciones, Sello y Firmas
    pdf.rect(x=10, y=146, w=142, h=50)
    pdf.rect(x=10, y=197, w=190, h=57)
    pdf.line(153, 146, 200, 146)
    pdf.line(153, 146, 153, 197)
    pdf.line(200, 146, 200, 197)
    pdf.line(10, 204, 200, 204)
    pdf.line(10, 238, 200, 238)
    pdf.line(73, 238, 73, 254)
    pdf.line(136, 238, 136, 254)
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=52, y=144, txt='GRÁFICO DEL PROGRESO ESCOLAR')
    pdf.text(x=60, y=202, txt='OBSERVACIONES SOBRE LA ACTUACIÓN DEL ESTUDIANTE')
    pdf.set_font('Arial', 'B', 8)
    pdf.text(x=163, y=172, txt='SELLO DEL PLANTEL')
    pdf.text(x=20, y=253, txt='DIRECTOR/A: YULEIDA ROJAS')
    pdf.text(x=85, y=253, txt='SUBDIRECTOR: ??????')
    pdf.text(x=144, y=253, txt='COORD. ACAD: CARMELO BOSCÁN')
    pdf.image('static/graficos/graficoIndividual2B.png', x=11, y=147, w=140, h=48)
    
    #Guardado y descarga
    pdf_path = os.path.join('pdfs', f'{nombre}-SegundoLapso.pdf')
    pdf.output(pdf_path)
    cursor.close()
    return redirect(url_for('descargarPdf2B', nombre=nombre))

#Ruta para generar reporte 3er Lapso B
@app.route('/reportLapso3B/<string:id>', methods=['GET', 'POST'])
def reportLapso3B(id):
    
    #Notas 3er Lapso
    cursor = db.database.cursor()
    sqlNotas = "SELECT * FROM tercer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlNotas, (id,))
    datos = cursor.fetchone()
    
    nombre = datos[1]
    cedula = datos[3]
    castellano = datos[4]
    matematica = datos[5]
    GHC = datos[6]
    religion = datos[7]
    biologia = datos[8]
    computacion = datos[9]
    ingles = datos[10]
    arte = datos[11]
    ed_fisica = datos[12]
    promedio = str(datos[13])
    
    #Notas 1er Lapso
    sqlNotas1erLapso = "SELECT * FROM primer_lapso_b WHERE Nro = %s"
    cursor.execute(sqlNotas1erLapso, (id,))
    datosLapso1 = cursor.fetchone()
    
    castellanoLapso1 = datosLapso1[4]
    matematicaLapso1 = datosLapso1[5]
    GHCLapso1 = datosLapso1[6]
    religionLapso1 = datosLapso1[7]
    biologiaLapso1 = datosLapso1[8]
    computacionLapso1 = datosLapso1[9]
    inglesLapso1 = datosLapso1[10]
    arteLapso1 = datosLapso1[11]
    ed_fisicaLapso1 = datosLapso1[12]
    promedioLapso1 = str(datosLapso1[13])
    
    #Notas 2do Lapso
    sqlNotas2doLapso = "SELECT * FROM segundo_lapso_b WHERE Nro = %s"
    cursor.execute(sqlNotas2doLapso, (id,))
    datosLapso2 = cursor.fetchone()
    
    castellanoLapso2 = datosLapso2[4]
    matematicaLapso2 = datosLapso2[5]
    GHCLapso2 = datosLapso2[6]
    religionLapso2 = datosLapso2[7]
    biologiaLapso2 = datosLapso2[8]
    computacionLapso2 = datosLapso2[9]
    inglesLapso2 = datosLapso2[10]
    arteLapso2 = datosLapso2[11]
    ed_fisicaLapso2 = datosLapso2[12]
    promedioLapso2 = str(datosLapso2[13])
    
    #Notas Definitivas y Promedio Final de Año
    sqlNotasFinales = "SELECT * FROM seccion_b WHERE Nro = %s"
    cursor.execute(sqlNotasFinales, (id,))
    datosFinales = cursor.fetchone()
    
    castellanoFinal = datosFinales[4]
    matematicaFinal = datosFinales[5]
    GHCFinal = datosFinales[6]
    religionFinal = datosFinales[7]
    biologiaFinal = datosFinales[8]
    computacionFinal = datosFinales[9]
    inglesFinal = datosFinales[10]
    arteFinal = datosFinales[11]
    ed_fisicaFinal = datosFinales[12]
    promedioFinal = str(datosFinales[13])
    
    #Promedios Seccion
    sqlPromCastellano = "SELECT Castellano FROM tercer_lapso_b"
    cursor.execute(sqlPromCastellano)
    resCastellano = cursor.fetchall()
    rowCastellano = [row[0] for row in resCastellano]
    promCastellano = round(sum(rowCastellano) / len(rowCastellano))
    
    sqlPromMatematica = "SELECT Matematica FROM tercer_lapso_b"
    cursor.execute(sqlPromMatematica)
    resMatematica = cursor.fetchall()
    rowMatematica = [row[0] for row in resMatematica]
    promMatematica = round(sum(rowMatematica) / len(rowMatematica))
    
    sqlPromGHC = "SELECT GHC FROM tercer_lapso_b"
    cursor.execute(sqlPromGHC)
    resGHC = cursor.fetchall()
    rowGHC = [row[0] for row in resGHC]
    promGHC = round(sum(rowGHC) / len(rowGHC))
    
    sqlPromReligion = "SELECT Religion FROM tercer_lapso_b"
    cursor.execute(sqlPromReligion)
    resReligion = cursor.fetchall()
    rowReligion = [row[0] for row in resReligion]
    promReligion = round(sum(rowReligion) / len(rowReligion))
    
    sqlPromBiologia = "SELECT Biologia FROM tercer_lapso_b"
    cursor.execute(sqlPromBiologia)
    resBiologia = cursor.fetchall()
    rowBiologia = [row[0] for row in resBiologia]
    promBiologia = round(sum(rowBiologia) / len(rowBiologia))
    
    sqlPromComputacion = "SELECT Computacion FROM tercer_lapso_b"
    cursor.execute(sqlPromComputacion)
    resComputacion = cursor.fetchall()
    rowComputacion = [row[0] for row in resComputacion]
    promComputacion = round(sum(rowComputacion) / len(rowComputacion))
    
    sqlPromIngles = "SELECT Ingles FROM tercer_lapso_b"
    cursor.execute(sqlPromIngles)
    resIngles = cursor.fetchall()
    rowIngles = [row[0] for row in resIngles]
    promIngles = round(sum(rowIngles) / len(rowIngles))
    
    sqlPromArte = "SELECT Arte FROM tercer_lapso_b"
    cursor.execute(sqlPromArte)
    resArte = cursor.fetchall()
    rowArte = [row[0] for row in resArte]
    promArte = round(sum(rowArte) / len(rowArte))
    
    sqlPromEd_fisica = "SELECT Educacion_fisica FROM tercer_lapso_b"
    cursor.execute(sqlPromEd_fisica)
    resEd_fisica = cursor.fetchall()
    rowEd_fisica = [row[0] for row in resEd_fisica]
    promEd_fisica = round(sum(rowEd_fisica) / len(rowEd_fisica))
    
    #Promedio General Seccion
    promedioGeneralLapsoSeccion = str(round((promCastellano + promMatematica + promGHC + promReligion + promBiologia + promComputacion + promIngles + promArte + promEd_fisica) / 9 , 2))
    
    #Grafico
    bar_width = 0.35
    separacion = 0.5
    x = np.arange(9) * (bar_width * 2 + separacion)
    y1 = [castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica]
    y2 = [promCastellano, promMatematica, promGHC, promReligion, promBiologia, promComputacion, promIngles, promArte, promEd_fisica]

    fig, ax = plt.subplots(figsize=(6, 2))
    bar1 = ax.bar(x - bar_width/2, y1, bar_width, label='Nota', color='black')
    bar2 = ax.bar(x + bar_width/2, y2, bar_width, label='Prom. Sec.', color='gray')

    ax.set_ylabel('Notas')
    ax.set_xticks(x)
    ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig('static/graficos/graficoIndividual3B.png')
     
    #Fecha
    fecha = datetime.datetime.now()
    fechaBuena = fecha.strftime('%d/%m/%Y')
    
    #--PDF--
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    #Cuadro Datos colegio
    pdf.set_font('Arial', '', 12)
    pdf.rect(x=10, y=10, w=190, h=130)
    pdf.text(x=50, y=15, txt='Unidad Educativa')
    pdf.text(x=50, y=21, txt='Padre José Cueto')
    pdf.line(50, 23, 84, 23)
    pdf.text(x=53, y=28, txt='Código Plantel:')
    pdf.text(x=55, y=34, txt='PD04022317')
    pdf.line(50, 36, 84, 36)
    pdf.text(x=49, y=41, txt='RIF: J-31435772-7')
    pdf.line(50, 43, 84, 43)
    pdf.line(10, 46, 200, 46)
    pdf.line(88, 10, 88, 46)
    pdf.image('static/imagenes/cueto2.jpeg', x=17, y=13, w=25, h=30)
    
    #Cuadro datos estudiante
    pdf.set_font('Arial', 'B', 12)
    pdf.text(x=100, y=14, txt='' + nombre)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.text(x=130, y=19, txt='Educación Media')
    
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=105, y=24, txt='N° CÉDULA: ' + cedula)
    pdf.text(x=99, y=29, txt='AÑO / SECCIÓN: 1ero / "B"')
    pdf.text(x=92, y=34, txt='PERIODO ESCOLAR: 2020-2021')
    pdf.text(x=112, y=38, txt='LAPSO: Tercero')
    pdf.text(x=91, y=43, txt='FECHA DE ENTREGA: ' + fechaBuena)
    
    #Titulo boletines
    pdf.set_font('Arial', 'B', 12)
    pdf.text(x=78, y=51, txt='BOLETÍN DE CALIFICACIONES')
    pdf.line(10, 53, 200, 53)

    #Contenido General
    pdf.line(10, 68, 200, 68)
    pdf.line(16, 68, 16, 134)
    pdf.line(10, 134, 200, 134)
    pdf.set_font('Arial', '', 11)
    pdf.text(x=11, y=72, txt='01')
    pdf.text(x=11, y=78, txt='02')
    pdf.text(x=11, y=84, txt='03')
    pdf.text(x=11, y=90, txt='04')
    pdf.text(x=11, y=96, txt='05')
    pdf.text(x=11, y=102, txt='06')
    pdf.text(x=11, y=108, txt='07')
    pdf.text(x=11, y=114, txt='08')
    pdf.text(x=11, y=120, txt='09')
    pdf.text(x=11, y=126, txt='10')
    pdf.text(x=11, y=132, txt='11')
    pdf.text(x=19, y=72, txt='Castellano')
    pdf.text(x=19, y=78, txt='Matemática')
    pdf.text(x=19, y=84, txt='GHC')
    pdf.text(x=19, y=90, txt='Religión')
    pdf.text(x=19, y=96, txt='Biología')
    pdf.text(x=19, y=102, txt='Computación')
    pdf.text(x=19, y=108, txt='Inglés')
    pdf.text(x=19, y=114, txt='Arte')
    pdf.text(x=19, y=120, txt='Educación Física')
    pdf.line(65, 53, 65, 140)
    pdf.line(104, 53, 104, 140)
    pdf.line(65, 60, 200, 60)
    pdf.line(152, 68, 152, 140)
    pdf.set_font('Arial', 'B', 11)
    pdf.text(x=24, y=62, txt='ASIGNATURAS')
    pdf.text(x=75, y=58, txt='3° LAPSO')
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=67, y=65, txt='DEFINITIVA DE LAPSO')
    pdf.set_font('Arial', '', 9)
    pdf.text(x=83, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=83, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=83, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=83, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=83, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=83, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=83, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=83, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=83, y=120, txt='' + f"{ed_fisica:02d}")
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=19, y=138, txt='Promedios Comparativos:')
    pdf.text(x=81, y=138, txt='' + promedio)
    pdf.text(x=108, y=138, txt='' + promedioLapso1)
    pdf.text(x=125, y=138, txt='' + promedioLapso2)
    pdf.text(x=141, y=138, txt='' + promedio)
    pdf.text(x=162, y=138, txt='' + promedioFinal)
    pdf.text(x=185, y=138, txt='' + promedioGeneralLapsoSeccion)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=130, y=58, txt='RESUMEN DE EVALUACIÓN')
    
    pdf.set_font('Arial', '', 8)
    pdf.text(x=106, y=63, txt='PRIMER')
    pdf.text(x=107, y=67, txt='LAPSO')
    pdf.text(x=121, y=63, txt='SEGUNDO')
    pdf.text(x=123, y=67, txt='LAPSO')
    pdf.text(x=139, y=63, txt='TERCER')
    pdf.text(x=140, y=67, txt='LAPSO')
    pdf.text(x=162, y=63, txt='NOTA')
    pdf.text(x=158, y=67, txt='DEFINITIVA')
    pdf.text(x=185, y=63, txt='PROM.')
    pdf.text(x=186, y=67, txt='SEC.')
    
    pdf.set_font('Arial', '', 9)
    pdf.text(x=110, y=72, txt='' + f"{castellanoLapso1:02d}")
    pdf.text(x=110, y=78, txt='' + f"{matematicaLapso1:02d}")
    pdf.text(x=110, y=84, txt='' + f"{GHCLapso1:02d}")
    pdf.text(x=110, y=90, txt='' + f"{religionLapso1:02d}")
    pdf.text(x=110, y=96, txt='' + f"{biologiaLapso1:02d}")
    pdf.text(x=110, y=102, txt='' + f"{computacionLapso1:02d}")
    pdf.text(x=110, y=108, txt='' + f"{inglesLapso1:02d}")
    pdf.text(x=110, y=114, txt='' + f"{arteLapso1:02d}")
    pdf.text(x=110, y=120, txt='' + f"{ed_fisicaLapso1:02d}")
    
    pdf.text(x=127, y=72, txt='' + f"{castellanoLapso2:02d}")
    pdf.text(x=127, y=78, txt='' + f"{matematicaLapso2:02d}")
    pdf.text(x=127, y=84, txt='' + f"{GHCLapso2:02d}")
    pdf.text(x=127, y=90, txt='' + f"{religionLapso2:02d}")
    pdf.text(x=127, y=96, txt='' + f"{biologiaLapso2:02d}")
    pdf.text(x=127, y=102, txt='' + f"{computacionLapso2:02d}")
    pdf.text(x=127, y=108, txt='' + f"{inglesLapso2:02d}")
    pdf.text(x=127, y=114, txt='' + f"{arteLapso2:02d}")
    pdf.text(x=127, y=120, txt='' + f"{ed_fisicaLapso2:02d}")
    
    pdf.text(x=143, y=72, txt='' + f"{castellano:02d}")
    pdf.text(x=143, y=78, txt='' + f"{matematica:02d}")
    pdf.text(x=143, y=84, txt='' + f"{GHC:02d}")
    pdf.text(x=143, y=90, txt='' + f"{religion:02d}")
    pdf.text(x=143, y=96, txt='' + f"{biologia:02d}")
    pdf.text(x=143, y=102, txt='' + f"{computacion:02d}")
    pdf.text(x=143, y=108, txt='' + f"{ingles:02d}")
    pdf.text(x=143, y=114, txt='' + f"{arte:02d}")
    pdf.text(x=143, y=120, txt='' + f"{ed_fisica:02d}")
    
    pdf.text(x=164, y=72, txt='' + f"{castellanoFinal:02d}")
    pdf.text(x=164, y=78, txt='' + f"{matematicaFinal:02d}")
    pdf.text(x=164, y=84, txt='' + f"{GHCFinal:02d}")
    pdf.text(x=164, y=90, txt='' + f"{religionFinal:02d}")
    pdf.text(x=164, y=96, txt='' + f"{biologiaFinal:02d}")
    pdf.text(x=164, y=102, txt='' + f"{computacionFinal:02d}")
    pdf.text(x=164, y=108, txt='' + f"{inglesFinal:02d}")
    pdf.text(x=164, y=114, txt='' + f"{arteFinal:02d}")
    pdf.text(x=164, y=120, txt='' + f"{ed_fisicaFinal:02d}")
    
    pdf.text(x=187, y=72, txt='' + f"{promCastellano:02d}")
    pdf.text(x=187, y=78, txt='' + f"{promMatematica:02d}")
    pdf.text(x=187, y=84, txt='' + f"{promGHC:02d}")
    pdf.text(x=187, y=90, txt='' + f"{promReligion:02d}")
    pdf.text(x=187, y=96, txt='' + f"{promBiologia:02d}")
    pdf.text(x=187, y=102, txt='' + f"{promComputacion:02d}")
    pdf.text(x=187, y=108, txt='' + f"{promIngles:02d}")
    pdf.text(x=187, y=114, txt='' + f"{promArte:02d}")
    pdf.text(x=187, y=120, txt='' + f"{promEd_fisica:02d}")
    
    #Grafico, Observaciones, Sello y Firmas
    pdf.rect(x=10, y=146, w=142, h=50)
    pdf.rect(x=10, y=197, w=190, h=57)
    pdf.line(153, 146, 200, 146)
    pdf.line(153, 146, 153, 197)
    pdf.line(200, 146, 200, 197)
    pdf.line(10, 204, 200, 204)
    pdf.line(10, 238, 200, 238)
    pdf.line(73, 238, 73, 254)
    pdf.line(136, 238, 136, 254)
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=52, y=144, txt='GRÁFICO DEL PROGRESO ESCOLAR')
    pdf.text(x=60, y=202, txt='OBSERVACIONES SOBRE LA ACTUACIÓN DEL ESTUDIANTE')
    pdf.set_font('Arial', 'B', 8)
    pdf.text(x=163, y=172, txt='SELLO DEL PLANTEL')
    pdf.text(x=20, y=253, txt='DIRECTOR/A: YULEIDA ROJAS')
    pdf.text(x=85, y=253, txt='SUBDIRECTOR: ??????')
    pdf.text(x=144, y=253, txt='COORD. ACAD: CARMELO BOSCÁN')
    pdf.image('static/graficos/graficoIndividual3B.png', x=11, y=147, w=140, h=48)
    
    #Guardado y descarga
    pdf_path = os.path.join('pdfs', f'{nombre}-TercerLapso.pdf')
    pdf.output(pdf_path)
    cursor.close()
    return redirect(url_for('descargarPdf3B', nombre=nombre))

#--Ruta de creacion de pack de pdfs--

#-1A-
@app.route('/construirPdf1A', methods=['POST'])
def packPdf1A():
    
    cursor = db.database.cursor()
    sqlNotas = "SELECT Nombre_completo, Cedula, Castellano, Matematica, GHC, Religion, Biologia, Computacion, Ingles, Arte, Educacion_fisica, Promedio FROM primer_lapso_a"
    cursor.execute(sqlNotas)
    estudiantes = cursor.fetchall()
    estudiantes_json = json.dumps(estudiantes, cls=DecimalEncoder)
    
    estudiantesJson = json.loads(estudiantes_json)
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for i, estudiante in enumerate(estudiantesJson):
        
        cursor = db.database.cursor()
        
        pdf.add_page()
                
        nombre, cedula, castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica, promedio = estudiante
        
        #Promedios Seccion
        sqlPromCastellano = "SELECT Castellano FROM primer_lapso_a"
        cursor.execute(sqlPromCastellano)
        resCastellano = cursor.fetchall()
        rowCastellano = [row[0] for row in resCastellano]
        promCastellano = round(sum(rowCastellano) / len(rowCastellano))
        
        sqlPromMatematica = "SELECT Matematica FROM primer_lapso_a"
        cursor.execute(sqlPromMatematica)
        resMatematica = cursor.fetchall()
        rowMatematica = [row[0] for row in resMatematica]
        promMatematica = round(sum(rowMatematica) / len(rowMatematica))
        
        sqlPromGHC = "SELECT GHC FROM primer_lapso_a"
        cursor.execute(sqlPromGHC)
        resGHC = cursor.fetchall()
        rowGHC = [row[0] for row in resGHC]
        promGHC = round(sum(rowGHC) / len(rowGHC))
        
        sqlPromReligion = "SELECT Religion FROM primer_lapso_a"
        cursor.execute(sqlPromReligion)
        resReligion = cursor.fetchall()
        rowReligion = [row[0] for row in resReligion]
        promReligion = round(sum(rowReligion) / len(rowReligion))
        
        sqlPromBiologia = "SELECT Biologia FROM primer_lapso_a"
        cursor.execute(sqlPromBiologia)
        resBiologia = cursor.fetchall()
        rowBiologia = [row[0] for row in resBiologia]
        promBiologia = round(sum(rowBiologia) / len(rowBiologia))
        
        sqlPromComputacion = "SELECT Computacion FROM primer_lapso_a"
        cursor.execute(sqlPromComputacion)
        resComputacion = cursor.fetchall()
        rowComputacion = [row[0] for row in resComputacion]
        promComputacion = round(sum(rowComputacion) / len(rowComputacion))
        
        sqlPromIngles = "SELECT Ingles FROM primer_lapso_a"
        cursor.execute(sqlPromIngles)
        resIngles = cursor.fetchall()
        rowIngles = [row[0] for row in resIngles]
        promIngles = round(sum(rowIngles) / len(rowIngles))
        
        sqlPromArte = "SELECT Arte FROM primer_lapso_a"
        cursor.execute(sqlPromArte)
        resArte = cursor.fetchall()
        rowArte = [row[0] for row in resArte]
        promArte = round(sum(rowArte) / len(rowArte))
        
        sqlPromEd_fisica = "SELECT Educacion_fisica FROM primer_lapso_a"
        cursor.execute(sqlPromEd_fisica)
        resEd_fisica = cursor.fetchall()
        rowEd_fisica = [row[0] for row in resEd_fisica]
        promEd_fisica = round(sum(rowEd_fisica) / len(rowEd_fisica))
        
        #Promedio General Seccion
        promedioGeneralLapsoSeccion = str(round((promCastellano + promMatematica + promGHC + promReligion + promBiologia + promComputacion + promIngles + promArte + promEd_fisica) / 9 , 2))
        
        #Grafico
        bar_width = 0.35
        separacion = 0.5
        x = np.arange(9) * (bar_width * 2 + separacion)
        y1 = [castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica]
        y2 = [promCastellano, promMatematica, promGHC, promReligion, promBiologia, promComputacion, promIngles, promArte, promEd_fisica]

        fig, ax = plt.subplots(figsize=(6, 2))
        bar1 = ax.bar(x - bar_width/2, y1, bar_width, label='Nota', color='black')
        bar2 = ax.bar(x + bar_width/2, y2, bar_width, label='Prom. Sec.', color='gray')

        ax.set_ylabel('Notas')
        ax.set_xticks(x)
        ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(f'static/graficos/grafico{i}.png')
        
        #Fecha
        fecha = datetime.datetime.now()
        fechaBuena = fecha.strftime('%d/%m/%Y')
        
        #--PDF--
        
        #Cuadro Datos colegio
        pdf.set_font('Arial', '', 12)
        pdf.rect(x=10, y=10, w=190, h=130)
        pdf.text(x=50, y=15, txt='Unidad Educativa')
        pdf.text(x=50, y=21, txt='Padre José Cueto')
        pdf.line(50, 23, 84, 23)
        pdf.text(x=53, y=28, txt='Código Plantel:')
        pdf.text(x=55, y=34, txt='PD04022317')
        pdf.line(50, 36, 84, 36)
        pdf.text(x=49, y=41, txt='RIF: J-31435772-7')
        pdf.line(50, 43, 84, 43)
        pdf.line(10, 46, 200, 46)
        pdf.line(88, 10, 88, 46)
        pdf.image('static/imagenes/cueto2.jpeg', x=17, y=13, w=25, h=30)
        
        #Cuadro datos estudiante
        pdf.set_font('Arial', 'B', 12)
        pdf.text(x=100, y=14, txt='' + nombre)
        
        pdf.set_font('Arial', 'B', 10)
        pdf.text(x=130, y=19, txt='Educación Media')
        
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=105, y=24, txt='N° CÉDULA: ' + cedula)
        pdf.text(x=99, y=29, txt='AÑO / SECCIÓN: 1ero / "A"')
        pdf.text(x=92, y=34, txt='PERIODO ESCOLAR: 2020-2021')
        pdf.text(x=107, y=38, txt='MOMENTO: Primero')
        pdf.text(x=91, y=43, txt='FECHA DE ENTREGA: ' + fechaBuena)
        
        #Titulo boletines
        pdf.set_font('Arial', 'B', 12)
        pdf.text(x=78, y=51, txt='BOLETÍN DE CALIFICACIONES')
        pdf.line(10, 53, 200, 53)

        #Contenido General
        pdf.line(10, 68, 200, 68)
        pdf.line(16, 68, 16, 134)
        pdf.line(10, 134, 200, 134)
        pdf.set_font('Arial', '', 11)
        pdf.text(x=11, y=72, txt='01')
        pdf.text(x=11, y=78, txt='02')
        pdf.text(x=11, y=84, txt='03')
        pdf.text(x=11, y=90, txt='04')
        pdf.text(x=11, y=96, txt='05')
        pdf.text(x=11, y=102, txt='06')
        pdf.text(x=11, y=108, txt='07')
        pdf.text(x=11, y=114, txt='08')
        pdf.text(x=11, y=120, txt='09')
        pdf.text(x=11, y=126, txt='10')
        pdf.text(x=11, y=132, txt='11')
        pdf.text(x=19, y=72, txt='Castellano')
        pdf.text(x=19, y=78, txt='Matemática')
        pdf.text(x=19, y=84, txt='GHC')
        pdf.text(x=19, y=90, txt='Religión')
        pdf.text(x=19, y=96, txt='Biología')
        pdf.text(x=19, y=102, txt='Computación')
        pdf.text(x=19, y=108, txt='Inglés')
        pdf.text(x=19, y=114, txt='Arte')
        pdf.text(x=19, y=120, txt='Educación Física')
        pdf.line(65, 53, 65, 140)
        pdf.line(104, 53, 104, 140)
        pdf.line(65, 60, 200, 60)
        pdf.line(152, 68, 152, 140)
        pdf.set_font('Arial', 'B', 11)
        pdf.text(x=24, y=62, txt='ASIGNATURAS')
        pdf.text(x=72, y=58, txt='1° MOMENTO')
        pdf.set_font('Arial', 'B', 8)
        pdf.text(x=67, y=65, txt='DEFINITIVA DE MOMENTO')
        pdf.set_font('Arial', '', 9)
        pdf.text(x=83, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=83, y=78, txt='' + f"{matematica:02d}")
        pdf.text(x=83, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=83, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=83, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=83, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=83, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=83, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=83, y=120, txt='' + f"{ed_fisica:02d}")
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=19, y=138, txt='Promedios Comparativos:')
        pdf.text(x=81, y=138, txt='' + f"{promedio}")
        pdf.text(x=108, y=138, txt='' + f"{promedio}")
        pdf.text(x=128, y=138, txt='--')
        pdf.text(x=144, y=138, txt='--')
        pdf.text(x=162, y=138, txt='' + f"{promedio}")
        pdf.text(x=185, y=138, txt='' + promedioGeneralLapsoSeccion)
        
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=130, y=58, txt='RESUMEN DE EVALUACIÓN')
        
        pdf.set_font('Arial', '', 8)
        pdf.text(x=106, y=63, txt='PRIMER')
        pdf.text(x=105, y=67, txt='MOMENTO')
        pdf.text(x=121, y=63, txt='SEGUNDO')
        pdf.text(x=121, y=67, txt='MOMENTO')
        pdf.text(x=139, y=63, txt='TERCER')
        pdf.text(x=138, y=67, txt='MOMENTO')
        pdf.text(x=162, y=63, txt='NOTA')
        pdf.text(x=158, y=67, txt='DEFINITIVA')
        pdf.text(x=185, y=63, txt='PROM.')
        pdf.text(x=186, y=67, txt='SEC.')
        
        pdf.set_font('Arial', '', 9)
        pdf.text(x=110, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=110, y=78, txt='' +  f"{matematica:02d}")
        pdf.text(x=110, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=110, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=110, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=110, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=110, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=110, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=110, y=120, txt='' + f"{ed_fisica:02d}")
        
        pdf.text(x=128, y=72, txt='-')
        pdf.text(x=128, y=78, txt='-')
        pdf.text(x=128, y=84, txt='-')
        pdf.text(x=128, y=90, txt='-')
        pdf.text(x=128, y=96, txt='-')
        pdf.text(x=128, y=102, txt='-')
        pdf.text(x=128, y=108, txt='-')
        pdf.text(x=128, y=114, txt='-')
        pdf.text(x=128, y=120, txt='-')
        
        pdf.text(x=145, y=72, txt='-')
        pdf.text(x=145, y=78, txt='-')
        pdf.text(x=145, y=84, txt='-')
        pdf.text(x=145, y=90, txt='-')
        pdf.text(x=145, y=96, txt='-')
        pdf.text(x=145, y=102, txt='-')
        pdf.text(x=145, y=108, txt='-')
        pdf.text(x=145, y=114, txt='-')
        pdf.text(x=145, y=120, txt='-')
        
        pdf.text(x=164, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=164, y=78, txt='' + f"{matematica:02d}")
        pdf.text(x=164, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=164, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=164, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=164, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=164, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=164, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=164, y=120, txt='' + f"{ed_fisica:02d}")
        
        pdf.text(x=187, y=72, txt='' + f"{promCastellano:02d}")
        pdf.text(x=187, y=78, txt='' + f"{promMatematica:02d}")
        pdf.text(x=187, y=84, txt='' + f"{promGHC:02d}")
        pdf.text(x=187, y=90, txt='' + f"{promReligion:02d}")
        pdf.text(x=187, y=96, txt='' + f"{promBiologia:02d}")
        pdf.text(x=187, y=102, txt='' + f"{promComputacion:02d}")
        pdf.text(x=187, y=108, txt='' + f"{promIngles:02d}")
        pdf.text(x=187, y=114, txt='' + f"{promArte:02d}")
        pdf.text(x=187, y=120, txt='' + f"{promEd_fisica:02d}")
        
        #Grafico, Observaciones, Sello y Firmas
        pdf.rect(x=10, y=146, w=142, h=50)
        pdf.rect(x=10, y=197, w=190, h=57)
        pdf.line(153, 146, 200, 146)
        pdf.line(153, 146, 153, 197)
        pdf.line(200, 146, 200, 197)
        pdf.line(10, 204, 200, 204)
        pdf.line(10, 238, 200, 238)
        pdf.line(73, 238, 73, 254)
        pdf.line(136, 238, 136, 254)
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=52, y=144, txt='GRÁFICO DEL PROGRESO ESCOLAR')
        pdf.text(x=60, y=202, txt='OBSERVACIONES SOBRE LA ACTUACIÓN DEL ESTUDIANTE')
        pdf.set_font('Arial', 'B', 8)
        pdf.text(x=163, y=172, txt='SELLO DEL PLANTEL')
        pdf.text(x=20, y=253, txt='DIRECTOR/A: YULEIDA ROJAS')
        pdf.text(x=85, y=253, txt='SUBDIRECTOR: ??????')
        pdf.text(x=144, y=253, txt='COORD. ACAD: CARMELO BOSCÁN')
        pdf.image(f'static/graficos/grafico{i}.png', x=11, y=147, w=140, h=48)
        
        pdf.text(x=105, y=280, txt='' + f"{pdf.page_no()}")
        
        cursor.close()
        
    pdf_path = os.path.join('pdfs', 'ReporteGeneral-1erMomentoA.pdf')
    pdf.output(pdf_path)
    return redirect(url_for('descargarPdfPack1A'))

#-2A-
@app.route('/construirPdf2A', methods=['POST'])
def packPdf2A():
    
    cursor = db.database.cursor()
    
    sqlNotasCombinadas = """
    SELECT
        s.Nombre_completo,
        s.Cedula,
        s.Castellano AS CastellanoSegundo,
        s.Matematica AS MatematicaSegundo,
        s.GHC AS GHCSegundo,
        s.Religion AS ReligionSegundo,
        s.Biologia AS BiologiaSegundo,
        s.Computacion AS ComputacionSegundo,
        s.Ingles AS InglesSegundo,
        s.Arte AS ArteSegundo,
        s.Educacion_fisica AS Educacion_fisicaSegundo,
        s.Promedio AS PromedioSegundo,
        p.Castellano AS CastellanoPrimer,
        p.Matematica AS MatematicaPrimer,
        p.GHC AS GHCPrimer,
        p.Religion AS ReligionPrimer,
        p.Biologia AS BiologiaPrimer,
        p.Computacion AS ComputacionPrimer,
        p.Ingles AS InglesPrimer,
        p.Arte AS ArtePrimer,
        p.Educacion_fisica AS Educacion_fisicaPrimer,
        p.Promedio AS PromedioPrimer
    FROM
        segundo_lapso_a s
    LEFT JOIN
        primer_lapso_a p ON s.Cedula = p.Cedula;
    """

    cursor.execute(sqlNotasCombinadas)
    estudiantesCombinados = cursor.fetchall()
    estudiantesCombinados_json = json.dumps(estudiantesCombinados, cls=DecimalEncoder)

    estudiantesCombinadosJson = json.loads(estudiantesCombinados_json)
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for i, estudiante in enumerate(estudiantesCombinadosJson):
        
        #2do Lapso
        nombre = estudiante[0]
        cedula = estudiante[1]
        castellano = estudiante[2]
        matematica = estudiante[3]
        GHC = estudiante[4]
        religion = estudiante[5]
        biologia = estudiante[6]
        computacion = estudiante[7]
        ingles = estudiante[8]
        arte = estudiante[9]
        ed_fisica = estudiante[10]
        promedio = estudiante[11]
        
        #1er Lapso
        castellano1 = estudiante[12]
        matematica1 = estudiante[13]
        GHC1 = estudiante[14]
        religion1 = estudiante[15]
        biologia1 = estudiante[16]
        computacion1 = estudiante[17]
        ingles1 = estudiante[18]
        arte1 = estudiante[19]
        ed_fisica1 = estudiante[20]
        promedio1 = estudiante[21]
        
        cursor = db.database.cursor()
        
        pdf.add_page()
                        
        #Promedios Seccion
        sqlPromCastellano = "SELECT Castellano FROM segundo_lapso_a"
        cursor.execute(sqlPromCastellano)
        resCastellano = cursor.fetchall()
        rowCastellano = [row[0] for row in resCastellano]
        promCastellano = round(sum(rowCastellano) / len(rowCastellano))
        
        sqlPromMatematica = "SELECT Matematica FROM segundo_lapso_a"
        cursor.execute(sqlPromMatematica)
        resMatematica = cursor.fetchall()
        rowMatematica = [row[0] for row in resMatematica]
        promMatematica = round(sum(rowMatematica) / len(rowMatematica))
        
        sqlPromGHC = "SELECT GHC FROM segundo_lapso_a"
        cursor.execute(sqlPromGHC)
        resGHC = cursor.fetchall()
        rowGHC = [row[0] for row in resGHC]
        promGHC = round(sum(rowGHC) / len(rowGHC))
        
        sqlPromReligion = "SELECT Religion FROM segundo_lapso_a"
        cursor.execute(sqlPromReligion)
        resReligion = cursor.fetchall()
        rowReligion = [row[0] for row in resReligion]
        promReligion = round(sum(rowReligion) / len(rowReligion))
        
        sqlPromBiologia = "SELECT Biologia FROM segundo_lapso_a"
        cursor.execute(sqlPromBiologia)
        resBiologia = cursor.fetchall()
        rowBiologia = [row[0] for row in resBiologia]
        promBiologia = round(sum(rowBiologia) / len(rowBiologia))
        
        sqlPromComputacion = "SELECT Computacion FROM segundo_lapso_a"
        cursor.execute(sqlPromComputacion)
        resComputacion = cursor.fetchall()
        rowComputacion = [row[0] for row in resComputacion]
        promComputacion = round(sum(rowComputacion) / len(rowComputacion))
        
        sqlPromIngles = "SELECT Ingles FROM segundo_lapso_a"
        cursor.execute(sqlPromIngles)
        resIngles = cursor.fetchall()
        rowIngles = [row[0] for row in resIngles]
        promIngles = round(sum(rowIngles) / len(rowIngles))
        
        sqlPromArte = "SELECT Arte FROM segundo_lapso_a"
        cursor.execute(sqlPromArte)
        resArte = cursor.fetchall()
        rowArte = [row[0] for row in resArte]
        promArte = round(sum(rowArte) / len(rowArte))
        
        sqlPromEd_fisica = "SELECT Educacion_fisica FROM segundo_lapso_a"
        cursor.execute(sqlPromEd_fisica)
        resEd_fisica = cursor.fetchall()
        rowEd_fisica = [row[0] for row in resEd_fisica]
        promEd_fisica = round(sum(rowEd_fisica) / len(rowEd_fisica))
        
        #Promedio General Seccion
        promedioGeneralLapsoSeccion = str(round((promCastellano + promMatematica + promGHC + promReligion + promBiologia + promComputacion + promIngles + promArte + promEd_fisica) / 9 , 2))
        
        #Grafico
        bar_width = 0.35
        separacion = 0.5
        x = np.arange(9) * (bar_width * 2 + separacion)
        y1 = [castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica]
        y2 = [promCastellano, promMatematica, promGHC, promReligion, promBiologia, promComputacion, promIngles, promArte, promEd_fisica]

        fig, ax = plt.subplots(figsize=(6, 2))
        bar1 = ax.bar(x - bar_width/2, y1, bar_width, label='Nota', color='black')
        bar2 = ax.bar(x + bar_width/2, y2, bar_width, label='Prom. Sec.', color='gray')

        ax.set_ylabel('Notas')
        ax.set_xticks(x)
        ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(f'static/graficos/grafico{i}.png')
        
        #Fecha
        fecha = datetime.datetime.now()
        fechaBuena = fecha.strftime('%d/%m/%Y')
        
        #--PDF--
        
        #Cuadro Datos colegio
        pdf.set_font('Arial', '', 12)
        pdf.rect(x=10, y=10, w=190, h=130)
        pdf.text(x=50, y=15, txt='Unidad Educativa')
        pdf.text(x=50, y=21, txt='Padre José Cueto')
        pdf.line(50, 23, 84, 23)
        pdf.text(x=53, y=28, txt='Código Plantel:')
        pdf.text(x=55, y=34, txt='PD04022317')
        pdf.line(50, 36, 84, 36)
        pdf.text(x=49, y=41, txt='RIF: J-31435772-7')
        pdf.line(50, 43, 84, 43)
        pdf.line(10, 46, 200, 46)
        pdf.line(88, 10, 88, 46)
        pdf.image('static/imagenes/cueto2.jpeg', x=17, y=13, w=25, h=30)
        
        #Cuadro datos estudiante
        pdf.set_font('Arial', 'B', 12)
        pdf.text(x=100, y=14, txt='' + nombre)
        
        pdf.set_font('Arial', 'B', 10)
        pdf.text(x=130, y=19, txt='Educación Media')
        
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=105, y=24, txt='N° CÉDULA: ' + cedula)
        pdf.text(x=99, y=29, txt='AÑO / SECCIÓN: 1ero / "A"')
        pdf.text(x=92, y=34, txt='PERIODO ESCOLAR: 2020-2021')
        pdf.text(x=107, y=38, txt='MOMENTO: Segundo')
        pdf.text(x=91, y=43, txt='FECHA DE ENTREGA: ' + fechaBuena)
        
        #Titulo boletines
        pdf.set_font('Arial', 'B', 12)
        pdf.text(x=78, y=51, txt='BOLETÍN DE CALIFICACIONES')
        pdf.line(10, 53, 200, 53)

        #Contenido General
        pdf.line(10, 68, 200, 68)
        pdf.line(16, 68, 16, 134)
        pdf.line(10, 134, 200, 134)
        pdf.set_font('Arial', '', 11)
        pdf.text(x=11, y=72, txt='01')
        pdf.text(x=11, y=78, txt='02')
        pdf.text(x=11, y=84, txt='03')
        pdf.text(x=11, y=90, txt='04')
        pdf.text(x=11, y=96, txt='05')
        pdf.text(x=11, y=102, txt='06')
        pdf.text(x=11, y=108, txt='07')
        pdf.text(x=11, y=114, txt='08')
        pdf.text(x=11, y=120, txt='09')
        pdf.text(x=11, y=126, txt='10')
        pdf.text(x=11, y=132, txt='11')
        pdf.text(x=19, y=72, txt='Castellano')
        pdf.text(x=19, y=78, txt='Matemática')
        pdf.text(x=19, y=84, txt='GHC')
        pdf.text(x=19, y=90, txt='Religión')
        pdf.text(x=19, y=96, txt='Biología')
        pdf.text(x=19, y=102, txt='Computación')
        pdf.text(x=19, y=108, txt='Inglés')
        pdf.text(x=19, y=114, txt='Arte')
        pdf.text(x=19, y=120, txt='Educación Física')
        pdf.line(65, 53, 65, 140)
        pdf.line(104, 53, 104, 140)
        pdf.line(65, 60, 200, 60)
        pdf.line(152, 68, 152, 140)
        pdf.set_font('Arial', 'B', 11)
        pdf.text(x=24, y=62, txt='ASIGNATURAS')
        pdf.text(x=72, y=58, txt='2° MOMENTO')
        pdf.set_font('Arial', 'B', 8)
        pdf.text(x=67, y=65, txt='DEFINITIVA DE MOMENTO')
        pdf.set_font('Arial', '', 9)
        pdf.text(x=83, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=83, y=78, txt='' + f"{matematica:02d}")
        pdf.text(x=83, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=83, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=83, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=83, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=83, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=83, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=83, y=120, txt='' + f"{ed_fisica:02d}")
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=19, y=138, txt='Promedios Comparativos:')
        pdf.text(x=81, y=138, txt='' + f"{promedio}")
        pdf.text(x=108, y=138, txt='' + f"{promedio1}")
        pdf.text(x=125, y=138, txt='' + f"{promedio}")
        pdf.text(x=144, y=138, txt='--')
        pdf.text(x=162, y=138, txt='' + f"{promedio}")
        pdf.text(x=185, y=138, txt='' + promedioGeneralLapsoSeccion)
        
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=130, y=58, txt='RESUMEN DE EVALUACIÓN')
        
        pdf.set_font('Arial', '', 8)
        pdf.text(x=106, y=63, txt='PRIMER')
        pdf.text(x=105, y=67, txt='MOMENTO')
        pdf.text(x=121, y=63, txt='SEGUNDO')
        pdf.text(x=121, y=67, txt='MOMENTO')
        pdf.text(x=139, y=63, txt='TERCER')
        pdf.text(x=138, y=67, txt='MOMENTO')
        pdf.text(x=162, y=63, txt='NOTA')
        pdf.text(x=158, y=67, txt='DEFINITIVA')
        pdf.text(x=185, y=63, txt='PROM.')
        pdf.text(x=186, y=67, txt='SEC.')
        
        pdf.set_font('Arial', '', 9)
        pdf.text(x=110, y=72, txt='' + f"{castellano1:02d}")
        pdf.text(x=110, y=78, txt='' + f"{matematica1:02d}")
        pdf.text(x=110, y=84, txt='' + f"{GHC1:02d}")
        pdf.text(x=110, y=90, txt='' + f"{religion1:02d}")
        pdf.text(x=110, y=96, txt='' + f"{biologia1:02d}")
        pdf.text(x=110, y=102, txt='' + f"{computacion1:02d}")
        pdf.text(x=110, y=108, txt='' + f"{ingles1:02d}")
        pdf.text(x=110, y=114, txt='' + f"{arte1:02d}")
        pdf.text(x=110, y=120, txt='' + f"{ed_fisica1:02d}")
        
        pdf.text(x=126, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=126, y=78, txt='' + f"{matematica:02d}")
        pdf.text(x=126, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=126, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=126, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=126, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=126, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=126, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=126, y=120, txt='' + f"{ed_fisica:02d}")
        
        pdf.text(x=145, y=72, txt='-')
        pdf.text(x=145, y=78, txt='-')
        pdf.text(x=145, y=84, txt='-')
        pdf.text(x=145, y=90, txt='-')
        pdf.text(x=145, y=96, txt='-')
        pdf.text(x=145, y=102, txt='-')
        pdf.text(x=145, y=108, txt='-')
        pdf.text(x=145, y=114, txt='-')
        pdf.text(x=145, y=120, txt='-')
        
        pdf.text(x=164, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=164, y=78, txt='' + f"{matematica:02d}")
        pdf.text(x=164, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=164, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=164, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=164, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=164, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=164, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=164, y=120, txt='' + f"{ed_fisica:02d}")
        
        pdf.text(x=187, y=72, txt='' + f"{promCastellano:02d}")
        pdf.text(x=187, y=78, txt='' + f"{promMatematica:02d}")
        pdf.text(x=187, y=84, txt='' + f"{promGHC:02d}")
        pdf.text(x=187, y=90, txt='' + f"{promReligion:02d}")
        pdf.text(x=187, y=96, txt='' + f"{promBiologia:02d}")
        pdf.text(x=187, y=102, txt='' + f"{promComputacion:02d}")
        pdf.text(x=187, y=108, txt='' + f"{promIngles:02d}")
        pdf.text(x=187, y=114, txt='' + f"{promArte:02d}")
        pdf.text(x=187, y=120, txt='' + f"{promEd_fisica:02d}")
        
        #Grafico, Observaciones, Sello y Firmas
        pdf.rect(x=10, y=146, w=142, h=50)
        pdf.rect(x=10, y=197, w=190, h=57)
        pdf.line(153, 146, 200, 146)
        pdf.line(153, 146, 153, 197)
        pdf.line(200, 146, 200, 197)
        pdf.line(10, 204, 200, 204)
        pdf.line(10, 238, 200, 238)
        pdf.line(73, 238, 73, 254)
        pdf.line(136, 238, 136, 254)
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=52, y=144, txt='GRÁFICO DEL PROGRESO ESCOLAR')
        pdf.text(x=60, y=202, txt='OBSERVACIONES SOBRE LA ACTUACIÓN DEL ESTUDIANTE')
        pdf.set_font('Arial', 'B', 8)
        pdf.text(x=163, y=172, txt='SELLO DEL PLANTEL')
        pdf.text(x=20, y=253, txt='DIRECTOR/A: YULEIDA ROJAS')
        pdf.text(x=85, y=253, txt='SUBDIRECTOR: ??????')
        pdf.text(x=144, y=253, txt='COORD. ACAD: CARMELO BOSCÁN')
        pdf.image(f'static/graficos/grafico{i}.png', x=11, y=147, w=140, h=48)
        
        pdf.text(x=105, y=280, txt='' + f"{pdf.page_no()}")
        
        cursor.close()
        
    pdf_path = os.path.join('pdfs', 'ReporteGeneral-2doMomentoA.pdf')
    pdf.output(pdf_path)
    return redirect(url_for('descargarPdfPack2A'))

#-3A-
@app.route('/construirPdf3A', methods=['POST'])
def packPdf3A():
    
    cursor = db.database.cursor()
    
    sqlNotasCombinadas = """
    SELECT
        s.Nombre_completo,
        s.Cedula,
        s.Castellano AS CastellanoSegundo,
        s.Matematica AS MatematicaSegundo,
        s.GHC AS GHCSegundo,
        s.Religion AS ReligionSegundo,
        s.Biologia AS BiologiaSegundo,
        s.Computacion AS ComputacionSegundo,
        s.Ingles AS InglesSegundo,
        s.Arte AS ArteSegundo,
        s.Educacion_fisica AS Educacion_fisicaSegundo,
        s.Promedio AS PromedioSegundo,
        p.Castellano AS CastellanoPrimer,
        p.Matematica AS MatematicaPrimer,
        p.GHC AS GHCPrimer,
        p.Religion AS ReligionPrimer,
        p.Biologia AS BiologiaPrimer,
        p.Computacion AS ComputacionPrimer,
        p.Ingles AS InglesPrimer,
        p.Arte AS ArtePrimer,
        p.Educacion_fisica AS Educacion_fisicaPrimer,
        p.Promedio AS PromedioPrimer,
        t.Castellano AS CastellanoTercer,
        t.Matematica AS MatematicaTercer,
        t.GHC AS GHCTercer,
        t.Religion AS ReligionTercer,
        t.Biologia AS BiologiaTercer,
        t.Computacion AS ComputacionTercer,
        t.Ingles AS InglesTercer,
        t.Arte AS ArteTercer,
        t.Educacion_fisica AS Educacion_fisicaTercer,
        t.Promedio AS PromedioTercer,
        f.Castellano AS CastellanoFinal,
        f.Matematica AS MatematicaFinal,
        f.GHC AS GHCFinal,
        f.Religion AS ReligionFinal,
        f.Biologia AS BiologiaFinal,
        f.Computacion AS ComputacionFinal,
        f.Ingles AS InglesFinal,
        f.Arte AS ArteFinal,
        f.Educacion_fisica AS Educacion_fisicaFinal,
        f.Promedio AS PromedioFinal
    FROM
        segundo_lapso_a s
    LEFT JOIN
        primer_lapso_a p ON s.Cedula = p.Cedula
    LEFT JOIN
        tercer_lapso_a t ON s.Cedula = t.Cedula
    LEFT JOIN
        seccion_a f ON s.Cedula = f.Cedula;
    """

    cursor.execute(sqlNotasCombinadas)
    estudiantesCombinados = cursor.fetchall()
    estudiantesCombinados_json = json.dumps(estudiantesCombinados, cls=DecimalEncoder)

    estudiantesCombinadosJson = json.loads(estudiantesCombinados_json)
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for i, estudiante in enumerate(estudiantesCombinadosJson):
        
        #2do Lapso
        nombre = estudiante[0]
        cedula = estudiante[1]
        castellano = estudiante[2]
        matematica = estudiante[3]
        GHC = estudiante[4]
        religion = estudiante[5]
        biologia = estudiante[6]
        computacion = estudiante[7]
        ingles = estudiante[8]
        arte = estudiante[9]
        ed_fisica = estudiante[10]
        promedio = estudiante[11]
        
        #1er Lapso
        castellano1 = estudiante[12]
        matematica1 = estudiante[13]
        GHC1 = estudiante[14]
        religion1 = estudiante[15]
        biologia1 = estudiante[16]
        computacion1 = estudiante[17]
        ingles1 = estudiante[18]
        arte1 = estudiante[19]
        ed_fisica1 = estudiante[20]
        promedio1 = estudiante[21]
        
        #3er Lapso
        castellano3 = estudiante[22]
        matematica3 = estudiante[23]
        GHC3 = estudiante[24]
        religion3 = estudiante[25]
        biologia3 = estudiante[26]
        computacion3 = estudiante[27]
        ingles3 = estudiante[28]
        arte3 = estudiante[29]
        ed_fisica3 = estudiante[30]
        promedio3 = estudiante[31]
        
        #Finales
        castellanoF = estudiante[32]
        matematicaF = estudiante[33]
        GHCF = estudiante[34]
        religionF = estudiante[35]
        biologiaF = estudiante[36]
        computacionF = estudiante[37]
        inglesF = estudiante[38]
        arteF = estudiante[39]
        ed_fisicaF = estudiante[40]
        promedioF = estudiante[41]
        
        cursor = db.database.cursor()
        
        pdf.add_page()
                        
        #Promedios Seccion
        sqlPromCastellano = "SELECT Castellano FROM tercer_lapso_a"
        cursor.execute(sqlPromCastellano)
        resCastellano = cursor.fetchall()
        rowCastellano = [row[0] for row in resCastellano]
        promCastellano = round(sum(rowCastellano) / len(rowCastellano))
        
        sqlPromMatematica = "SELECT Matematica FROM tercer_lapso_a"
        cursor.execute(sqlPromMatematica)
        resMatematica = cursor.fetchall()
        rowMatematica = [row[0] for row in resMatematica]
        promMatematica = round(sum(rowMatematica) / len(rowMatematica))
        
        sqlPromGHC = "SELECT GHC FROM tercer_lapso_a"
        cursor.execute(sqlPromGHC)
        resGHC = cursor.fetchall()
        rowGHC = [row[0] for row in resGHC]
        promGHC = round(sum(rowGHC) / len(rowGHC))
        
        sqlPromReligion = "SELECT Religion FROM tercer_lapso_a"
        cursor.execute(sqlPromReligion)
        resReligion = cursor.fetchall()
        rowReligion = [row[0] for row in resReligion]
        promReligion = round(sum(rowReligion) / len(rowReligion))
        
        sqlPromBiologia = "SELECT Biologia FROM tercer_lapso_a"
        cursor.execute(sqlPromBiologia)
        resBiologia = cursor.fetchall()
        rowBiologia = [row[0] for row in resBiologia]
        promBiologia = round(sum(rowBiologia) / len(rowBiologia))
        
        sqlPromComputacion = "SELECT Computacion FROM tercer_lapso_a"
        cursor.execute(sqlPromComputacion)
        resComputacion = cursor.fetchall()
        rowComputacion = [row[0] for row in resComputacion]
        promComputacion = round(sum(rowComputacion) / len(rowComputacion))
        
        sqlPromIngles = "SELECT Ingles FROM tercer_lapso_a"
        cursor.execute(sqlPromIngles)
        resIngles = cursor.fetchall()
        rowIngles = [row[0] for row in resIngles]
        promIngles = round(sum(rowIngles) / len(rowIngles))
        
        sqlPromArte = "SELECT Arte FROM tercer_lapso_a"
        cursor.execute(sqlPromArte)
        resArte = cursor.fetchall()
        rowArte = [row[0] for row in resArte]
        promArte = round(sum(rowArte) / len(rowArte))
        
        sqlPromEd_fisica = "SELECT Educacion_fisica FROM tercer_lapso_a"
        cursor.execute(sqlPromEd_fisica)
        resEd_fisica = cursor.fetchall()
        rowEd_fisica = [row[0] for row in resEd_fisica]
        promEd_fisica = round(sum(rowEd_fisica) / len(rowEd_fisica))
        
        #Promedio General Seccion
        promedioGeneralLapsoSeccion = str(round((promCastellano + promMatematica + promGHC + promReligion + promBiologia + promComputacion + promIngles + promArte + promEd_fisica) / 9 , 2))
        
        #Grafico
        bar_width = 0.35
        separacion = 0.5
        x = np.arange(9) * (bar_width * 2 + separacion)
        y1 = [castellano3, matematica3, GHC3, religion3, biologia3, computacion3, ingles3, arte3, ed_fisica3]
        y2 = [promCastellano, promMatematica, promGHC, promReligion, promBiologia, promComputacion, promIngles, promArte, promEd_fisica]

        fig, ax = plt.subplots(figsize=(6, 2))
        bar1 = ax.bar(x - bar_width/2, y1, bar_width, label='Nota', color='black')
        bar2 = ax.bar(x + bar_width/2, y2, bar_width, label='Prom. Sec.', color='gray')

        ax.set_ylabel('Notas')
        ax.set_xticks(x)
        ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(f'static/graficos/grafico{i}.png')
        
        #Fecha
        fecha = datetime.datetime.now()
        fechaBuena = fecha.strftime('%d/%m/%Y')
        
        #--PDF--
        
        #Cuadro Datos colegio
        pdf.set_font('Arial', '', 12)
        pdf.rect(x=10, y=10, w=190, h=130)
        pdf.text(x=50, y=15, txt='Unidad Educativa')
        pdf.text(x=50, y=21, txt='Padre José Cueto')
        pdf.line(50, 23, 84, 23)
        pdf.text(x=53, y=28, txt='Código Plantel:')
        pdf.text(x=55, y=34, txt='PD04022317')
        pdf.line(50, 36, 84, 36)
        pdf.text(x=49, y=41, txt='RIF: J-31435772-7')
        pdf.line(50, 43, 84, 43)
        pdf.line(10, 46, 200, 46)
        pdf.line(88, 10, 88, 46)
        pdf.image('static/imagenes/cueto2.jpeg', x=17, y=13, w=25, h=30)
        
        #Cuadro datos estudiante
        pdf.set_font('Arial', 'B', 12)
        pdf.text(x=100, y=14, txt='' + nombre)
        
        pdf.set_font('Arial', 'B', 10)
        pdf.text(x=130, y=19, txt='Educación Media')
        
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=105, y=24, txt='N° CÉDULA: ' + cedula)
        pdf.text(x=99, y=29, txt='AÑO / SECCIÓN: 1ero / "A"')
        pdf.text(x=92, y=34, txt='PERIODO ESCOLAR: 2020-2021')
        pdf.text(x=107, y=38, txt='MOMENTO: Tercero')
        pdf.text(x=91, y=43, txt='FECHA DE ENTREGA: ' + fechaBuena)
        
        #Titulo boletines
        pdf.set_font('Arial', 'B', 12)
        pdf.text(x=78, y=51, txt='BOLETÍN DE CALIFICACIONES')
        pdf.line(10, 53, 200, 53)

        #Contenido General
        pdf.line(10, 68, 200, 68)
        pdf.line(16, 68, 16, 134)
        pdf.line(10, 134, 200, 134)
        pdf.set_font('Arial', '', 11)
        pdf.text(x=11, y=72, txt='01')
        pdf.text(x=11, y=78, txt='02')
        pdf.text(x=11, y=84, txt='03')
        pdf.text(x=11, y=90, txt='04')
        pdf.text(x=11, y=96, txt='05')
        pdf.text(x=11, y=102, txt='06')
        pdf.text(x=11, y=108, txt='07')
        pdf.text(x=11, y=114, txt='08')
        pdf.text(x=11, y=120, txt='09')
        pdf.text(x=11, y=126, txt='10')
        pdf.text(x=11, y=132, txt='11')
        pdf.text(x=19, y=72, txt='Castellano')
        pdf.text(x=19, y=78, txt='Matemática')
        pdf.text(x=19, y=84, txt='GHC')
        pdf.text(x=19, y=90, txt='Religión')
        pdf.text(x=19, y=96, txt='Biología')
        pdf.text(x=19, y=102, txt='Computación')
        pdf.text(x=19, y=108, txt='Inglés')
        pdf.text(x=19, y=114, txt='Arte')
        pdf.text(x=19, y=120, txt='Educación Física')
        pdf.line(65, 53, 65, 140)
        pdf.line(104, 53, 104, 140)
        pdf.line(65, 60, 200, 60)
        pdf.line(152, 68, 152, 140)
        pdf.set_font('Arial', 'B', 11)
        pdf.text(x=24, y=62, txt='ASIGNATURAS')
        pdf.text(x=72, y=58, txt='3° MOMENTO')
        pdf.set_font('Arial', 'B', 8)
        pdf.text(x=67, y=65, txt='DEFINITIVA DE MOMENTO')
        pdf.set_font('Arial', '', 9)
        pdf.text(x=83, y=72, txt='' + f"{castellano3:02d}")
        pdf.text(x=83, y=78, txt='' + f"{matematica3:02d}")
        pdf.text(x=83, y=84, txt='' + f"{GHC3:02d}")
        pdf.text(x=83, y=90, txt='' + f"{religion3:02d}")
        pdf.text(x=83, y=96, txt='' + f"{biologia3:02d}")
        pdf.text(x=83, y=102, txt='' + f"{computacion3:02d}")
        pdf.text(x=83, y=108, txt='' + f"{ingles3:02d}")
        pdf.text(x=83, y=114, txt='' + f"{arte3:02d}")
        pdf.text(x=83, y=120, txt='' + f"{ed_fisica3:02d}")
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=19, y=138, txt='Promedios Comparativos:')
        pdf.text(x=81, y=138, txt='' + f"{promedio3}")
        pdf.text(x=108, y=138, txt='' + f"{promedio1}")
        pdf.text(x=125, y=138, txt='' + f"{promedio}")
        pdf.text(x=142, y=138, txt='' + f"{promedio3}")
        pdf.text(x=162, y=138, txt='' + f"{promedioF}")
        pdf.text(x=185, y=138, txt='' + promedioGeneralLapsoSeccion)
        
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=130, y=58, txt='RESUMEN DE EVALUACIÓN')
        
        pdf.set_font('Arial', '', 8)
        pdf.text(x=106, y=63, txt='PRIMER')
        pdf.text(x=105, y=67, txt='MOMENTO')
        pdf.text(x=121, y=63, txt='SEGUNDO')
        pdf.text(x=121, y=67, txt='MOMENTO')
        pdf.text(x=139, y=63, txt='TERCER')
        pdf.text(x=138, y=67, txt='MOMENTO')
        pdf.text(x=162, y=63, txt='NOTA')
        pdf.text(x=158, y=67, txt='DEFINITIVA')
        pdf.text(x=185, y=63, txt='PROM.')
        pdf.text(x=186, y=67, txt='SEC.')
        
        pdf.set_font('Arial', '', 9)
        pdf.text(x=110, y=72, txt='' + f"{castellano1:02d}")
        pdf.text(x=110, y=78, txt='' + f"{matematica1:02d}")
        pdf.text(x=110, y=84, txt='' + f"{GHC1:02d}")
        pdf.text(x=110, y=90, txt='' + f"{religion1:02d}")
        pdf.text(x=110, y=96, txt='' + f"{biologia1:02d}")
        pdf.text(x=110, y=102, txt='' + f"{computacion1:02d}")
        pdf.text(x=110, y=108, txt='' + f"{ingles1:02d}")
        pdf.text(x=110, y=114, txt='' + f"{arte1:02d}")
        pdf.text(x=110, y=120, txt='' + f"{ed_fisica1:02d}")
        
        pdf.text(x=126, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=126, y=78, txt='' + f"{matematica:02d}")
        pdf.text(x=126, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=126, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=126, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=126, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=126, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=126, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=126, y=120, txt='' + f"{ed_fisica:02d}")
        
        pdf.text(x=143, y=72, txt='' + f"{castellano3:02d}")
        pdf.text(x=143, y=78, txt='' + f"{matematica3:02d}")
        pdf.text(x=143, y=84, txt='' + f"{GHC3:02d}")
        pdf.text(x=143, y=90, txt='' + f"{religion3:02d}")
        pdf.text(x=143, y=96, txt='' + f"{biologia3:02d}")
        pdf.text(x=143, y=102, txt='' + f"{computacion3:02d}")
        pdf.text(x=143, y=108, txt='' + f"{ingles3:02d}")
        pdf.text(x=143, y=114, txt='' + f"{arte3:02d}")
        pdf.text(x=143, y=120, txt='' + f"{ed_fisica3:02d}")
        
        pdf.text(x=164, y=72, txt='' + f"{castellanoF:02d}")
        pdf.text(x=164, y=78, txt='' + f"{matematicaF:02d}")
        pdf.text(x=164, y=84, txt='' + f"{GHCF:02d}")
        pdf.text(x=164, y=90, txt='' + f"{religionF:02d}")
        pdf.text(x=164, y=96, txt='' + f"{biologiaF:02d}")
        pdf.text(x=164, y=102, txt='' + f"{computacionF:02d}")
        pdf.text(x=164, y=108, txt='' + f"{inglesF:02d}")
        pdf.text(x=164, y=114, txt='' + f"{arteF:02d}")
        pdf.text(x=164, y=120, txt='' + f"{ed_fisicaF:02d}")
        
        pdf.text(x=187, y=72, txt='' + f"{promCastellano:02d}")
        pdf.text(x=187, y=78, txt='' + f"{promMatematica:02d}")
        pdf.text(x=187, y=84, txt='' + f"{promGHC:02d}")
        pdf.text(x=187, y=90, txt='' + f"{promReligion:02d}")
        pdf.text(x=187, y=96, txt='' + f"{promBiologia:02d}")
        pdf.text(x=187, y=102, txt='' + f"{promComputacion:02d}")
        pdf.text(x=187, y=108, txt='' + f"{promIngles:02d}")
        pdf.text(x=187, y=114, txt='' + f"{promArte:02d}")
        pdf.text(x=187, y=120, txt='' + f"{promEd_fisica:02d}")
        
        #Grafico, Observaciones, Sello y Firmas
        pdf.rect(x=10, y=146, w=142, h=50)
        pdf.rect(x=10, y=197, w=190, h=57)
        pdf.line(153, 146, 200, 146)
        pdf.line(153, 146, 153, 197)
        pdf.line(200, 146, 200, 197)
        pdf.line(10, 204, 200, 204)
        pdf.line(10, 238, 200, 238)
        pdf.line(73, 238, 73, 254)
        pdf.line(136, 238, 136, 254)
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=52, y=144, txt='GRÁFICO DEL PROGRESO ESCOLAR')
        pdf.text(x=60, y=202, txt='OBSERVACIONES SOBRE LA ACTUACIÓN DEL ESTUDIANTE')
        pdf.set_font('Arial', 'B', 8)
        pdf.text(x=163, y=172, txt='SELLO DEL PLANTEL')
        pdf.text(x=20, y=253, txt='DIRECTOR/A: YULEIDA ROJAS')
        pdf.text(x=85, y=253, txt='SUBDIRECTOR: ??????')
        pdf.text(x=144, y=253, txt='COORD. ACAD: CARMELO BOSCÁN')
        pdf.image(f'static/graficos/grafico{i}.png', x=11, y=147, w=140, h=48)
        
        pdf.text(x=105, y=280, txt='' + f"{pdf.page_no()}")
        
        cursor.close()
        
    pdf_path = os.path.join('pdfs', 'ReporteGeneral-3erMomentoA.pdf')
    pdf.output(pdf_path)
    return redirect(url_for('descargarPdfPack3A'))

#-1B-
@app.route('/construirPdf1B', methods=['POST'])
def packPdf1B():
    
    cursor = db.database.cursor()
    sqlNotas = "SELECT Nombre_completo, Cedula, Castellano, Matematica, GHC, Religion, Biologia, Computacion, Ingles, Arte, Educacion_fisica, Promedio FROM primer_lapso_b"
    cursor.execute(sqlNotas)
    estudiantes = cursor.fetchall()
    estudiantes_json = json.dumps(estudiantes, cls=DecimalEncoder)
    
    estudiantesJson = json.loads(estudiantes_json)
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for i, estudiante in enumerate(estudiantesJson):
        
        cursor = db.database.cursor()
        
        pdf.add_page()
                
        nombre, cedula, castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica, promedio = estudiante
        
        #Promedios Seccion
        sqlPromCastellano = "SELECT Castellano FROM primer_lapso_b"
        cursor.execute(sqlPromCastellano)
        resCastellano = cursor.fetchall()
        rowCastellano = [row[0] for row in resCastellano]
        promCastellano = round(sum(rowCastellano) / len(rowCastellano))
        
        sqlPromMatematica = "SELECT Matematica FROM primer_lapso_b"
        cursor.execute(sqlPromMatematica)
        resMatematica = cursor.fetchall()
        rowMatematica = [row[0] for row in resMatematica]
        promMatematica = round(sum(rowMatematica) / len(rowMatematica))
        
        sqlPromGHC = "SELECT GHC FROM primer_lapso_b"
        cursor.execute(sqlPromGHC)
        resGHC = cursor.fetchall()
        rowGHC = [row[0] for row in resGHC]
        promGHC = round(sum(rowGHC) / len(rowGHC))
        
        sqlPromReligion = "SELECT Religion FROM primer_lapso_b"
        cursor.execute(sqlPromReligion)
        resReligion = cursor.fetchall()
        rowReligion = [row[0] for row in resReligion]
        promReligion = round(sum(rowReligion) / len(rowReligion))
        
        sqlPromBiologia = "SELECT Biologia FROM primer_lapso_b"
        cursor.execute(sqlPromBiologia)
        resBiologia = cursor.fetchall()
        rowBiologia = [row[0] for row in resBiologia]
        promBiologia = round(sum(rowBiologia) / len(rowBiologia))
        
        sqlPromComputacion = "SELECT Computacion FROM primer_lapso_b"
        cursor.execute(sqlPromComputacion)
        resComputacion = cursor.fetchall()
        rowComputacion = [row[0] for row in resComputacion]
        promComputacion = round(sum(rowComputacion) / len(rowComputacion))
        
        sqlPromIngles = "SELECT Ingles FROM primer_lapso_b"
        cursor.execute(sqlPromIngles)
        resIngles = cursor.fetchall()
        rowIngles = [row[0] for row in resIngles]
        promIngles = round(sum(rowIngles) / len(rowIngles))
        
        sqlPromArte = "SELECT Arte FROM primer_lapso_b"
        cursor.execute(sqlPromArte)
        resArte = cursor.fetchall()
        rowArte = [row[0] for row in resArte]
        promArte = round(sum(rowArte) / len(rowArte))
        
        sqlPromEd_fisica = "SELECT Educacion_fisica FROM primer_lapso_b"
        cursor.execute(sqlPromEd_fisica)
        resEd_fisica = cursor.fetchall()
        rowEd_fisica = [row[0] for row in resEd_fisica]
        promEd_fisica = round(sum(rowEd_fisica) / len(rowEd_fisica))
        
        #Promedio General Seccion
        promedioGeneralLapsoSeccion = str(round((promCastellano + promMatematica + promGHC + promReligion + promBiologia + promComputacion + promIngles + promArte + promEd_fisica) / 9 , 2))
        
        #Grafico
        bar_width = 0.35
        separacion = 0.5
        x = np.arange(9) * (bar_width * 2 + separacion)
        y1 = [castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica]
        y2 = [promCastellano, promMatematica, promGHC, promReligion, promBiologia, promComputacion, promIngles, promArte, promEd_fisica]

        fig, ax = plt.subplots(figsize=(6, 2))
        bar1 = ax.bar(x - bar_width/2, y1, bar_width, label='Nota', color='black')
        bar2 = ax.bar(x + bar_width/2, y2, bar_width, label='Prom. Sec.', color='gray')

        ax.set_ylabel('Notas')
        ax.set_xticks(x)
        ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(f'static/graficos/grafico{i}.png')
        
        #Fecha
        fecha = datetime.datetime.now()
        fechaBuena = fecha.strftime('%d/%m/%Y')
        
        #--PDF--
        
        #Cuadro Datos colegio
        pdf.set_font('Arial', '', 12)
        pdf.rect(x=10, y=10, w=190, h=130)
        pdf.text(x=50, y=15, txt='Unidad Educativa')
        pdf.text(x=50, y=21, txt='Padre José Cueto')
        pdf.line(50, 23, 84, 23)
        pdf.text(x=53, y=28, txt='Código Plantel:')
        pdf.text(x=55, y=34, txt='PD04022317')
        pdf.line(50, 36, 84, 36)
        pdf.text(x=49, y=41, txt='RIF: J-31435772-7')
        pdf.line(50, 43, 84, 43)
        pdf.line(10, 46, 200, 46)
        pdf.line(88, 10, 88, 46)
        pdf.image('static/imagenes/cueto2.jpeg', x=17, y=13, w=25, h=30)
        
        #Cuadro datos estudiante
        pdf.set_font('Arial', 'B', 12)
        pdf.text(x=100, y=14, txt='' + nombre)
        
        pdf.set_font('Arial', 'B', 10)
        pdf.text(x=130, y=19, txt='Educación Media')
        
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=105, y=24, txt='N° CÉDULA: ' + cedula)
        pdf.text(x=99, y=29, txt='AÑO / SECCIÓN: 1ero / "B"')
        pdf.text(x=92, y=34, txt='PERIODO ESCOLAR: 2020-2021')
        pdf.text(x=107, y=38, txt='MOMENTO: Primero')
        pdf.text(x=91, y=43, txt='FECHA DE ENTREGA: ' + fechaBuena)
        
        #Titulo boletines
        pdf.set_font('Arial', 'B', 12)
        pdf.text(x=78, y=51, txt='BOLETÍN DE CALIFICACIONES')
        pdf.line(10, 53, 200, 53)

        #Contenido General
        pdf.line(10, 68, 200, 68)
        pdf.line(16, 68, 16, 134)
        pdf.line(10, 134, 200, 134)
        pdf.set_font('Arial', '', 11)
        pdf.text(x=11, y=72, txt='01')
        pdf.text(x=11, y=78, txt='02')
        pdf.text(x=11, y=84, txt='03')
        pdf.text(x=11, y=90, txt='04')
        pdf.text(x=11, y=96, txt='05')
        pdf.text(x=11, y=102, txt='06')
        pdf.text(x=11, y=108, txt='07')
        pdf.text(x=11, y=114, txt='08')
        pdf.text(x=11, y=120, txt='09')
        pdf.text(x=11, y=126, txt='10')
        pdf.text(x=11, y=132, txt='11')
        pdf.text(x=19, y=72, txt='Castellano')
        pdf.text(x=19, y=78, txt='Matemática')
        pdf.text(x=19, y=84, txt='GHC')
        pdf.text(x=19, y=90, txt='Religión')
        pdf.text(x=19, y=96, txt='Biología')
        pdf.text(x=19, y=102, txt='Computación')
        pdf.text(x=19, y=108, txt='Inglés')
        pdf.text(x=19, y=114, txt='Arte')
        pdf.text(x=19, y=120, txt='Educación Física')
        pdf.line(65, 53, 65, 140)
        pdf.line(104, 53, 104, 140)
        pdf.line(65, 60, 200, 60)
        pdf.line(152, 68, 152, 140)
        pdf.set_font('Arial', 'B', 11)
        pdf.text(x=24, y=62, txt='ASIGNATURAS')
        pdf.text(x=72, y=58, txt='1° MOMENTO')
        pdf.set_font('Arial', 'B', 8)
        pdf.text(x=67, y=65, txt='DEFINITIVA DE MOMENTO')
        pdf.set_font('Arial', '', 9)
        pdf.text(x=83, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=83, y=78, txt='' + f"{matematica:02d}")
        pdf.text(x=83, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=83, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=83, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=83, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=83, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=83, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=83, y=120, txt='' + f"{ed_fisica:02d}")
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=19, y=138, txt='Promedios Comparativos:')
        pdf.text(x=81, y=138, txt='' + f"{promedio}")
        pdf.text(x=108, y=138, txt='' + f"{promedio}")
        pdf.text(x=128, y=138, txt='--')
        pdf.text(x=144, y=138, txt='--')
        pdf.text(x=162, y=138, txt='' + f"{promedio}")
        pdf.text(x=185, y=138, txt='' + promedioGeneralLapsoSeccion)
        
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=130, y=58, txt='RESUMEN DE EVALUACIÓN')
        
        pdf.set_font('Arial', '', 8)
        pdf.text(x=106, y=63, txt='PRIMER')
        pdf.text(x=105, y=67, txt='MOMENTO')
        pdf.text(x=121, y=63, txt='SEGUNDO')
        pdf.text(x=121, y=67, txt='MOMENTO')
        pdf.text(x=139, y=63, txt='TERCER')
        pdf.text(x=138, y=67, txt='MOMENTO')
        pdf.text(x=162, y=63, txt='NOTA')
        pdf.text(x=158, y=67, txt='DEFINITIVA')
        pdf.text(x=185, y=63, txt='PROM.')
        pdf.text(x=186, y=67, txt='SEC.')
        
        pdf.set_font('Arial', '', 9)
        pdf.text(x=110, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=110, y=78, txt='' +  f"{matematica:02d}")
        pdf.text(x=110, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=110, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=110, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=110, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=110, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=110, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=110, y=120, txt='' + f"{ed_fisica:02d}")
        
        pdf.text(x=128, y=72, txt='-')
        pdf.text(x=128, y=78, txt='-')
        pdf.text(x=128, y=84, txt='-')
        pdf.text(x=128, y=90, txt='-')
        pdf.text(x=128, y=96, txt='-')
        pdf.text(x=128, y=102, txt='-')
        pdf.text(x=128, y=108, txt='-')
        pdf.text(x=128, y=114, txt='-')
        pdf.text(x=128, y=120, txt='-')
        
        pdf.text(x=145, y=72, txt='-')
        pdf.text(x=145, y=78, txt='-')
        pdf.text(x=145, y=84, txt='-')
        pdf.text(x=145, y=90, txt='-')
        pdf.text(x=145, y=96, txt='-')
        pdf.text(x=145, y=102, txt='-')
        pdf.text(x=145, y=108, txt='-')
        pdf.text(x=145, y=114, txt='-')
        pdf.text(x=145, y=120, txt='-')
        
        pdf.text(x=164, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=164, y=78, txt='' + f"{matematica:02d}")
        pdf.text(x=164, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=164, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=164, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=164, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=164, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=164, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=164, y=120, txt='' + f"{ed_fisica:02d}")
        
        pdf.text(x=187, y=72, txt='' + f"{promCastellano:02d}")
        pdf.text(x=187, y=78, txt='' + f"{promMatematica:02d}")
        pdf.text(x=187, y=84, txt='' + f"{promGHC:02d}")
        pdf.text(x=187, y=90, txt='' + f"{promReligion:02d}")
        pdf.text(x=187, y=96, txt='' + f"{promBiologia:02d}")
        pdf.text(x=187, y=102, txt='' + f"{promComputacion:02d}")
        pdf.text(x=187, y=108, txt='' + f"{promIngles:02d}")
        pdf.text(x=187, y=114, txt='' + f"{promArte:02d}")
        pdf.text(x=187, y=120, txt='' + f"{promEd_fisica:02d}")
        
        #Grafico, Observaciones, Sello y Firmas
        pdf.rect(x=10, y=146, w=142, h=50)
        pdf.rect(x=10, y=197, w=190, h=57)
        pdf.line(153, 146, 200, 146)
        pdf.line(153, 146, 153, 197)
        pdf.line(200, 146, 200, 197)
        pdf.line(10, 204, 200, 204)
        pdf.line(10, 238, 200, 238)
        pdf.line(73, 238, 73, 254)
        pdf.line(136, 238, 136, 254)
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=52, y=144, txt='GRÁFICO DEL PROGRESO ESCOLAR')
        pdf.text(x=60, y=202, txt='OBSERVACIONES SOBRE LA ACTUACIÓN DEL ESTUDIANTE')
        pdf.set_font('Arial', 'B', 8)
        pdf.text(x=163, y=172, txt='SELLO DEL PLANTEL')
        pdf.text(x=20, y=253, txt='DIRECTOR/A: YULEIDA ROJAS')
        pdf.text(x=85, y=253, txt='SUBDIRECTOR: ??????')
        pdf.text(x=144, y=253, txt='COORD. ACAD: CARMELO BOSCÁN')
        pdf.image(f'static/graficos/grafico{i}.png', x=11, y=147, w=140, h=48)
        
        pdf.text(x=105, y=280, txt='' + f"{pdf.page_no()}")
        
        cursor.close()
        
    pdf_path = os.path.join('pdfs', 'ReporteGeneral-1erMomentoB.pdf')
    pdf.output(pdf_path)
    return redirect(url_for('descargarPdfPack1B'))

#-2B-
@app.route('/construirPdf2B', methods=['POST'])
def packPdf2B():
    
    cursor = db.database.cursor()
    
    sqlNotasCombinadas = """
    SELECT
        s.Nombre_completo,
        s.Cedula,
        s.Castellano AS CastellanoSegundo,
        s.Matematica AS MatematicaSegundo,
        s.GHC AS GHCSegundo,
        s.Religion AS ReligionSegundo,
        s.Biologia AS BiologiaSegundo,
        s.Computacion AS ComputacionSegundo,
        s.Ingles AS InglesSegundo,
        s.Arte AS ArteSegundo,
        s.Educacion_fisica AS Educacion_fisicaSegundo,
        s.Promedio AS PromedioSegundo,
        p.Castellano AS CastellanoPrimer,
        p.Matematica AS MatematicaPrimer,
        p.GHC AS GHCPrimer,
        p.Religion AS ReligionPrimer,
        p.Biologia AS BiologiaPrimer,
        p.Computacion AS ComputacionPrimer,
        p.Ingles AS InglesPrimer,
        p.Arte AS ArtePrimer,
        p.Educacion_fisica AS Educacion_fisicaPrimer,
        p.Promedio AS PromedioPrimer
    FROM
        segundo_lapso_b s
    LEFT JOIN
        primer_lapso_b p ON s.Cedula = p.Cedula;
    """

    cursor.execute(sqlNotasCombinadas)
    estudiantesCombinados = cursor.fetchall()
    estudiantesCombinados_json = json.dumps(estudiantesCombinados, cls=DecimalEncoder)

    estudiantesCombinadosJson = json.loads(estudiantesCombinados_json)
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for i, estudiante in enumerate(estudiantesCombinadosJson):
        
        #2do Lapso
        nombre = estudiante[0]
        cedula = estudiante[1]
        castellano = estudiante[2]
        matematica = estudiante[3]
        GHC = estudiante[4]
        religion = estudiante[5]
        biologia = estudiante[6]
        computacion = estudiante[7]
        ingles = estudiante[8]
        arte = estudiante[9]
        ed_fisica = estudiante[10]
        promedio = estudiante[11]
        
        #1er Lapso
        castellano1 = estudiante[12]
        matematica1 = estudiante[13]
        GHC1 = estudiante[14]
        religion1 = estudiante[15]
        biologia1 = estudiante[16]
        computacion1 = estudiante[17]
        ingles1 = estudiante[18]
        arte1 = estudiante[19]
        ed_fisica1 = estudiante[20]
        promedio1 = estudiante[21]
        
        cursor = db.database.cursor()
        
        pdf.add_page()
                        
        #Promedios Seccion
        sqlPromCastellano = "SELECT Castellano FROM segundo_lapso_b"
        cursor.execute(sqlPromCastellano)
        resCastellano = cursor.fetchall()
        rowCastellano = [row[0] for row in resCastellano]
        promCastellano = round(sum(rowCastellano) / len(rowCastellano))
        
        sqlPromMatematica = "SELECT Matematica FROM segundo_lapso_b"
        cursor.execute(sqlPromMatematica)
        resMatematica = cursor.fetchall()
        rowMatematica = [row[0] for row in resMatematica]
        promMatematica = round(sum(rowMatematica) / len(rowMatematica))
        
        sqlPromGHC = "SELECT GHC FROM segundo_lapso_b"
        cursor.execute(sqlPromGHC)
        resGHC = cursor.fetchall()
        rowGHC = [row[0] for row in resGHC]
        promGHC = round(sum(rowGHC) / len(rowGHC))
        
        sqlPromReligion = "SELECT Religion FROM segundo_lapso_b"
        cursor.execute(sqlPromReligion)
        resReligion = cursor.fetchall()
        rowReligion = [row[0] for row in resReligion]
        promReligion = round(sum(rowReligion) / len(rowReligion))
        
        sqlPromBiologia = "SELECT Biologia FROM segundo_lapso_b"
        cursor.execute(sqlPromBiologia)
        resBiologia = cursor.fetchall()
        rowBiologia = [row[0] for row in resBiologia]
        promBiologia = round(sum(rowBiologia) / len(rowBiologia))
        
        sqlPromComputacion = "SELECT Computacion FROM segundo_lapso_b"
        cursor.execute(sqlPromComputacion)
        resComputacion = cursor.fetchall()
        rowComputacion = [row[0] for row in resComputacion]
        promComputacion = round(sum(rowComputacion) / len(rowComputacion))
        
        sqlPromIngles = "SELECT Ingles FROM segundo_lapso_b"
        cursor.execute(sqlPromIngles)
        resIngles = cursor.fetchall()
        rowIngles = [row[0] for row in resIngles]
        promIngles = round(sum(rowIngles) / len(rowIngles))
        
        sqlPromArte = "SELECT Arte FROM segundo_lapso_b"
        cursor.execute(sqlPromArte)
        resArte = cursor.fetchall()
        rowArte = [row[0] for row in resArte]
        promArte = round(sum(rowArte) / len(rowArte))
        
        sqlPromEd_fisica = "SELECT Educacion_fisica FROM segundo_lapso_b"
        cursor.execute(sqlPromEd_fisica)
        resEd_fisica = cursor.fetchall()
        rowEd_fisica = [row[0] for row in resEd_fisica]
        promEd_fisica = round(sum(rowEd_fisica) / len(rowEd_fisica))
        
        #Promedio General Seccion
        promedioGeneralLapsoSeccion = str(round((promCastellano + promMatematica + promGHC + promReligion + promBiologia + promComputacion + promIngles + promArte + promEd_fisica) / 9 , 2))
        
        #Grafico
        bar_width = 0.35
        separacion = 0.5
        x = np.arange(9) * (bar_width * 2 + separacion)
        y1 = [castellano, matematica, GHC, religion, biologia, computacion, ingles, arte, ed_fisica]
        y2 = [promCastellano, promMatematica, promGHC, promReligion, promBiologia, promComputacion, promIngles, promArte, promEd_fisica]

        fig, ax = plt.subplots(figsize=(6, 2))
        bar1 = ax.bar(x - bar_width/2, y1, bar_width, label='Nota', color='black')
        bar2 = ax.bar(x + bar_width/2, y2, bar_width, label='Prom. Sec.', color='gray')

        ax.set_ylabel('Notas')
        ax.set_xticks(x)
        ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(f'static/graficos/grafico{i}.png')
        
        #Fecha
        fecha = datetime.datetime.now()
        fechaBuena = fecha.strftime('%d/%m/%Y')
        
        #--PDF--
        
        #Cuadro Datos colegio
        pdf.set_font('Arial', '', 12)
        pdf.rect(x=10, y=10, w=190, h=130)
        pdf.text(x=50, y=15, txt='Unidad Educativa')
        pdf.text(x=50, y=21, txt='Padre José Cueto')
        pdf.line(50, 23, 84, 23)
        pdf.text(x=53, y=28, txt='Código Plantel:')
        pdf.text(x=55, y=34, txt='PD04022317')
        pdf.line(50, 36, 84, 36)
        pdf.text(x=49, y=41, txt='RIF: J-31435772-7')
        pdf.line(50, 43, 84, 43)
        pdf.line(10, 46, 200, 46)
        pdf.line(88, 10, 88, 46)
        pdf.image('static/imagenes/cueto2.jpeg', x=17, y=13, w=25, h=30)
        
        #Cuadro datos estudiante
        pdf.set_font('Arial', 'B', 12)
        pdf.text(x=100, y=14, txt='' + nombre)
        
        pdf.set_font('Arial', 'B', 10)
        pdf.text(x=130, y=19, txt='Educación Media')
        
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=105, y=24, txt='N° CÉDULA: ' + cedula)
        pdf.text(x=99, y=29, txt='AÑO / SECCIÓN: 1ero / "B"')
        pdf.text(x=92, y=34, txt='PERIODO ESCOLAR: 2020-2021')
        pdf.text(x=107, y=38, txt='MOMENTO: Segundo')
        pdf.text(x=91, y=43, txt='FECHA DE ENTREGA: ' + fechaBuena)
        
        #Titulo boletines
        pdf.set_font('Arial', 'B', 12)
        pdf.text(x=78, y=51, txt='BOLETÍN DE CALIFICACIONES')
        pdf.line(10, 53, 200, 53)

        #Contenido General
        pdf.line(10, 68, 200, 68)
        pdf.line(16, 68, 16, 134)
        pdf.line(10, 134, 200, 134)
        pdf.set_font('Arial', '', 11)
        pdf.text(x=11, y=72, txt='01')
        pdf.text(x=11, y=78, txt='02')
        pdf.text(x=11, y=84, txt='03')
        pdf.text(x=11, y=90, txt='04')
        pdf.text(x=11, y=96, txt='05')
        pdf.text(x=11, y=102, txt='06')
        pdf.text(x=11, y=108, txt='07')
        pdf.text(x=11, y=114, txt='08')
        pdf.text(x=11, y=120, txt='09')
        pdf.text(x=11, y=126, txt='10')
        pdf.text(x=11, y=132, txt='11')
        pdf.text(x=19, y=72, txt='Castellano')
        pdf.text(x=19, y=78, txt='Matemática')
        pdf.text(x=19, y=84, txt='GHC')
        pdf.text(x=19, y=90, txt='Religión')
        pdf.text(x=19, y=96, txt='Biología')
        pdf.text(x=19, y=102, txt='Computación')
        pdf.text(x=19, y=108, txt='Inglés')
        pdf.text(x=19, y=114, txt='Arte')
        pdf.text(x=19, y=120, txt='Educación Física')
        pdf.line(65, 53, 65, 140)
        pdf.line(104, 53, 104, 140)
        pdf.line(65, 60, 200, 60)
        pdf.line(152, 68, 152, 140)
        pdf.set_font('Arial', 'B', 11)
        pdf.text(x=24, y=62, txt='ASIGNATURAS')
        pdf.text(x=72, y=58, txt='2° MOMENTO')
        pdf.set_font('Arial', 'B', 8)
        pdf.text(x=67, y=65, txt='DEFINITIVA DE MOMENTO')
        pdf.set_font('Arial', '', 9)
        pdf.text(x=83, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=83, y=78, txt='' + f"{matematica:02d}")
        pdf.text(x=83, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=83, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=83, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=83, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=83, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=83, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=83, y=120, txt='' + f"{ed_fisica:02d}")
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=19, y=138, txt='Promedios Comparativos:')
        pdf.text(x=81, y=138, txt='' + f"{promedio}")
        pdf.text(x=108, y=138, txt='' + f"{promedio1}")
        pdf.text(x=125, y=138, txt='' + f"{promedio}")
        pdf.text(x=144, y=138, txt='--')
        pdf.text(x=162, y=138, txt='' + f"{promedio}")
        pdf.text(x=185, y=138, txt='' + promedioGeneralLapsoSeccion)
        
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=130, y=58, txt='RESUMEN DE EVALUACIÓN')
        
        pdf.set_font('Arial', '', 8)
        pdf.text(x=106, y=63, txt='PRIMER')
        pdf.text(x=105, y=67, txt='MOMENTO')
        pdf.text(x=121, y=63, txt='SEGUNDO')
        pdf.text(x=121, y=67, txt='MOMENTO')
        pdf.text(x=139, y=63, txt='TERCER')
        pdf.text(x=138, y=67, txt='MOMENTO')
        pdf.text(x=162, y=63, txt='NOTA')
        pdf.text(x=158, y=67, txt='DEFINITIVA')
        pdf.text(x=185, y=63, txt='PROM.')
        pdf.text(x=186, y=67, txt='SEC.')
        
        pdf.set_font('Arial', '', 9)
        pdf.text(x=110, y=72, txt='' + f"{castellano1:02d}")
        pdf.text(x=110, y=78, txt='' + f"{matematica1:02d}")
        pdf.text(x=110, y=84, txt='' + f"{GHC1:02d}")
        pdf.text(x=110, y=90, txt='' + f"{religion1:02d}")
        pdf.text(x=110, y=96, txt='' + f"{biologia1:02d}")
        pdf.text(x=110, y=102, txt='' + f"{computacion1:02d}")
        pdf.text(x=110, y=108, txt='' + f"{ingles1:02d}")
        pdf.text(x=110, y=114, txt='' + f"{arte1:02d}")
        pdf.text(x=110, y=120, txt='' + f"{ed_fisica1:02d}")
        
        pdf.text(x=126, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=126, y=78, txt='' + f"{matematica:02d}")
        pdf.text(x=126, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=126, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=126, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=126, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=126, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=126, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=126, y=120, txt='' + f"{ed_fisica:02d}")
        
        pdf.text(x=145, y=72, txt='-')
        pdf.text(x=145, y=78, txt='-')
        pdf.text(x=145, y=84, txt='-')
        pdf.text(x=145, y=90, txt='-')
        pdf.text(x=145, y=96, txt='-')
        pdf.text(x=145, y=102, txt='-')
        pdf.text(x=145, y=108, txt='-')
        pdf.text(x=145, y=114, txt='-')
        pdf.text(x=145, y=120, txt='-')
        
        pdf.text(x=164, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=164, y=78, txt='' + f"{matematica:02d}")
        pdf.text(x=164, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=164, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=164, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=164, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=164, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=164, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=164, y=120, txt='' + f"{ed_fisica:02d}")
        
        pdf.text(x=187, y=72, txt='' + f"{promCastellano:02d}")
        pdf.text(x=187, y=78, txt='' + f"{promMatematica:02d}")
        pdf.text(x=187, y=84, txt='' + f"{promGHC:02d}")
        pdf.text(x=187, y=90, txt='' + f"{promReligion:02d}")
        pdf.text(x=187, y=96, txt='' + f"{promBiologia:02d}")
        pdf.text(x=187, y=102, txt='' + f"{promComputacion:02d}")
        pdf.text(x=187, y=108, txt='' + f"{promIngles:02d}")
        pdf.text(x=187, y=114, txt='' + f"{promArte:02d}")
        pdf.text(x=187, y=120, txt='' + f"{promEd_fisica:02d}")
        
        #Grafico, Observaciones, Sello y Firmas
        pdf.rect(x=10, y=146, w=142, h=50)
        pdf.rect(x=10, y=197, w=190, h=57)
        pdf.line(153, 146, 200, 146)
        pdf.line(153, 146, 153, 197)
        pdf.line(200, 146, 200, 197)
        pdf.line(10, 204, 200, 204)
        pdf.line(10, 238, 200, 238)
        pdf.line(73, 238, 73, 254)
        pdf.line(136, 238, 136, 254)
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=52, y=144, txt='GRÁFICO DEL PROGRESO ESCOLAR')
        pdf.text(x=60, y=202, txt='OBSERVACIONES SOBRE LA ACTUACIÓN DEL ESTUDIANTE')
        pdf.set_font('Arial', 'B', 8)
        pdf.text(x=163, y=172, txt='SELLO DEL PLANTEL')
        pdf.text(x=20, y=253, txt='DIRECTOR/A: YULEIDA ROJAS')
        pdf.text(x=85, y=253, txt='SUBDIRECTOR: ??????')
        pdf.text(x=144, y=253, txt='COORD. ACAD: CARMELO BOSCÁN')
        pdf.image(f'static/graficos/grafico{i}.png', x=11, y=147, w=140, h=48)
        
        pdf.text(x=105, y=280, txt='' + f"{pdf.page_no()}")
        
        cursor.close()
        
    pdf_path = os.path.join('pdfs', 'ReporteGeneral-2doMomentoB.pdf')
    pdf.output(pdf_path)
    return redirect(url_for('descargarPdfPack2B'))

#-3B-
@app.route('/construirPdf3B', methods=['POST'])
def packPdf3B():
    
    cursor = db.database.cursor()
    
    sqlNotasCombinadas = """
    SELECT
        s.Nombre_completo,
        s.Cedula,
        s.Castellano AS CastellanoSegundo,
        s.Matematica AS MatematicaSegundo,
        s.GHC AS GHCSegundo,
        s.Religion AS ReligionSegundo,
        s.Biologia AS BiologiaSegundo,
        s.Computacion AS ComputacionSegundo,
        s.Ingles AS InglesSegundo,
        s.Arte AS ArteSegundo,
        s.Educacion_fisica AS Educacion_fisicaSegundo,
        s.Promedio AS PromedioSegundo,
        p.Castellano AS CastellanoPrimer,
        p.Matematica AS MatematicaPrimer,
        p.GHC AS GHCPrimer,
        p.Religion AS ReligionPrimer,
        p.Biologia AS BiologiaPrimer,
        p.Computacion AS ComputacionPrimer,
        p.Ingles AS InglesPrimer,
        p.Arte AS ArtePrimer,
        p.Educacion_fisica AS Educacion_fisicaPrimer,
        p.Promedio AS PromedioPrimer,
        t.Castellano AS CastellanoTercer,
        t.Matematica AS MatematicaTercer,
        t.GHC AS GHCTercer,
        t.Religion AS ReligionTercer,
        t.Biologia AS BiologiaTercer,
        t.Computacion AS ComputacionTercer,
        t.Ingles AS InglesTercer,
        t.Arte AS ArteTercer,
        t.Educacion_fisica AS Educacion_fisicaTercer,
        t.Promedio AS PromedioTercer,
        f.Castellano AS CastellanoFinal,
        f.Matematica AS MatematicaFinal,
        f.GHC AS GHCFinal,
        f.Religion AS ReligionFinal,
        f.Biologia AS BiologiaFinal,
        f.Computacion AS ComputacionFinal,
        f.Ingles AS InglesFinal,
        f.Arte AS ArteFinal,
        f.Educacion_fisica AS Educacion_fisicaFinal,
        f.Promedio AS PromedioFinal
    FROM
        segundo_lapso_b s
    LEFT JOIN
        primer_lapso_b p ON s.Cedula = p.Cedula
    LEFT JOIN
        tercer_lapso_b t ON s.Cedula = t.Cedula
    LEFT JOIN
        seccion_b f ON s.Cedula = f.Cedula;
    """

    cursor.execute(sqlNotasCombinadas)
    estudiantesCombinados = cursor.fetchall()
    estudiantesCombinados_json = json.dumps(estudiantesCombinados, cls=DecimalEncoder)

    estudiantesCombinadosJson = json.loads(estudiantesCombinados_json)
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for i, estudiante in enumerate(estudiantesCombinadosJson):
        
        #2do Lapso
        nombre = estudiante[0]
        cedula = estudiante[1]
        castellano = estudiante[2]
        matematica = estudiante[3]
        GHC = estudiante[4]
        religion = estudiante[5]
        biologia = estudiante[6]
        computacion = estudiante[7]
        ingles = estudiante[8]
        arte = estudiante[9]
        ed_fisica = estudiante[10]
        promedio = estudiante[11]
        
        #1er Lapso
        castellano1 = estudiante[12]
        matematica1 = estudiante[13]
        GHC1 = estudiante[14]
        religion1 = estudiante[15]
        biologia1 = estudiante[16]
        computacion1 = estudiante[17]
        ingles1 = estudiante[18]
        arte1 = estudiante[19]
        ed_fisica1 = estudiante[20]
        promedio1 = estudiante[21]
        
        #3er Lapso
        castellano3 = estudiante[22]
        matematica3 = estudiante[23]
        GHC3 = estudiante[24]
        religion3 = estudiante[25]
        biologia3 = estudiante[26]
        computacion3 = estudiante[27]
        ingles3 = estudiante[28]
        arte3 = estudiante[29]
        ed_fisica3 = estudiante[30]
        promedio3 = estudiante[31]
        
        #Finales
        castellanoF = estudiante[32]
        matematicaF = estudiante[33]
        GHCF = estudiante[34]
        religionF = estudiante[35]
        biologiaF = estudiante[36]
        computacionF = estudiante[37]
        inglesF = estudiante[38]
        arteF = estudiante[39]
        ed_fisicaF = estudiante[40]
        promedioF = estudiante[41]
        
        cursor = db.database.cursor()
        
        pdf.add_page()
                        
        #Promedios Seccion
        sqlPromCastellano = "SELECT Castellano FROM tercer_lapso_b"
        cursor.execute(sqlPromCastellano)
        resCastellano = cursor.fetchall()
        rowCastellano = [row[0] for row in resCastellano]
        promCastellano = round(sum(rowCastellano) / len(rowCastellano))
        
        sqlPromMatematica = "SELECT Matematica FROM tercer_lapso_b"
        cursor.execute(sqlPromMatematica)
        resMatematica = cursor.fetchall()
        rowMatematica = [row[0] for row in resMatematica]
        promMatematica = round(sum(rowMatematica) / len(rowMatematica))
        
        sqlPromGHC = "SELECT GHC FROM tercer_lapso_b"
        cursor.execute(sqlPromGHC)
        resGHC = cursor.fetchall()
        rowGHC = [row[0] for row in resGHC]
        promGHC = round(sum(rowGHC) / len(rowGHC))
        
        sqlPromReligion = "SELECT Religion FROM tercer_lapso_b"
        cursor.execute(sqlPromReligion)
        resReligion = cursor.fetchall()
        rowReligion = [row[0] for row in resReligion]
        promReligion = round(sum(rowReligion) / len(rowReligion))
        
        sqlPromBiologia = "SELECT Biologia FROM tercer_lapso_b"
        cursor.execute(sqlPromBiologia)
        resBiologia = cursor.fetchall()
        rowBiologia = [row[0] for row in resBiologia]
        promBiologia = round(sum(rowBiologia) / len(rowBiologia))
        
        sqlPromComputacion = "SELECT Computacion FROM tercer_lapso_b"
        cursor.execute(sqlPromComputacion)
        resComputacion = cursor.fetchall()
        rowComputacion = [row[0] for row in resComputacion]
        promComputacion = round(sum(rowComputacion) / len(rowComputacion))
        
        sqlPromIngles = "SELECT Ingles FROM tercer_lapso_b"
        cursor.execute(sqlPromIngles)
        resIngles = cursor.fetchall()
        rowIngles = [row[0] for row in resIngles]
        promIngles = round(sum(rowIngles) / len(rowIngles))
        
        sqlPromArte = "SELECT Arte FROM tercer_lapso_b"
        cursor.execute(sqlPromArte)
        resArte = cursor.fetchall()
        rowArte = [row[0] for row in resArte]
        promArte = round(sum(rowArte) / len(rowArte))
        
        sqlPromEd_fisica = "SELECT Educacion_fisica FROM tercer_lapso_b"
        cursor.execute(sqlPromEd_fisica)
        resEd_fisica = cursor.fetchall()
        rowEd_fisica = [row[0] for row in resEd_fisica]
        promEd_fisica = round(sum(rowEd_fisica) / len(rowEd_fisica))
        
        #Promedio General Seccion
        promedioGeneralLapsoSeccion = str(round((promCastellano + promMatematica + promGHC + promReligion + promBiologia + promComputacion + promIngles + promArte + promEd_fisica) / 9 , 2))
        
        #Grafico
        bar_width = 0.35
        separacion = 0.5
        x = np.arange(9) * (bar_width * 2 + separacion)
        y1 = [castellano3, matematica3, GHC3, religion3, biologia3, computacion3, ingles3, arte3, ed_fisica3]
        y2 = [promCastellano, promMatematica, promGHC, promReligion, promBiologia, promComputacion, promIngles, promArte, promEd_fisica]

        fig, ax = plt.subplots(figsize=(6, 2))
        bar1 = ax.bar(x - bar_width/2, y1, bar_width, label='Nota', color='black')
        bar2 = ax.bar(x + bar_width/2, y2, bar_width, label='Prom. Sec.', color='gray')

        ax.set_ylabel('Notas')
        ax.set_xticks(x)
        ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(f'static/graficos/grafico{i}.png')
        
        #Fecha
        fecha = datetime.datetime.now()
        fechaBuena = fecha.strftime('%d/%m/%Y')
        
        #--PDF--
        
        #Cuadro Datos colegio
        pdf.set_font('Arial', '', 12)
        pdf.rect(x=10, y=10, w=190, h=130)
        pdf.text(x=50, y=15, txt='Unidad Educativa')
        pdf.text(x=50, y=21, txt='Padre José Cueto')
        pdf.line(50, 23, 84, 23)
        pdf.text(x=53, y=28, txt='Código Plantel:')
        pdf.text(x=55, y=34, txt='PD04022317')
        pdf.line(50, 36, 84, 36)
        pdf.text(x=49, y=41, txt='RIF: J-31435772-7')
        pdf.line(50, 43, 84, 43)
        pdf.line(10, 46, 200, 46)
        pdf.line(88, 10, 88, 46)
        pdf.image('static/imagenes/cueto2.jpeg', x=17, y=13, w=25, h=30)
        
        #Cuadro datos estudiante
        pdf.set_font('Arial', 'B', 12)
        pdf.text(x=100, y=14, txt='' + nombre)
        
        pdf.set_font('Arial', 'B', 10)
        pdf.text(x=130, y=19, txt='Educación Media')
        
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=105, y=24, txt='N° CÉDULA: ' + cedula)
        pdf.text(x=99, y=29, txt='AÑO / SECCIÓN: 1ero / "B"')
        pdf.text(x=92, y=34, txt='PERIODO ESCOLAR: 2020-2021')
        pdf.text(x=107, y=38, txt='MOMENTO: Tercero')
        pdf.text(x=91, y=43, txt='FECHA DE ENTREGA: ' + fechaBuena)
        
        #Titulo boletines
        pdf.set_font('Arial', 'B', 12)
        pdf.text(x=78, y=51, txt='BOLETÍN DE CALIFICACIONES')
        pdf.line(10, 53, 200, 53)

        #Contenido General
        pdf.line(10, 68, 200, 68)
        pdf.line(16, 68, 16, 134)
        pdf.line(10, 134, 200, 134)
        pdf.set_font('Arial', '', 11)
        pdf.text(x=11, y=72, txt='01')
        pdf.text(x=11, y=78, txt='02')
        pdf.text(x=11, y=84, txt='03')
        pdf.text(x=11, y=90, txt='04')
        pdf.text(x=11, y=96, txt='05')
        pdf.text(x=11, y=102, txt='06')
        pdf.text(x=11, y=108, txt='07')
        pdf.text(x=11, y=114, txt='08')
        pdf.text(x=11, y=120, txt='09')
        pdf.text(x=11, y=126, txt='10')
        pdf.text(x=11, y=132, txt='11')
        pdf.text(x=19, y=72, txt='Castellano')
        pdf.text(x=19, y=78, txt='Matemática')
        pdf.text(x=19, y=84, txt='GHC')
        pdf.text(x=19, y=90, txt='Religión')
        pdf.text(x=19, y=96, txt='Biología')
        pdf.text(x=19, y=102, txt='Computación')
        pdf.text(x=19, y=108, txt='Inglés')
        pdf.text(x=19, y=114, txt='Arte')
        pdf.text(x=19, y=120, txt='Educación Física')
        pdf.line(65, 53, 65, 140)
        pdf.line(104, 53, 104, 140)
        pdf.line(65, 60, 200, 60)
        pdf.line(152, 68, 152, 140)
        pdf.set_font('Arial', 'B', 11)
        pdf.text(x=24, y=62, txt='ASIGNATURAS')
        pdf.text(x=72, y=58, txt='3° MOMENTO')
        pdf.set_font('Arial', 'B', 8)
        pdf.text(x=67, y=65, txt='DEFINITIVA DE MOMENTO')
        pdf.set_font('Arial', '', 9)
        pdf.text(x=83, y=72, txt='' + f"{castellano3:02d}")
        pdf.text(x=83, y=78, txt='' + f"{matematica3:02d}")
        pdf.text(x=83, y=84, txt='' + f"{GHC3:02d}")
        pdf.text(x=83, y=90, txt='' + f"{religion3:02d}")
        pdf.text(x=83, y=96, txt='' + f"{biologia3:02d}")
        pdf.text(x=83, y=102, txt='' + f"{computacion3:02d}")
        pdf.text(x=83, y=108, txt='' + f"{ingles3:02d}")
        pdf.text(x=83, y=114, txt='' + f"{arte3:02d}")
        pdf.text(x=83, y=120, txt='' + f"{ed_fisica3:02d}")
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=19, y=138, txt='Promedios Comparativos:')
        pdf.text(x=81, y=138, txt='' + f"{promedio3}")
        pdf.text(x=108, y=138, txt='' + f"{promedio1}")
        pdf.text(x=125, y=138, txt='' + f"{promedio}")
        pdf.text(x=142, y=138, txt='' + f"{promedio3}")
        pdf.text(x=162, y=138, txt='' + f"{promedioF}")
        pdf.text(x=185, y=138, txt='' + promedioGeneralLapsoSeccion)
        
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=130, y=58, txt='RESUMEN DE EVALUACIÓN')
        
        pdf.set_font('Arial', '', 8)
        pdf.text(x=106, y=63, txt='PRIMER')
        pdf.text(x=105, y=67, txt='MOMENTO')
        pdf.text(x=121, y=63, txt='SEGUNDO')
        pdf.text(x=121, y=67, txt='MOMENTO')
        pdf.text(x=139, y=63, txt='TERCER')
        pdf.text(x=138, y=67, txt='MOMENTO')
        pdf.text(x=162, y=63, txt='NOTA')
        pdf.text(x=158, y=67, txt='DEFINITIVA')
        pdf.text(x=185, y=63, txt='PROM.')
        pdf.text(x=186, y=67, txt='SEC.')
        
        pdf.set_font('Arial', '', 9)
        pdf.text(x=110, y=72, txt='' + f"{castellano1:02d}")
        pdf.text(x=110, y=78, txt='' + f"{matematica1:02d}")
        pdf.text(x=110, y=84, txt='' + f"{GHC1:02d}")
        pdf.text(x=110, y=90, txt='' + f"{religion1:02d}")
        pdf.text(x=110, y=96, txt='' + f"{biologia1:02d}")
        pdf.text(x=110, y=102, txt='' + f"{computacion1:02d}")
        pdf.text(x=110, y=108, txt='' + f"{ingles1:02d}")
        pdf.text(x=110, y=114, txt='' + f"{arte1:02d}")
        pdf.text(x=110, y=120, txt='' + f"{ed_fisica1:02d}")
        
        pdf.text(x=126, y=72, txt='' + f"{castellano:02d}")
        pdf.text(x=126, y=78, txt='' + f"{matematica:02d}")
        pdf.text(x=126, y=84, txt='' + f"{GHC:02d}")
        pdf.text(x=126, y=90, txt='' + f"{religion:02d}")
        pdf.text(x=126, y=96, txt='' + f"{biologia:02d}")
        pdf.text(x=126, y=102, txt='' + f"{computacion:02d}")
        pdf.text(x=126, y=108, txt='' + f"{ingles:02d}")
        pdf.text(x=126, y=114, txt='' + f"{arte:02d}")
        pdf.text(x=126, y=120, txt='' + f"{ed_fisica:02d}")
        
        pdf.text(x=143, y=72, txt='' + f"{castellano3:02d}")
        pdf.text(x=143, y=78, txt='' + f"{matematica3:02d}")
        pdf.text(x=143, y=84, txt='' + f"{GHC3:02d}")
        pdf.text(x=143, y=90, txt='' + f"{religion3:02d}")
        pdf.text(x=143, y=96, txt='' + f"{biologia3:02d}")
        pdf.text(x=143, y=102, txt='' + f"{computacion3:02d}")
        pdf.text(x=143, y=108, txt='' + f"{ingles3:02d}")
        pdf.text(x=143, y=114, txt='' + f"{arte3:02d}")
        pdf.text(x=143, y=120, txt='' + f"{ed_fisica3:02d}")
        
        pdf.text(x=164, y=72, txt='' + f"{castellanoF:02d}")
        pdf.text(x=164, y=78, txt='' + f"{matematicaF:02d}")
        pdf.text(x=164, y=84, txt='' + f"{GHCF:02d}")
        pdf.text(x=164, y=90, txt='' + f"{religionF:02d}")
        pdf.text(x=164, y=96, txt='' + f"{biologiaF:02d}")
        pdf.text(x=164, y=102, txt='' + f"{computacionF:02d}")
        pdf.text(x=164, y=108, txt='' + f"{inglesF:02d}")
        pdf.text(x=164, y=114, txt='' + f"{arteF:02d}")
        pdf.text(x=164, y=120, txt='' + f"{ed_fisicaF:02d}")
        
        pdf.text(x=187, y=72, txt='' + f"{promCastellano:02d}")
        pdf.text(x=187, y=78, txt='' + f"{promMatematica:02d}")
        pdf.text(x=187, y=84, txt='' + f"{promGHC:02d}")
        pdf.text(x=187, y=90, txt='' + f"{promReligion:02d}")
        pdf.text(x=187, y=96, txt='' + f"{promBiologia:02d}")
        pdf.text(x=187, y=102, txt='' + f"{promComputacion:02d}")
        pdf.text(x=187, y=108, txt='' + f"{promIngles:02d}")
        pdf.text(x=187, y=114, txt='' + f"{promArte:02d}")
        pdf.text(x=187, y=120, txt='' + f"{promEd_fisica:02d}")
        
        #Grafico, Observaciones, Sello y Firmas
        pdf.rect(x=10, y=146, w=142, h=50)
        pdf.rect(x=10, y=197, w=190, h=57)
        pdf.line(153, 146, 200, 146)
        pdf.line(153, 146, 153, 197)
        pdf.line(200, 146, 200, 197)
        pdf.line(10, 204, 200, 204)
        pdf.line(10, 238, 200, 238)
        pdf.line(73, 238, 73, 254)
        pdf.line(136, 238, 136, 254)
        pdf.set_font('Arial', 'B', 9)
        pdf.text(x=52, y=144, txt='GRÁFICO DEL PROGRESO ESCOLAR')
        pdf.text(x=60, y=202, txt='OBSERVACIONES SOBRE LA ACTUACIÓN DEL ESTUDIANTE')
        pdf.set_font('Arial', 'B', 8)
        pdf.text(x=163, y=172, txt='SELLO DEL PLANTEL')
        pdf.text(x=20, y=253, txt='DIRECTOR/A: YULEIDA ROJAS')
        pdf.text(x=85, y=253, txt='SUBDIRECTOR: ??????')
        pdf.text(x=144, y=253, txt='COORD. ACAD: CARMELO BOSCÁN')
        pdf.image(f'static/graficos/grafico{i}.png', x=11, y=147, w=140, h=48)
        
        pdf.text(x=105, y=280, txt='' + f"{pdf.page_no()}")
        
        cursor.close()
        
    pdf_path = os.path.join('pdfs', 'ReporteGeneral-3erMomentoB.pdf')
    pdf.output(pdf_path)
    return redirect(url_for('descargarPdfPack3B'))
        
#--Rutas de descarga de los PDFs Individuales--

#-"A"-

#Ruta 1A
@app.route('/descargarPdf1A/<string:nombre>', methods=['GET'])
def descargarPdf1A(nombre):
    pdf_path = os.path.join('pdfs', f'{nombre}-PrimerLapso.pdf')
    return send_file(pdf_path, as_attachment=True, download_name=f'{nombre}-PrimerLapso.pdf')

#Ruta 2A
@app.route('/descargarPdf2A/<string:nombre>', methods=['GET'])
def descargarPdf2A(nombre):
    pdf_path = os.path.join('pdfs', f'{nombre}-SegundoLapso.pdf')
    return send_file(pdf_path, as_attachment=True, download_name=f'{nombre}-SegundoLapso.pdf')

#Ruta 3A
@app.route('/descargarPdf3A/<string:nombre>', methods=['GET'])
def descargarPdf3A(nombre):
    pdf_path = os.path.join('pdfs', f'{nombre}-TercerLapso.pdf')
    return send_file(pdf_path, as_attachment=True, download_name=f'{nombre}-TercerLapso.pdf')

#-"B"-

#Ruta 1B
@app.route('/descargarPdf1B/<string:nombre>', methods=['GET'])
def descargarPdf1B(nombre):
    pdf_path = os.path.join('pdfs', f'{nombre}-PrimerLapso.pdf')
    return send_file(pdf_path, as_attachment=True, download_name=f'{nombre}-PrimerLapso.pdf')

#Ruta 2B
@app.route('/descargarPdf2B/<string:nombre>', methods=['GET'])
def descargarPdf2B(nombre):
    pdf_path = os.path.join('pdfs', f'{nombre}-SegundoLapso.pdf')
    return send_file(pdf_path, as_attachment=True, download_name=f'{nombre}-SegundoLapso.pdf')

#Ruta 3B
@app.route('/descargarPdf3B/<string:nombre>', methods=['GET'])
def descargarPdf3B(nombre):
    pdf_path = os.path.join('pdfs', f'{nombre}-TercerLapso.pdf')
    return send_file(pdf_path, as_attachment=True, download_name=f'{nombre}-TercerLapso.pdf')

#-Ruta packs completos de descarga-

#-A-

#Completo 1A
@app.route('/descargarPdfPack1A')
def descargarPdfPack1A():
    pdf_path = os.path.join('pdfs', 'ReporteGeneral-1erMomentoA.pdf')
    return send_file(pdf_path, as_attachment=True, download_name = 'ReporteGeneral-1erMomentoA.pdf')

#Completo 2A
@app.route('/descargarPdfPack2A')
def descargarPdfPack2A():
    pdf_path = os.path.join('pdfs', 'ReporteGeneral-2doMomentoA.pdf')
    return send_file(pdf_path, as_attachment=True, download_name = 'ReporteGeneral-2doMomentoA.pdf')

#Completo 3A
@app.route('/descargarPdfPack3A')
def descargarPdfPack3A():
    pdf_path = os.path.join('pdfs', 'ReporteGeneral-3erMomentoA.pdf')
    return send_file(pdf_path, as_attachment=True, download_name = 'ReporteGeneral-3erMomentoA.pdf')

#-B-

#Completo 1B
@app.route('/descargarPdfPack1B')
def descargarPdfPack1B():
    pdf_path = os.path.join('pdfs', 'ReporteGeneral-1erMomentoB.pdf')
    return send_file(pdf_path, as_attachment=True, download_name = 'ReporteGeneral-1erMomentoB.pdf')

#Completo 2B
@app.route('/descargarPdfPack2B')
def descargarPdfPack2B():
    pdf_path = os.path.join('pdfs', 'ReporteGeneral-2doMomentoB.pdf')
    return send_file(pdf_path, as_attachment=True, download_name = 'ReporteGeneral-2doMomentoB.pdf')

#Completo 3B
@app.route('/descargarPdfPack3B')
def descargarPdfPack3B():
    pdf_path = os.path.join('pdfs', 'ReporteGeneral-3erMomentoB.pdf')
    return send_file(pdf_path, as_attachment=True, download_name = 'ReporteGeneral-3erMomentoB.pdf')

#Ruta de Reinicio de Numeracion pestaña eliminar
@app.route('/reinicio')
def reinicio_numeracion():
    
    cursor = db.database.cursor()
    sqlAlters = [
    "ALTER TABLE registro_estudiantes_a AUTO_INCREMENT = 1",
    "ALTER TABLE registro_estudiantes_b AUTO_INCREMENT = 1",
    "ALTER TABLE seccion_a AUTO_INCREMENT = 1",
    "ALTER TABLE seccion_b AUTO_INCREMENT = 1",
    "ALTER TABLE primer_lapso_a AUTO_INCREMENT = 1",
    "ALTER TABLE primer_lapso_b AUTO_INCREMENT = 1",
    "ALTER TABLE segundo_lapso_a AUTO_INCREMENT = 1",
    "ALTER TABLE segundo_lapso_b AUTO_INCREMENT = 1",
    "ALTER TABLE tercer_lapso_a AUTO_INCREMENT = 1", 
    "ALTER TABLE tercer_lapso_b AUTO_INCREMENT = 1"
    ]
    
    for sql in sqlAlters:
        cursor.execute(sql)
    
    db.database.commit()
    cursor.close()
    return redirect(url_for('pestaña2'))

#Ruta de Reinicio de Numeracion pestaña usuarios
@app.route('/reinicioUsuarios')
def reinicio_numeracion_usuarios():
    
    cursor = db.database.cursor()
    sqlAlters = "ALTER TABLE administradores AUTO_INCREMENT = 1"
    
    cursor.execute(sqlAlters)
    
    db.database.commit()
    cursor.close()
    return redirect(url_for('users'))

if __name__ == '__main__':
    app.secret_key = "corzo"
    app.run(debug=True, port=5000) 