import os
import telebot
import time
import pymysql
import urllib

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


"""
knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

User = os.environ['USER']
Pass = os.environ['pass']

client = pymongo.MongoClient(
    "mongodb+srv://" + User + ":" + Pass +
    "@clusterpepo.saoby.mongodb.net/ClusterPepo?retryWrites=true&w=majority")
db = client.ClusterPepo
print(db.list_collection_names())
"""
dicc={}  
API_KEY = "2034503541:AAGIeh9RmLHhJuVzwMSMk5pQ0PZMYs8OrsQ"
bot = telebot.TeleBot(API_KEY)
#mysql databse
class Database:
    def __init__(self):
        self.connection=pymysql.connect( 
            
            host='localhost', #or add ip
            user='root',
            password='',
            db='bd_placas'
        )

        self.cursor =self.connection.cursor()

        print("conexion estavblecida")

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

    
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    cid = message.chat.id
    mid = message.message_id 
    message_text = message.text 
    user_id = message.from_user.id 
    user_name = message.from_user.first_name 

    print(dicc)
    print(message_text)

    if dicc.get(cid) == 1:
        print("autenticando")
        bot.send_message(message.chat.id, "autenticando...")
        if (database.select_user(message_text,message)):
            bot.send_message(message.chat.id, "usuario encontrado!")
        

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
    bot.reply_to(message, "Informacion de placa \n\nPlaca anterior: AAA-000-A\nPlaca vigente:UWG-204-E \nMunicipio de placa:San Luis Potosí \nSerie: 1G1YY25R695700001 \nMotor: 4 Cil \nModelo/año: 2003 \nMarca: Chevrolet \nSubmarca: Corsa \nTipo: 1 \nClase: 5 \nProcedencia: Nacional \nCombustible: Gasolina\nColor: Azul \nUso: Particular \nCapacidad: 5 personas \nEstatus: Activo \nPrecio: 4000 dls \nFactura:2017-002\n\nInformacion del propietario\nNombre: David Espinoza Escamilla\nRFC: EIED123456ASD\nDirección: Urbano Villalón 500\nTélefono: 1234567890\nURL ubicación: https://www.google.com.mx/maps/place/Urbano+Villalon+500")
    

url = 'https://www.boredpanda.com/blog/wp-content/uploads/2018/12/ai-image-generation-fake-faces-people-nvidia-5c18b20b472c2__700.jpg'
f = open('out.jpg','wb')
f.write(urllib.request.urlopen(url).read())
f.close()

def send_photo(message):
    bot.send_chat_action(message.chat.id, 'upload_photo')
    img = open('out.jpg', 'rb')
    bot.send_photo(message.chat.id, img)
    img.close()

@bot.message_handler(commands=['nombre'])
def nom(message):
    bot.reply_to(message,"RFC:EIED123456ASD\nFecha de nacimiento: 01/01/00\nNacionalidad: Mexicano\nDirección: Urbano Villalón 500 Tierra blanca\nCiudad: San Luis Potosí\nMunicipio: San Luis Potosí\nC.P.: 78369\nNúmero: 1234567890\nGénero: Hombre\nTipo de sangre: O+\nLugar de trabajo: UPSLP\n\nContacto de referencia\nDirección: Urbano Villalón 131 Tierra Blanca\nC.P.: 78369\nTeléfono: 0987654321\nURL redes:https://www.facebook.com/upslp\nURL ubicación: https://www.google.com.mx/maps/place/Urbano+Villalon+131")
    bot.send_message(message.chat.id,"Foto de contacto")
    send_photo(message)
    

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

bot.polling()
