from asyncio.windows_events import NULL
import telebot
import mysql.connector

# commands for sql
# cd C:\xampp\mysql\bin
# mysql -u root
# use busapp

#59201
#181
#
#2101483
#Boon Lay int to Bird Pk

#hiding the api key from everyone
from constants import API_KEY
bot = telebot.TeleBot(API_KEY,parse_mode="MarkdownV2")

# create connection object
con = mysql.connector.connect(host="localhost", user="root", password="", database="busapp")

@bot.message_handler(commands=['query1'])
def query1_1(message):
    prompt = bot.send_message(message.chat.id, "Please enter the *Bus Code* that you want to check")
    bot.register_next_step_handler(prompt, query1)

def query1(message):
    
    bus_code = message.text
    print(bus_code)

    # create cursor object
    cursor = con.cursor()

    # executing cursor
    cursor.execute("select DISTINCT bi.ServiceNo, bs.BusStopCode, bs.RoadName from BusStops bs, BusRoutes bi \
                    where bs.BusStopCode = bi.busstopcode and bi.BusStopCode = '%s'" % bus_code)

    # fetch answer/reply
    serviceno = cursor.fetchall()

    print(serviceno)

    bot.send_message(message.chat.id, "Buses Availables here in this *Bus Stop* are: ")

    combine = ""

    for i in serviceno:

        if (i != NULL):
            combine = combine + serviceno[serviceno.index(i)][0].replace("_", "\\_") + ", "

        else:
            break
    
    bot.send_message(message.chat.id, combine) 

    # closing cursor connection
    cursor.close()

@bot.message_handler(commands=['query2'])
def query2_2(message):
    prompt = bot.send_message(message.chat.id, "Please enter a *Bus Service Number* to check its route")
    bot.register_next_step_handler(prompt, query2)

def query2(message):
    # create cursor object
    cursor = con.cursor()
    
    bus_no = message.text + '_1'
    print(bus_no)

    # executing cursor
    cursor.execute("SELECT DISTINCT bi.StopSequence, bs.BusStopCode, bs.Description, bi.ServiceNo FROM BusRoutes bi, BusStops bs, Busservices bc \
    WHERE bi.ServiceNo = '%s' and bi.serviceNo = bc.serviceno and bs.BusStopCode = bi.busstopcode ORDER BY length(bi.StopSequence), bi.stopsequence asc" % bus_no)

    # fetch answer/reply
    serviceno2 = cursor.fetchall()
    
    bot.send_message(message.chat.id, "*Bus sequence: *")

    combine = ""

    for i in serviceno2:

        if (i != NULL):
            combine = combine + serviceno2[serviceno2.index(i)][0] + ":     " + serviceno2[serviceno2.index(i)][2] + "\n"

        else:
            break
    
    bot.send_message(message.chat.id,combine)

    # closing cursor connection
    cursor.close()

@bot.message_handler(commands=['query3'])
def query3(message):

    bot.send_message(message.chat.id,"Please send your *current location*")
    
    @bot.message_handler(content_types=['location'])
    def handle_location(message):

        # create cursor object
        cursor = con.cursor()

        # a = 1.39814   
        # l = 103.90656

        a = message.location.latitude
        l = message.location.longitude

        print(a, l)
        # executing cursor
        cursor = con.cursor()
        
        cursor.execute("select bs.BusStopCode,bs.RoadName, bs.Description, sb.serviceno, bs.Latitude, bs.Longitude from  busstops bs, \
                        BusRoutes sb where bs.Latitude between '%s' and ('%s'+0.0035) and bs.Longitude between '%s' and ('%s'+0.0035) and bs.BusStopCode = sb.BusStopCode" % (a,a,l,l))
        
        # fetch answer/reply
        serviceno3 = cursor.fetchall()

        bot.send_message(message.chat.id, "*Buses* nearby available: ")

        combine = ""

        for i in serviceno3:

            if (i != NULL):
                combine = combine + "*Bus Stop Code: *" + serviceno3[serviceno3.index(i)][0] + "\n" + "*Bus Stop Name: *" + serviceno3[serviceno3.index(i)][1] + \
                 "\n" + "*Bus Stop Desc: *" + serviceno3[serviceno3.index(i)][2] + "\n" + "*Bus number: *" + serviceno3[serviceno3.index(i)][3].replace("_", "\\_") + "\n\n"

            else:
                break
        
        bot.send_message(message.chat.id,combine)

        # closing cursor connection
        cursor.close()

@bot.message_handler(commands=['query4'])
def query4_4(message):
    prompt = bot.send_message(message.chat.id, "Please enter a *Student's ID* to check for favourite bus services")
    bot.register_next_step_handler(prompt, query4)

def query4(message):
    # create cursor object
    cursor = con.cursor()   
    
    fav_id = message.text
    print(fav_id)

    # executing cursor
    cursor.execute("SELECT u.user_name, u.user_number, f.fav_busservice, bs.category , f.fav_busstop, a.bus1, a.bus2 \
                    FROM user u, favourites f, have h, arrivaltiming a, busservices bs \
                    WHERE u.user_number = h.user_id and h.fav_bus_stop = f.fav_busstop and a.buscode = f.fav_busstop and \
                    a.busno = f.fav_busservice and bs.serviceno = a.busno and u.user_number = %s" % fav_id)

    # fetch answer/reply
    serviceno4 = cursor.fetchall()

    bot.send_message(message.chat.id, "*Favourite Saved Buses *")

    combine = ""

    for i in serviceno4:

        if (i != NULL):
            combine = combine + "*Student's Name: *" + serviceno4[serviceno4.index(i)][0] + "\n" + "*Student's ID: *" + serviceno4[serviceno4.index(i)][1] + "\n" + "*Bus Service Number: *" + serviceno4[serviceno4.index(i)][2].replace("_", "\\_") + \
                            "\n" + "*Bus Category: *" + serviceno4[serviceno4.index(i)][3] + "\n" + "*Bus Stop Code: *" + serviceno4[serviceno4.index(i)][4] + "\n" + "*First Timing: *" + serviceno4[serviceno4.index(i)][5] + "\n" \
                             + "*Second Timing : *" + serviceno4[serviceno4.index(i)][6]

        else:
            break
    
    bot.send_message(message.chat.id, combine)

    # closing cursor connection
    cursor.close()

@bot.message_handler(commands=['query5'])
def query5_5(message):
    prompt = bot.send_message(message.chat.id, "Please enter your current *Bus Stop Description*")
    bot.register_next_step_handler(prompt,query5_1)

def query5_1(message):
    global first
    first = message.text
    prompt = bot.send_message(message.chat.id, "Please enter your preffered destination *Bus Stop Description*")
    bot.register_next_step_handler(prompt,query5_2)
    
def query5_2(message):
    global second
    second = message.text

    # create cursor object
    print(first,second)

    cursor = con.cursor()   

    query2 = "SELECT br.ServiceNo FROM BusStops bs, BusRoutes br WHERE bs.Description LIKE %s AND bs.BusStopCode=br.BusStopCode INTERSECT SELECT br.ServiceNo \
    FROM BusStops bs, BusRoutes br WHERE bs.Description LIKE %s AND bs.BusStopCode=br.BusStopCode"

    cursor.execute(query2, ("%" + first + "%", "%" + second + "%"))

    # cursor.execute(sql,(first,second))

    # fetch answer/reply
    serviceno5 = cursor.fetchall()
        
    bot.send_message(message.chat.id, "Take *buses*: ")

    combine = ""

    for i in serviceno5:
        if (i != NULL):
            combine = combine + serviceno5[serviceno5.index(i)][0].replace("_", "\\_") + ", "

        else:
            break

    bot.send_message(message.chat.id, combine)

    # closing cursor connection
    cursor.close()

#starter
@bot.message_handler(commands=['start'])
def start(message):
  bot.reply_to(message, "Welcome to the *SG BUS APP BOT* \nEnter /query1 to find buses in that bus stop \
                        \nEnter /query2 to search for all the stops that your bus will travel \
                        \nEnter /query3 to search for buses around you \
                        \nEnter /query4 for your favourite bus stops \
                        \nEnter /query5 to search on which buses to take from a Bus Description")
                        
bot.polling()