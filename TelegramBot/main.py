import os
import telebot
import time
import pymysql
import urllib
import hashlib 

'''


'''
commands = {  # command description used in the "help" command
    'start': 'Empieza a usar el bot',
    'help': 'Información de inicio',
    'auth':'iniciar con la autentificación'
    
}

comm_log = {
    'ayuda':'Información acerca del bot',
    'placas' : 'Buscar por placas',
    'nombre': 'Buscar por nombre'

}


comm_busqueda = {
    'placas':'Busqueda por placas',
    'nombre' : 'Busqueda por nombre',
}

"""
knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

User = os.environ['USER']
Pass = os.environ['pass']

"""
#diccionario en el que guardaremos las opciones de los usuarios
dicc={}  
#diccionario para guardar los id
id={}

#diccionario para inicio de sesion
session={}
activ={}

names={}
lasname={}
#
API_KEY = "2034503541:AAGIeh9RmLHhJuVzwMSMk5pQ0PZMYs8OrsQ"
bot = telebot.TeleBot(API_KEY)


    

def send_photo(message):
    url = 'https://res.cloudinary.com/hijsgerw8/image/upload/v1635731437/as_kizuao.jpg'
    f = open('out.jpg','wb')
    f.write(urllib.request.urlopen(url).read())
    f.close()
    bot.send_chat_action(message.chat.id, 'upload_photo')
    img = open('out.jpg', 'rb')
    bot.send_photo(message.chat.id, img)
    img.close()
#mysql databse
class Database:
    def __init__(self):
        '''
        self.connection=pymysql.connect( 
            
            host='localhost', #or add ip
            user='root',
            password='',
            db='bd_placas'
        )
        '''
        #conexion a cloud DB
        
        self.connection=pymysql.connect( 
            
            host='us-cdbr-east-04.cleardb.com', #or add ip
            user='bc931d0e0f9a13',
            password='8e81fbda',
            db='heroku_c58f3f7b5df6dd0'
        )
        

        self.cursor =self.connection.cursor()

        print("conexion establecida")
    #validamos el usuario
    def select_user(self,id,m) -> bool:
        sql='SELECT id_usr FROM usuarios WHERE id_usr = \''+ str(id)+'\'' 

        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            if(user[0]==id):                
                return True
        except Exception as e:
            bot.send_message(m.chat.id, "No se puede autenticar en este momento, por favor contacte con el"+ 
            " administrador de este bot")
            return False
    #validamos la contraseña
    def pasw(self,id,pw,m)->bool:
        
        sql='SELECT pass FROM usuarios WHERE id_usr = \''+ str(id)+'\' and pass = \''+ str(pw)+'\''
        print("validacion :"+pw)
        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            print("Contrabd : "+str(user[0]))
            if(user[0]==pw):
                return True
        except Exception as e:
            bot.send_message(m.chat.id, "Contraseña incorrecta")  
            return False  
    #consulta de datos
    def consulta(self,usr,app,m)-> bool:
        sql='SELECT * FROM propietario WHERE nombre = \''+ str(usr)+'\' and apellido= \''+ str(app)+'\''

        try:
            self.cursor.execute(sql)
            users=self.cursor.fetchall()

            for u in users:
                mensaje="ID: "+str(u[0])+"\n Nombre: "+str(u[1])+"\n Apellido: "+str(u[2])+"\n RFC: "+str(u[3])
                bot.send_message(m.chat.id, mensaje)
                mensaje=""
            return True
        except Exception as e:
            print("La persona con el nombre: "+str(usr)+" "+str(app)+", No existe en la base de datos")
            return False

    #consultar especifico
    # 17/10/21 MODIFICAR CONSULTA SQL, REALIZAR UN JOIN CON LAS TABLAS A LAS QUE ESTA RELACIONADO!!!     
    def con_esp(self,id,m)->bool:
        sql='SELECT * FROM vista_prop WHERE id_pro = \''+str(id)+'\''

        try:
            self.cursor.execute(sql)
            spcu=self.cursor.fetchone()
            
            mensaje=("Nombre: "+str(spcu[1])+"\nApellido: "+str(spcu[2])+"\nRFC: "+str(spcu[3])
            +"\nFecha de nacimiento: "+str(spcu[4])+"\nNacionalidad: "+str(spcu[5])+"\nDireccion: "+str(spcu[6])+', '+str(spcu[7])+', '+str(spcu[8])+
            "\nCiudad: "+str(spcu[10])+"\nMunicipio: "+str(spcu[9])+"\nC.P.: "+str(spcu[11])+"\nNúmero telefónico: "+str(spcu[12])+
            "\nGénero: "+str(spcu[13])+"\nTipo de Sangre: "+str(spcu[14])+"\nLugar de trabajo: "+str(spcu[15])+"\nContacto de referencia: "+str(spcu[16])+
            "\nDirección: "+str(spcu[17])+', '+str(spcu[18])+', '+str(spcu[19])+"\nC.P.: "+str(spcu[20])+"\nTeléfono de contacto: "+str(spcu[21])+"\nURL redes sociales: "+str(spcu[22])+
            #"\nFotografia: "+str(spcu[23])+
            "\nURL Ubicacion: "+str(spcu[24]))
            bot.send_message(m.chat.id, mensaje)
            mensaje=""
            send_photo(m)
            return True
        except Exception as e:
            print("No se pudo realizar la consulta en estos momentos, por favor contacte a su LOCAL IT")
            return False
    #validacion de placa
    def con_placa(self,id,m)-> bool:
        sql='SELECT * FROM vista WHERE placa_an = \''+str(id)+'\''
        sql1='SELECT * FROM vista WHERE placa_vig = \''+str(id)+'\''

        r=0
        self.cursor.execute(sql)
        spcp=self.cursor.fetchone()

        #validacion en diccionario en caso de que no esten las placas
        if spcp==None:
            self.cursor.execute(sql1)
            spcp=self.cursor.fetchone()
            if spcp!=None:
                r=1
        else:
            r=1
        if r==1:
            mensaje=("Placa Anterior: "+str(spcp[0])+"\nPlaca Vigente: "+str(spcp[1])+"\nMunicipio: "+str(spcp[2])+"\nSerie: "+str(spcp[3])
            +"\nMotor: "+str(spcp[4])+"\nAño: "+str(spcp[5])+"\nMarca: "+str(spcp[6])+"\nSubmarca: "+str(spcp[7])+"\nTipo: "+str(spcp[8])
            +"\nClase: "+str(spcp[9])+"\nProcedencia: "+str(spcp[10])+"\nCombustible: "+str(spcp[11])+"\nColor: "+str(spcp[12])+"\nUso: "+str(spcp[13])
            +"\nCapacidad: "+str(spcp[14])+"\nEstatus: "+str(spcp[15])+"\nPrecio: "+str(spcp[16])+"\nFactura: "+str(spcp[17])+"\n\n----Usuario----"
            +"\nNombre: "+str(spcp[19])+' '+str(spcp[20])+"\nRFC: "+str(spcp[21])+"\nDirección: "+str(spcp[22])+', '+str(spcp[23])+', '+str(spcp[24])
            +', '+str(spcp[25])+"\nNumero de celular: "+str(spcp[26])+"\nURL Ubicación: "+str(spcp[27]))
            bot.send_message(m.chat.id, mensaje)
            mensaje=""
            r=0
            return True
        else:
            bot.send_message(m.chat.id, "No existen esas placas")
            return False
       
database= Database()



@bot.message_handler(commands=['start', 'hola', 'Hola'])
def greet(message):
    name = message.from_user.first_name
    #bot.reply_to(message,"Hola, bienvenido")
    #user = update.message.from_user
    bot.send_message(message.chat.id, "Hola " + name + " bienvenido!!")
    #command_help(message)


#ayuda de inicio, before login

@bot.message_handler(commands=['help'])
def command_hel(m):
    cid = m.chat.id
    help_text = "Para iniciar con este bot tienes que autenticarte con el comando /auth"
    bot.send_message(cid, help_text)  # send the generated help page

#auth
@bot.message_handler(commands=['auth'])
def command_help(m):
    cid = m.chat.id
    mes = "Ingresa tu usuario"
    bot.send_message(cid, mes)  # send the generated help page

    dicc[cid]=1
    print(dicc)


# help page
@bot.message_handler(commands=['ayuda'])
def command_a(m):
    cid = m.chat.id
    help_text = "Puedes usar los siguiente comandos: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page





@bot.message_handler(commands=['placas'])
def placa(message):
    try:
        if(session[message.chat.id]==1):
            #bot.reply_to(message, "Informacion de placa \n\nPlaca anterior: AAA-000-A\nPlaca vigente:UWG-204-E \nMunicipio de placa:San Luis Potosí \nSerie: 1G1YY25R695700001 \nMotor: 4 Cil \nModelo/año: 2003 \nMarca: Chevrolet \nSubmarca: Corsa \nTipo: 1 \nClase: 5 \nProcedencia: Nacional \nCombustible: Gasolina\nColor: Azul \nUso: Particular \nCapacidad: 5 personas \nEstatus: Activo \nPrecio: 4000 dls \nFactura:2017-002\n\nInformacion del propietario\nNombre: David Espinoza Escamilla\nRFC: EIED123456ASD\nDirección: Urbano Villalón 500\nTélefono: 1234567890\nURL ubicación: https://www.google.com.mx/maps/place/Urbano+Villalon+500")
            bot.reply_to(message,"Ingresa la placa a buscar (sin guiones, EJ: AAA000A)")
            dicc[message.chat.id]='placas'
    except Exception as e:
        bot.reply_to(message,"Debes de iniciar sesión primero!!!! usa el comando /auth para iniciar")
    


@bot.message_handler(commands=['nombre'])
def nom(message):
    try:
        if(session[message.chat.id]==1):
            #bot.reply_to(message,"RFC:EIED123456ASD\nFecha de nacimiento: 01/01/00\nNacionalidad: Mexicano\nDirección: Urbano Villalón 500 Tierra blanca\nCiudad: San Luis Potosí\nMunicipio: San Luis Potosí\nC.P.: 78369\nNúmero: 1234567890\nGénero: Hombre\nTipo de sangre: O+\nLugar de trabajo: UPSLP\n\nContacto de referencia\nDirección: Urbano Villalón 131 Tierra Blanca\nC.P.: 78369\nTeléfono: 0987654321\nURL redes:https://www.facebook.com/upslp\nURL ubicación: https://www.google.com.mx/maps/place/Urbano+Villalon+131")
            #bot.send_message(message.chat.id,"Foto de contacto")
            #send_photo(message)
            bot.reply_to(message,"Para buscar por nombre, primero ingresa el nombre y despues el apellido\n")
            bot.reply_to(message,"Ingresa el nombre: ")
            dicc[message.chat.id]='nombre'
    except Exception as e:
        bot.reply_to(message,"Debes de iniciar sesión primero!!!! usa el comando /auth para iniciar")
    

'''
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(
        m.chat.id, "No entiendo \"" + m.text +
        "\"\nUsa el comando /help para conocer como utilizar el bot")



def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0
'''


#aqui validamos la respuesta del usuario, lo realizo con banderas para ver en que accion estamos    
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    cid = message.chat.id
    mid = message.message_id 
    message_text = message.text 
    user_id = message.from_user.id 
    user_name = message.from_user.first_name 

    print(dicc)
    print(message_text)
    activ[cid]=1
    if dicc.get(cid) == 1 and activ[cid]==1:  
        print("autenticando")
        bot.send_message(message.chat.id, "autenticando...")
        if (database.select_user(message_text,message)):
            id[cid]=message_text
#            bot.send_message(message.chat.id, "usuario encontrado!")
            bot.send_message(message.chat.id, "Ingresa la contraseña")
            dicc[cid]=2
            activ[cid]=0
#13.10.21            
    #validacion de la contraseña
    if dicc.get(cid) == 2 and activ[cid]==1:            
        res=hashlib.sha256(message_text.encode())
        print("contraseña: "+str(res.hexdigest()))
        if (database.pasw(id.get(cid),res.hexdigest(),message)):
            #si el usuario y contraseña son correctos el usuario estara logeado
           bot.send_message(message.chat.id, "Bienvenido "+str(id.get(cid))) 
           dicc[cid]=0
           activ[cid]=0
           session[cid]=1           
           help_text = "Puedes usar los siguiente comandos para buscar: \n"
           for key in comm_busqueda:  # generate help text out of the commands dictionary defined at the top
               help_text += "/" + key + ": "
               help_text += comm_busqueda[key] + "\n"
                    
           bot.send_message(cid, help_text)  # send the generated help page
        
    if dicc.get(cid) == 'placas' and activ[cid]==1:  
        print("validar placa")
        bot.send_message(message.chat.id, "Buscando....")
        if (database.con_placa(message_text,message)):
            dicc[cid]=22
            activ[cid]=0
        else:
           dicc[cid]=22
           activ[cid]=0
            

    if dicc.get(cid) == 'nombre' and activ[cid]==1:  
        print("validar nombre")
        names[cid]=message_text
        dicc[cid]='app'
        activ[cid]=0
        bot.send_message(message.chat.id, "Ingresa el apellido: ") 

    if dicc.get(cid) == 'app' and activ[cid]==1:  
        print("validar apellido")        
        lasname[cid]=message_text        
        if (database.consulta(names[cid],lasname[cid],message)):
            dicc[cid]='nominfo'
            activ[cid]=0
            bot.send_message(message.chat.id, "Ingresa el numero de ID de la persona: ")
        else:
            dicc[cid]=22
            activ[cid]=0  

    if dicc.get(cid) == 'nominfo' and activ[cid]==1:  
        print("consulta de informacion")
               
        if (database.con_esp(message_text,message)):
            dicc[cid]=22
            activ[cid]=0 
        else:
            dicc[cid]=22
            activ[cid]=0
    if dicc.get(cid) == 22:
        help_text=''
        for key in comm_busqueda:  # generate help text out of the commands dictionary defined at the top
               help_text += "/" + key + ": "
               help_text += comm_busqueda[key] + "\n"                       
        bot.send_message(cid, help_text)  # send the generated help page

bot.polling()
