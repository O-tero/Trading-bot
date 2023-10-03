from iqoptionapi.stable_api import IQ_Option
import time as t
from datetime import datetime
import datetime as dt

#Platform credentials
my_user = input("Username: ")
my_pass = input("Password: ")

#LOG IN TO TRADE ACCOUNT
Iq = IQ_Option(my_user,my_pass)
iqch1, iqchi2 = Iq.connect()

if iqch1 ==True:
    print("Log In successful.")
else:
    print("Log In failed.")

my_blc = Iq.get_balance()
print(f"Balance : {my_blc}")

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
