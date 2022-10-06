import sqlite3

def ver_enviados(correo): #enviar un usuario y contraseña
    db=sqlite3.connect("mensajeria.s3db") #se conecta a la base de datos
    db.row_factory=sqlite3.Row #envia las cabeceras
    cursor=db.cursor() #crea un apuntador
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora,u.nombreusuario from usuarios u, mensajeria m where u.correo=m.id_usu_recibe and m.id_usu_envia='"+correo+"' order by fecha desc, hora desc"
    cursor.execute(consulta) #ejecuta la consulta
    resultado=cursor.fetchall() #la respuesta la envia a resultado
    return resultado
#--------------------------------------------------
#--------------------------------------------------
def ver_recibidos(correo): #enviar un usuario y contraseña
    db=sqlite3.connect("mensajeria.s3db") #se conecta a la base de datos
    db.row_factory=sqlite3.Row #envia las cabeceras
    cursor=db.cursor() #crea un apuntador
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora,u.nombreusuario from usuarios u, mensajeria m where u.correo=m.id_usu_envia and m.id_usu_recibe='"+correo+"' order by fecha desc, hora desc"
    cursor.execute(consulta) #ejecuta la consulta
    resultado=cursor.fetchall() #la respuesta la envia a resultado
    return resultado
#--------------------------------------------------
#--------------------------------------------------
def validar_usuario(usuario, password): #enviar un usuario y contraseña
    db=sqlite3.connect("mensajeria.s3db") #se conecta a la base de datos
    db.row_factory=sqlite3.Row #envia las cabeceras
    cursor=db.cursor() #crea un apuntador
    consulta="select *from usuarios where correo='"+usuario+"' and password='"+password+"' and estado='1' " #crea la cadena de consulta
    cursor.execute(consulta) #ejecuta la consulta
    resultado=cursor.fetchall() #la respuesta la envia a resultado
    return resultado
#--------------------------------------------------
#--------------------------------------------------
def lista_destinatarios(usuario): #enviar un usuario y contraseña
    db=sqlite3.connect("mensajeria.s3db") #se conecta a la base de datos
    db.row_factory=sqlite3.Row #envia las cabeceras
    cursor=db.cursor() #crea un apuntador
    consulta="select *from usuarios where correo<>'"+usuario+"' " #crea la cadena de consulta
    cursor.execute(consulta) #ejecuta la consulta
    resultado=cursor.fetchall() #la respuesta la envia a resultado
    return resultado
#--------------------------------------------------
#--------------------------------------------------
def actualizaPass(password, correo): 
    db=sqlite3.connect("mensajeria.s3db") #se conecta a la base de datos
    db.row_factory=sqlite3.Row #envia las cabeceras
    cursor=db.cursor() #crea un apuntador
    consulta="update usuarios set password='"+password+"' where correo='"+correo+"' " #crea la cadena de consulta
    cursor.execute(consulta) #ejecuta la consulta
    db.commit() #para confirmar inserccion
    return "1"
#--------------------------------------------------
#--------------------------------------------------
def registrar_mail(origen, destino, asunto, mensaje): #
    db=sqlite3.connect("mensajeria.s3db") #se conecta a la base de datos
    db.row_factory=sqlite3.Row #envia las cabeceras
    cursor=db.cursor() #crea un apuntador
    consulta="insert into mensajeria (asunto,mensaje,fecha,hora,id_usu_envia,id_usu_recibe,estado) values('"+asunto+"','"+mensaje+"',DATE('now'),TIME('now'),'"+origen+"','"+destino+"','0') " #crea la cadena de consulta
    cursor.execute(consulta) #ejecuta la consulta
    db.commit() #para confirmar inserccion
    return "1"
#--------------------------------------------------
#--------------------------------------------------
def registrar_usuario(nombre, correo, password, codigo): #
    try:
        db=sqlite3.connect("mensajeria.s3db") #se conecta a la base de datos
        db.row_factory=sqlite3.Row #envia las cabeceras
        cursor=db.cursor() #crea un apuntador
        consulta="insert into Usuarios (nombreusuario,correo,password,estado,codigoactivacion) values ('"+nombre+"','"+correo+"','"+password+"','0','"+codigo+"') " #crea la cadena de consulta
        cursor.execute(consulta) #ejecuta la consulta
        db.commit() #para confirmar inserccion
        return "Usuario registrado Satisfactoriamente"
    except:
        return "Error!!! Correo ya existente, verifique sus datos de nuevo."

    
#--------------------------------------------------
#--------------------------------------------------
def activar_usuario(codigo): #
    db=sqlite3.connect("mensajeria.s3db") #se conecta a la base de datos
    db.row_factory=sqlite3.Row #envia las cabeceras
    cursor=db.cursor() #crea un apuntador
    consulta="update usuarios set estado='1' where codigoactivacion='"+codigo+"' " #crea la cadena de consulta
    cursor.execute(consulta) #ejecuta la consulta
    db.commit() #para confirmar inserccion

    consulta2="select *from usuarios where codigoactivacion='"+codigo+"' and estado='1' " #crea la cadena de consulta
    cursor.execute(consulta2) #ejecuta la consulta
    resultado=cursor.fetchall() #la respuesta la envia a resultado
    return resultado

   