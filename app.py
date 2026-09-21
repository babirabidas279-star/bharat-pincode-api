from flask import Flask, jsonify
import sqlite3, os
app = Flask(__name__)
DB_FILE = 'bharat_pincode.db'
NO_COD = {'744101','793001','790001','795001','796001'}
STATE_RTO = {'West Bengal':'WB','Maharashtra':'MH','Delhi':'DL','Karnataka':'KA','Tamil Nadu':'TN'}
TIER1 = {'Mumbai','Delhi','Bangalore','Chennai','Kolkata','Hyderabad','Pune'}

def init_db():
    if os.path.exists(DB_FILE): return
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('CREATE TABLE pincodes (pincode TEXT PRIMARY KEY, city TEXT, state TEXT, district TEXT, zone TEXT)')
    data = [('713330','Asansol','West Bengal','Paschim Bardhaman','East'),
            ('110001','New Delhi','Delhi','Central Delhi','North'),
            ('400001','Mumbai','Maharashtra','Mumbai','West'),
            ('744101','Port Blair','Andaman','South Andaman','East')]
    cur.executemany('INSERT INTO pincodes VALUES (?,?,?,?,?)', data)
    conn.commit(); conn.close()

@app.route('/')
def home(): return jsonify({"api":"Bharat Pincode API","status":"Live by Rudra"})

@app.route('/v1/pincode/<code>')
def get_pin(code):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('SELECT city,state,district,zone FROM pincodes WHERE pincode=?', (code,))
    row = cur.fetchone(); conn.close()
    if not row: return jsonify({"success":False,"error":"Not found"}),404
    city,state,district,zone=row
    return jsonify({"success":True,"data":{"pincode":code,"city":city,"state":state,"district":district,"zone":zone,"cod_available":code not in NO_COD,"rto_code":f"{STATE_RTO.get(state,'XX')}01","delivery_days":2 if city in TIER1 else 5}})

init_db()
if __name__ == '__main__': app.run()