
from flask import Flask, render_template, request
import hashlib
import controlador
from datetime import datetime
import envioemail

app = Flask(__name__)

email_origen=""

@app.route("/")
def hello_world():
    return render_template("login.html")    
#--------------------------------------------------
#--------------------------------------------------
@app.route("/validarUsuario", methods=['GET','POST'])
def validarUsuario():
    if request.method=="POST":
        usu=request.form["txtusuario"]
        #inyeccion de datos sql para prevenir que nos dañen, alteren o hackeen la base de datos
        usu=usu.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw=request.form["txtpass"]
        passw=passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw2=passw.encode()
        passw2=hashlib.sha384(passw2).hexdigest()

        respuesta=controlador.validar_usuario(usu,passw2)

        global email_origen

        if len(respuesta)==0:
            email_origen=""
            mensaje = "ERROR DE AUTENTICACION!!!  Verifique sus datos"
            return render_template("informacion.html",datas=mensaje) 
        else:
            email_origen=usu
            respuesta2=controlador.lista_destinatarios(usu)
            return render_template("principal.html",datas=respuesta2)   
#--------------------------------------------------
#--------------------------------------------------
@app.route("/registrarUsuario", methods=['GET','POST'])
def registrarUsuario():
    if request.method=="POST":
        nombre=request.form["txtnombre"]
        nombre=nombre.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        email=request.form["txtusuario2registro"]
        email=email.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw=request.form["txtpassregistro"]
        passw=passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")

        passw2=passw.encode()
        passw2=hashlib.sha384(passw2).hexdigest() #encriptador

        codigo=datetime.now()
        codigo2=str(codigo)
        codigo2=codigo2.replace("-","")
        codigo2=codigo2.replace(" ","")
        codigo2=codigo2.replace(":","")
        codigo2=codigo2.replace(".","")

        print(codigo2)

        mensaje="Hola "+nombre+", tu código de activación es :\n\n"+codigo2+ "\n\n Copialo y pegalo para activar tu cuenta.\n\n Gracias"

        envioemail.enviar(email,mensaje,"Codigo de Activacion")
        
        respuesta=controlador.registrar_usuario(nombre,email,passw2,codigo2)
       
        #mensaje = "El Usuario" " " +nombre+" se ha registrado satisfactoriamente."
        return render_template("informacion.html",datas=respuesta) 
#--------------------------------------------------
#--------------------------------------------------
@app.route("/enviarMAIL", methods=['GET','POST'])
def enviarMAIL():
    if request.method=="POST":
        emailDestino=request.form["emailDestino"]
        asunto=request.form["asunto"]
        asunto=asunto.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        mensaje=request.form["mensaje"]
        mensaje=mensaje.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        controlador.registrar_mail(email_origen,emailDestino,asunto,mensaje)

        mensaje2= "Tienes un mensaje nuevo, por favor ingrese a la plataforma para revisarlo en la pestaña Historial. \n\n Gracias."
        envioemail.enviar(emailDestino,mensaje2,"Nuevo Mensaje Enviado")
        return "Email Enviado Satisfactoriamente"
#--------------------------------------------------
#--------------------------------------------------
@app.route("/HistorialEnviados", methods=['GET','POST'])
def HistorialEnviados():
    resultado=controlador.ver_enviados(email_origen)
    return render_template("respuesta.html",datas=resultado) 
#--------------------------------------------------
#--------------------------------------------------
@app.route("/HistorialRecibidos", methods=['GET','POST'])
def HistorialRecibidos():
    resultado=controlador.ver_recibidos(email_origen)
    return render_template("respuesta2.html",datas=resultado)
#--------------------------------------------------
#--------------------------------------------------       
@app.route("/activarUsuario", methods=['GET','POST'])
def activarUsuario():
    if request.method=="POST":
        codigo=request.form["txtcodigo"]
        codigo=codigo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        respuesta=controlador.activar_usuario(codigo)
        
        if len(respuesta)==0:
            mensaje= "El código de activación es erroneo, verifíquelo e intente nuevamente."
        else: 
            mensaje= "Su usuario ha sido activado exitosamente."
       
        return render_template("informacion.html",datas=mensaje) 
#--------------------------------------------------
#--------------------------------------------------       
@app.route("/actualizacionPassword", methods=['GET','POST'])
def actualizacionPassword():
    if request.method=="POST":
        pass1=request.form["pass"]
        pass1=pass1.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw2=pass1.encode()
        passw2=hashlib.sha384(passw2).hexdigest() #encriptador

        controlador.actualizaPass(passw2,email_origen,)
        return "Actualizacion Exitosa"
        
       