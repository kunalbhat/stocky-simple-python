import os, json, ystockquote, re, datetime
from datetime import datetime, timedelta
from flask import Flask, url_for, render_template, request, g, abort

app = Flask(__name__)

# Index page
@app.route('/')
def index():
    return render_template('index.html')

# Symbol lookup
@app.route('/lookup', methods=['GET'])

def lookup():
    symbol = request.args.get('symbol')

    name = re.sub('["]', '', ystockquote.get_company_name(symbol))
    price = ystockquote.get_last_trade_price(symbol)
    change = ystockquote.get_change_percent_change(symbol)
    change_realtime, dash, change_percent = change.split()
    change_realtime = re.sub('["]', '', change_realtime)
    change_percent = re.sub('["]', '', change_percent)

    if change_realtime > 0:
        status = 'gain'
    else:
        status = 'loss'

    today = datetime.today()
    offset = 10
    week = datetime.now() - timedelta(days=offset)
    history = ystockquote.get_historical_prices(symbol, week.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))

    return json.dumps({ 'symbol': symbol, 'name': name, 'price': price, 'change_realtime': change_realtime, 'change_percent': change_percent, 'status': status, 'history': history })
    pass

if __name__ == "__main__":
    app.run()
