# Crypto Trading Bot

![](https://static01.nyt.com/images/2015/03/08/sunday-review/08ROBOT/08ROBOT-master1050.gif)

## Introduction

Use Crypto Trading Bot to autonomously trade and monitor over 250 crypto currencies on Bittrex. Users can configure their own
custom trading parameters which will control when the bot buys and sells. If you'd like to use only the trading indicators and
not the automated trading functionality, you can check out the
[`tracker`](https://github.com/JPStrydom/Crypto-Trading-Bot/tree/tracker) branch.

#### Features:

- Automated trading based on user configurations
- Automated technical analysis (TA)
- Trade analysis and tracking

Users can add their own algorithms and trading strategies based on technical analysis signals such as RSI, 24 Hour Volume,
and Unit Price.

## How to setup

1. This project requires Python 3.X.X, which can be be found [here](https://www.python.org/ftp/python/3.6.3/python-3.6.3.exe).

2. To install the dependencies for this project, run one of the following commands:

   - Windows: `pip3 install -r requirements.txt`

     _NOTE: If you receive a `'pip3' is not recognized as an internal or external command` error, you
     need to add `pip3` to your environmental `path` variable._

   - Unix: `sudo pip3 install -r requirements.txt`

## How to run

Navigate to the `src` file directory in terminal, and run the command `python bot.py` to start the trading bot.

_NOTE: I would highly recommend getting the python IDE **PyCharm** by JetBrains. Its a great development tool and makes
running and debugging this project a breeze. A free community edition can be found
[here](https://www.jetbrains.com/pycharm/download)._

## Trading

This system allows you to autonomously make and track crypto currency trades on IQ oPTION. It uses a local database strategy
to ensure data is not lost.

The `analyse_buys()` and `analyse_sells()` functions will then apply the `buy_strategy(coin_pair)` and
`sell_strategy(coin_pair)` functions to each valid coin pair on Bittrex. These functions will check each coin pair for
buy/sell signals by utilising the the following two functions:

```print("Bot started ...")
    now = datetime.now()
    # WILL BE USED TO GET OUR OPTION PLACEMENT TIME
    current_time = now.strftime("%H:%M:%S")
    # CUSTOME FORMAT WITHOUT THE DAY
    print("Current tim: ", current_time)

    end_time = now.replace(hour=23, minute=59, second=00, microsecond=00)

    # GET REAL TIME CANDLES
    cc = Iq.get_realtime_candles(goal, size)

    # PLACING AN OPTION
    remaining_time = Iq.get_remaning(expirations_mode)
    purchase_time = remaining_time
    """

    """
# WAIT FOR CURRENT BAR TO CLOSE
    for i in range(purchase_time, 0, -1):
        print(f"{i}", end="\r", flush=True)
        t.sleep(1)
    # PLACE ORDERS
    while now < end_time:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time: ", current_time)

        for k in list(cc.keys()):
            open = (cc[k]['open'])
            close = (cc[k]['close'])
            print("Open: ", open, "|| Close: ", close)

            # CALL OPTION
            if close > open:
                print("Green")

                check, id = Iq.buy(Money, goal, "call", expirations_mode)

                if check:
                    print("'CALL' Option Placed")
                    print("Awaiting 'Call' Option Result...")
                    # FUNCTION TO GET OPTION RESULT
                    print(Iq.check_win_v3(id))
                else:
                    print("'Call' Option Failed.")
            else:
                print("Red")
                check, id = Iq.buy(Money, goal, "put", expirations_mode)
```

See the source code for a more detailed description.

## Donations

## Liability

I am not your financial adviser, nor is this tool. Use this program cautiously as it will trade with your crypto-currencies.
None of the contributors to this project are liable for any loses you may incur. Be wise and always do your own research.

![](https://cdn-images-1.medium.com/max/1600/1*SKlPuk4vscYs3bl1bFdT5g.gif)
