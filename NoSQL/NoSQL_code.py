from asyncio.windows_events import NULL
import telebot
import numpy as np
import pymongo
import matplotlib.pyplot as plt
from asyncio.windows_events import NULL
import pymongo      

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['BusApp']
BusApp = db['BusApp']

#hiding the api key from everyone
from constants import API_KEY
bot = telebot.TeleBot(API_KEY,parse_mode="MarkdownV2")

#<class 'pymongo.cursor.Cursor'> only one value
#59201

plt.figure(figsize=(11,7))
plt.rcParams.update({'font.size':18})

cursor = BusApp.find()

mylist = []
mylist2 = []

#empty counter
b = 0

for item in cursor:
    
    if item["Latitude"] == '0' :
        #print("skip")
        b = b+1

    else:
        mylist.append(item["Latitude"])
        mylist2.append(item["Longitude"])

print(type(float(mylist[0])))

print(len(mylist))

i=0
while i < (len(mylist)-b):
    plt.plot(float(mylist[i]), float(mylist2[i]), marker="o", markersize=1, markeredgecolor="red", markerfacecolor="red")
    i = i+1

plt.xlabel('Latitude')
plt.ylabel('Longitude')

#Singapore main coordinates
plt.plot(1.3521, 103.8198, marker="x", markersize=8, markeredgecolor="black", markerfacecolor="black")

#uncomment to plot the graph
#plt.show()

@bot.message_handler(commands=['query1'])
def query1_1(message):
    prompt = bot.send_message(message.chat.id, "Please enter the *Bus Code* that you want to check")
    bot.register_next_step_handler(prompt, query1)

def query1(message):
    bus_code = message.text
    print(bus_code)
    
    #query1
    cursor = BusApp.find({'BusStopCode': bus_code},{"ServiceNo":1, "Description":1, "_id":0})

    #converting to array to print
    mylist = []
    mylist2 = []

    for item in cursor:
        mylist.append(item["ServiceNo"])
        mylist2.append(item["Description"])

    #optional to use
    #list = np.concatenate((mylist,mylist2), axis=0)

    combine1 = "*Buses Available* in this " + "BusStop: " + bus_code + ", " + "\n" + mylist2[0] + "\n"
    combine = ""
    for i in mylist:
        combine = combine + str(i) + ", "

    combine =combine1 + combine
    print(combine)
    
    #[:-2] to remove the last comma
    bot.send_message(message.chat.id, combine[:-2])

@bot.message_handler(commands=['query2'])
def query2_2(message):
    prompt = bot.send_message(message.chat.id, "Please enter a *Bus Service Number* to check its route")
    bot.register_next_step_handler(prompt, query2)

def query2(message):
    bus_no = message.text
    print(bus_no)

    #query2
    cursor = BusApp.find( {"$and": [{ "ServiceNo": bus_no},{ "Direction": '1'}]}, {"StopSequence":1, "BusStopCode":1, "Description":1, "_id":0})
    
    #converting to array to print
    mylist = []
    mylist2 = []
    mylist3 = []

    for item in cursor:
        mylist.append(item["StopSequence"])
        mylist2.append(item["BusStopCode"])
        mylist3.append(item["Description"])

    stk = np.stack((mylist, mylist2, mylist3), axis=1)


    combine1 = "*Bus Sequence* of " + "Bus: " + bus_no + " is: " + "\n"
    combine = ""
    i = 0;

    while i < len(stk):
        combine = combine + "Sequence: "+ stk[i][0] + ", BusStopCode: " + stk[i][1] + ", Description: "+ stk[i][2] + "\n"
        i = i+1
    combine = combine1 + combine

    
    bot.send_message(message.chat.id, combine)

@bot.message_handler(commands=['query3'])
def query3(message):

    bot.send_message(message.chat.id,"Please send your *current location*")
    
    @bot.message_handler(content_types=['location'])
    def handle_location(message):

        # create cursor object

        a = message.location.latitude
        l = message.location.longitude

        print(a, l)
        #1.351165 103.695718

        str1 = a + 0.0035
        str2 = l + 0.0035
        str3 = str(a)
        str4 = str(l)

        # #1.3133
        # #103.781

        s2 = str(str2)
        s1 = str(str1)

        #query3
        cursor = BusApp.find({"$and":[{"$and":[{"Latitude":{"$gt": str3}, "Longitude":{"$gt":str4}}]}, \
        {"$and":[{"Latitude":{"$lt": s1}, "Longitude":{"$lt": s2}}]}]}, {"Description":1, "ServiceNo":1, "BusStopCode":1, "_id":0}).sort("Description")

        mylist = []
        mylist2 = []
        mylist3 = []

        for item in cursor:
            mylist.append(item["ServiceNo"])
            mylist2.append(item["BusStopCode"])
            mylist3.append(item["Description"])

        stk = np.stack((mylist, mylist2, mylist3), axis=1)

        combine1 = ""
        combine1 = "*Buses* nearby available: " + "\n"
        combine = ""
        i = 0;

        while i < len(stk):
            combine = combine + "Sequence: "+ stk[i][0] + ", BusStopCode: " + stk[i][1] + ", Description: "+ stk[i][2] + "\n"
            i = i+1
        
        combine = combine1 + combine
        print(combine)
        bot.send_message(message.chat.id, combine)
        

@bot.message_handler(commands=['query4'])
def query4_4(message):
    prompt = bot.send_message(message.chat.id, "Please enter a *Bus No* to check for its details")
    bot.register_next_step_handler(prompt, query4)

def query4(message):
    #smth funny here for some reason
    bus_no = message.text
    print(bus_no)
    
    #query4
    cursor = BusApp.find_one({"$and":[{"ServiceNo":bus_no},{"Direction":'1'}]},
    {"ServiceNo":1,"WD_FirstBus":1,"WD_LastBus":1,"SAT_FirstBus":1,"SAT_LastBus":1,"SUN_FirstBus":1,"SUN_LastBus":1,"Category":1})

    a = list(cursor.values())

    print(type(a))
    print((type(str(a[0]))))
    msges = ""
    
    msges1 = "*The Bus details are*: " + "\n"
    msges = ("ServiceNo: " + str(a[1]) + "\n" + "Week Day First Bus: " + str(a[2]) + "hrs" + ", " + " Week Day Last Bus: " + str(a[3]) + "hrs" + "\n" 
    + "Saturday First Bus: " + str(a[4]) + "hrs" + ", " + " Saturday Last Bus: " + str(a[5]) + "hrs" + "\n" 
    + "Sunday First Bus: " + str(a[6]) + "hrs" + ", " + " Sunday Last Bus: " + str(a[7]) + "hrs" + "\n" 
    + "Bus Category: " + str(a[8]))

    msges = msges1 + msges

    bot.send_message(message.chat.id, msges)

    #print(message)
    print("finish print")
    

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

    #query5
    cursor = BusApp.aggregate([{'$match':{'$or':[{'Description': first},{'Description': second}]}},
    {'$group':{'_id':'$ServiceNo','count':{'$sum':1}}},{'$project':{'count':{'$gt':['$count',2]}}},{'$match':{'count':True}}])

    print(type(cursor))

    mylist = []

    for item in cursor:
        mylist.append(item["_id"])

    combine = ""
    message1 = "Take *bus/buses*: "

    for i in mylist:
            combine = combine + str(i) + ", "

    combine = message1 + combine

    bot.send_message(message.chat.id, combine[:-2])


#starter
@bot.message_handler(commands=['start'])
def start(message):
  bot.reply_to(message, "Welcome to the *SG BUS APP BOT* \nEnter /query1 to find buses in that bus stop \
                        \nEnter /query2 to search for all the stops that your bus will travel \
                        \nEnter /query3 to search for buses around you \
                        \nEnter /query4 to search for the buses's description \
                        \nEnter /query5 to search on which buses to take from a bus Description")
                        
bot.polling()

