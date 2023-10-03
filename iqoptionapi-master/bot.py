from threading import Thread
from MySQLdb.cursors import Cursor
from flask import Flask,redirect,url_for, request,url_for,flash
from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
from flask.templating import render_template
from iqoptionapi.stable_api import IQ_Option
import time as t
from datetime import datetime
import datetime as dt
import webbrowser

app = Flask(__name__)
app.secret_key = "secret key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'symon'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'user_details' 
mysql = MySQL(app)

#Global Variables
my_user = None
my_pass = None
Iq = None
iqch1 = None
iqchi2 = None

#Stop process
stop_run = False

@app.route("/")
def index():
    return render_template("login.html")
@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['passwd']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Accounts WHERE username='" + username + "' and passwd='" + passwd + "'")
        data = cursor.fetchone()
        if data is None:
            error = "Username or Password wrong"
        else:
            flash("You have successfuly logged in")
            return render_template("index.html")
    return render_template("login.html",error=error)

@app.route("/credentials", methods=['GET','POST'])
def my_form_post():
    global my_user, my_pass, Iq
    #Platform Credentials
    my_user = request.form['username1']
    my_pass = request.form['passwd1']

    #LOG IN TO TRADE ACCOUNT
    Iq = IQ_Option(my_user,my_pass)
    iqch1, iqchi2 = Iq.connect()
    if iqch1 ==True:
        flash("Log In successful.")
    else:
        error = "Log In failed."
    my_blc = Iq.get_balance()

    return render_template('home.html',my_blc=my_blc)

@app.route("/exchange", methods=['GET','POST'])
def view():
    global stop_run
    stop_run = False
    global Iq
    #LOG IN TO TRADE ACCOUNT
    Iq = IQ_Option(my_user,my_pass)
    iqch1, iqchi2 = Iq.connect()
    if iqch1 ==True:
        print("Log In successful.")
    else:
        error = "Log In failed."
    my_blc = Iq.get_balance()
    print(f"Balance : {my_blc}")
    get_url= webbrowser.open('https://iqoption.com/traderoom/')
    #SET TRADE PARAMETERS
    Money = 10
    goal = "EURUSD"
    size = 60
    maxdict = 1
    expirations_mode = 1

    #GET CANDLES
    print("Start Candle Stream/...")
    Iq.start_candles_stream(goal,size,maxdict)

    #LETS DO SOMETHING
    print("Bot started ...")
    now = datetime.now()
    #WILL BE USED TO GET OUR OPTION PLACEMENT TIME
    current_time = now.strftime("%H:%M:%S")
    #CUSTOME FORMAT WITHOUT THE DAY
    print("Current tim: ", current_time)

    end_time = now.replace(hour=23, minute=59, second=00, microsecond=00)

    #GET REAL TIME CANDLES
    cc = Iq.get_realtime_candles(goal,size)

    #PLACING AN OPTION
    remaining_time = Iq.get_remaning(expirations_mode)
    purchase_time = remaining_time

    #WAIT FOR CURRENT BAR TO CLOSE
    for i in range(purchase_time,0,-1):
        print(f"{i}", end="\r", flush=True)
        t.sleep(1)
    #PLACE ORDERS
    while now < end_time:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time: ", current_time)

        for k in list(cc.keys()):
            open = (cc[k]['open'])
            close = (cc[k]['close'])
            print("Open: ", open, "|| Close: ", close)

            # CALL OPTION
            if close>open:
                print("Green")
                
                check,id = Iq.buy(Money, goal, "call", expirations_mode)

                if check:
                    print("'CALL' Option Placed")
                    print("Awaiting 'Call' Option Result...")
                    #FUNCTION TO GET OPTION RESULT
                    print(Iq.check_win_v3(id))
                else:
                    print("'Call' Option Failed.")
            else:
                print("Red")
                check,id = Iq.buy(Money,goal,"put",expirations_mode)

                if check:
                    print("'Put' Option Placed")
                    print("Awaiting '' Option Result...")
                    #FUNCTION TO GET OPTION RESULT
                    print(Iq.check_win_v3(id))
                
                else:
                    print("'Put' option failed.")


def my_function():
    global stop_run
    while not stop_run:
        t.sleep(1)
        print("running...")

def manual_run():
    t = Thread(target=my_function)
    t.start()
    return "Processing"

@app.route("/shut", methods=['GET','POST'])
def shut():
    global stop_run
    stop_run = True
    return render_template("home.html")

@app.route('/register/', methods=['GET', 'POST'])
def register():
    adduser()
    return render_template('forms.html')
#Shutdown server
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET','POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/adduser/', methods=['GET', 'POST'])
def adduser():
    print("Entered")

    try:
        fname = request.form['firstname']
        age = request.form['age']
        return fname,age
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO 'login'('fname','age') VALUES (%s,%s)")
        Cursor.commit()       
        return "Registered"
    except Exception as e:
       return(str(e))

if __name__ == "__main__":
    app.run(debug=True)