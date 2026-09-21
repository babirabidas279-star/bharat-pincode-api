from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Vercel me /tmp folder me hi write kar sakte hain
DB_FILE = "/tmp/pincodes.db"

# No-COD pincodes list - Islands + JK + NE + Sensitive areas
NO_COD = [
    "744101","744102","744103","744104","744105","744106",  # Andaman
    "744107","744108","744109","744110","744111","744112",  # Andaman  
    "744201","744202","744203","744204","744205","744206",  # Nicobar
    "744207","744208","744209","744210","744211","744212",  # Nicobar
    "744301","744302","744303","744304","744305","744306",  # Nicobar
    "744307","744308","744309","744310","744311","744312",  # Nicobar
    "682001","682002","682003","682004","682005","682006",  # Lakshadweep
    "682007","682008","682009","682010","682011","682012",  # Lakshadweep
    "190001","190002","190003","190004","190005","190006",  # Srinagar
    "190007","190008","190009","190010","190011","190012",  # Srinagar
    "791001","791002","791003","791004","791005","791006"   # Arunachal
]

# State → RTO Code mapping
STATE_RTO = {
    "West Bengal": "WB", "Maharashtra": "MH", "Delhi": "DL", 
    "Karnataka": "KA", "Tamil Nadu": "TN", "Gujarat": "GJ",
    "Uttar Pradesh": "UP", "Rajasthan": "RJ", "Kerala": "KL",
    "Punjab": "PB", "Haryana": "HR", "Bihar": "BR", "Jharkhand": "JH"
}

# Metro/Tier1 cities = 2 din delivery
TIER1 = ["Mumbai","Delhi","Bangalore","Chennai","Kolkata","Hyderabad","Pune","Ahmedabad"]

def init_db():
    if os.path.exists(DB_FILE): return
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''CREATE TABLE pincodes 
                 (pincode TEXT PRIMARY KEY, city TEXT, state TEXT, district TEXT, zone TEXT)''')
    data = [
        ("713330","Asansol","West Bengal","Paschim Bardhaman","East"),
        ("400001","Mumbai","Maharashtra","Mumbai","West"),
        ("110001","Delhi","Delhi","Central Delhi","North"),
        ("560001","Bangalore","Karnataka","Bangalore Urban","South"),
        ("744101","Port Blair","Andaman and Nicobar Islands","South Andaman","East"),
        ("744301","Car Nicobar","Andaman and Nicobar Islands","Nicobar","East"),
        ("682001","Kavaratti","Lakshadweep","Lakshadweep","South")
    ]
    conn.executemany("INSERT INTO pincodes VALUES (?,?,?,?,?)", data)
    conn.commit(); conn.close()

@app.route("/")
def home():
    return jsonify({"api": "Bharat Pincode API", "status": "Live by Rudra", "docs": "/v1/pincode/713330"})

@app.route("/v1/pincode/<code>")
def get_pin(code):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('SELECT city,state,district,zone FROM pincodes WHERE pincode=?', (code,))
    row = cur.fetchone(); conn.close()
    if not row: return jsonify({"success":False,"error":"Not found"}), 404
    city,state,district,zone = row
    return jsonify({"success":True,"data":{
        "pincode":code,
        "city":city,
        "state":state,
        "district":district,
        "zone":zone,
        "cod_available":code not in NO_COD,
        "rto_code":f"{STATE_RTO.get(state,'XX')}01",
        "delivery_days":2 if city in TIER1 else 5
    }})

init_db()
if __name__ == '__main__': app.run()