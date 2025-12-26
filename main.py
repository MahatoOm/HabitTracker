from flask import Flask, render_template, request, redirect, url_for , flash
import jsonify
from datetime import datetime , timedelta , date
# System files
import database as database
# toast message
# from flask_toastr import Toastr
# toastr = Toastr()
SECRET_Key = "rtghajkrsfljhsklf"
import time

app = Flask(__name__)
app.secret_key = "rtghajkrsfljhsklf"

@app.route("/")
def home(username = 'Admin'):
    list_item = ["Assignment" , "Work" , "Physical Exercise", "Project1", "Project2" ,"Today's learning", "A good thing", "A bad thing", "Note"]
    
    todays_date = date.today()
    totalweek = []
    if database.find_username:
        for i in range(4, -1, -1):
            day = str(todays_date - timedelta(i))
            docs = database.find_by_date("om", day)

            day_data = {}

            for d in docs:
                day_data[d["habit"]] = {
                    "status": d["data"].get("status", ""),
                    "note": d["data"].get("note", "")
                }

            totalweek.append({
                "date": day,
                "habits": day_data
            })

    print(totalweek)
      

    return render_template("index.html", activities = list_item , totalweekdata = totalweek)
    


@app.route("/submitTracker", methods = ["POST" ])
def habit():
    
    payload = request.get_json()
    

    start_date = payload["start_date"]
    changes = payload["changes"]
    print(start_date)
    print(changes)

    date_format = '%Y-%m-%d'
    start_date  = datetime.strptime(start_date , date_format).date()
    save_cell(changes , start_date)
    # upload_data("om" , )
    return home()

def save_cell(changes , startdate):
    print("Save cell called")
    for habit, value1 in changes.items():

        for afterdate , value2 in value1.items():
            # print("om", habit, startdate + timedelta( int(afterdate)) , value2)
            upload_data("om", habit,  startdate , str(startdate + timedelta(int(afterdate))) , value2)
    return 

def upload_data(username , habit, upload_date ,event_date, data):
    print("upload cell called")
    res = database.save_habit(username, habit, upload_date , event_date, data)
    print(res , 'sucessfull')
    return 

import user
key = '000000'
username = ''
@app.route('/login' , methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form["Name"]
        email = request.form['Email']
        print(username, email)
        # key = user.userlogin()
        return render_template("entercode.html")
    return render_template("login.html")

@app.route('/entercode' , methods = ['POST', 'GET'])
def code():
    if request.method == "POST" :
        userinput = request.form['enteredcode']
        print(userinput)
        if userinput == key:
            print(username)
            print(key)
            flash("Account created Sucessfully.")
            time.sleep()
            return home(username)
        else:
            flash("Input Mismatched Try Again" )
            return render_template("entercode.html")
            

    return render_template("entercode.html")

if __name__ == "__main__":

    app.run(debug= True)