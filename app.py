from flask import Flask,render_template,redirect,request,url_for
from datetime import datetime
import json, requests

app = Flask(__name__)

message_list = []
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/contacts') 
def contacts():
    return render_template("contacts.html")

@app.route('/profile')
def profile():
    return redirect('/')

@app.route("/static/<path:file_path>")
def files(file_path):
    return url_for('static', filename=file_path)

@app.route('/chat', methods=["GET","POST"])
def chat():
    if request.method == "GET":
        return render_template("chat.html")
    else:
        message = request.form.get("message")
        addSystemMessage(message)
        # print(message_list)
        return render_template("chat_update.html", len = len(message_list), message_list=message_list)


@app.route("/sendemail/", methods=['POST'])
def sendemail():
	if request.method == "POST":
		name = request.form['name']
		subject = request.form['Subject']
		email = request.form['_replyto']
		message = request.form['message']

		# Set your credentials and send email using SMTP Server

		try:
			# sending an email
			# server.send_message(msg)
			print("Send")
		except:
			print("Fail to Send")
			pass
			
	return redirect('/')

def hello_world():
    return 'Hello, World!' 
    

def addSystemMessage(msg) :
    e = datetime.now()
    message_list.append({ "user": "user", "message" : msg, "date": "%s:%s" % (e.hour, e.minute)})


    msg = msg.lower()
    sys_msg = ""
    if msg == "hi":
        sys_msg= "Hi there"
    elif msg == "hello":
        sys_msg= "Hello there"
    elif msg == "hola":
        sys_msg= "Olaaa"
    elif msg == "current weather" or msg == "current weather?":
        sys_msg= getWeather()
    else:
        sys_msg= "Sorry! I'm not sure I udnerstand that"

    message_list.append({ "user": "system", "message" : sys_msg, "date" : "%s:%s" % (e.hour, e.minute)})

def getWeather(): 
    # Enter your API key here
    api_key = "35a3f6da1630a1fc51af24468b667652"
    
    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Give city name
    city_name = "St. Petersburg" # input("Enter city name : ")
    
    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    
    # get method of requests module
    # return response object
    response = requests.get(complete_url)
    
    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()
    print('response',x)
    
    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] == "401":
        return "Try again tomorrow";
    if x["cod"] != "404":
    
        # store the value of "main"
        # key in variable y
        y = x["main"]
    
        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]
    
        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]
    
        # store the value corresponding
        # to the "humidity" key of y
        current_humidity = y["humidity"]
    
        # store the value of "weather"
        # key in variable z
        z = x["weather"]
    
        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]
    
        # print following values
        return "Temperature (in kelvin unit) = " + str(current_temperature) + "\n atmospheric pressure (in hPa unit) = " + str(current_pressure) + "\n humidity (in percentage) = " + str(current_humidity) + "\n description = " + str(weather_description)
    else:
        return " City Not Found "


app.run(host="localhost", port=5000, debug=True)
