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

key = '000000'
username = ''
email = ''
keys =[]
data = {}
start_date = ''

@app.route("/habitTracker", defaults={"username": "Friend", "email": ""})
@app.route("/habitTracker/<username>/<email>")
def habitTracker(username, email):
    
    print(username, email)
    list_item = ["Assignment" , "Work" , "Physical Exercise", "Project1", "Project2" ,"Today's learning", "A good thing", "A bad thing", "Note"]

    
    todays_date = date.today()
    totalweek = []
    print("in tracker",username, email)

    if email != "":
        for i in range(4, -1, -1):
            day = str(todays_date - timedelta(i))
            docs = database.find_by_date(email, day)

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
    print(username, email)
    print(totalweek)
    return render_template("habithomepage.html", activities = list_item , totalweekdata = totalweek, username = username, email = email)
    


@app.route("/submitTracker", methods = ["POST", "GET" ])
def habit():
    print("THE HABIT IS CALLED")

    global data, start_date
    
    payload = request.get_json()
    start_date = payload["start_date"]
    changes = payload["changes"]
    # print(start_date)
    # print(changes)

    date_format = '%Y-%m-%d'
    start_date  = datetime.strptime(start_date , date_format).date()

    data = changes

    print("Log of a day " , data , email)

    print(email )
    print(email  == "")
    if   email == '' :
        
        return render_template('login.html')
    
    else:
        save_cell(username ,email, changes , start_date)    
    return redirect(url_for('habitTracker' , username = username ,email = email))

def save_cell(username ,email, changes , startdate):
    print("Save cell called")
    for habit, value1 in changes.items():

        for afterdate , value2 in value1.items():
            # print("om", habit, startdate + timedelta( int(afterdate)) , value2)
            upload_data(username ,email, habit,  startdate , str(startdate + timedelta(int(afterdate))) , value2)
    return 

def upload_data(username ,email , habit, upload_date ,event_date, data):
    # print("upload cell called")   
    res = database.save_habit(username ,email, habit, upload_date , event_date, data)
    # print(res , 'sucessfull')
    return 


import user
@app.route('/login' , methods = ['POST', 'GET'])
def login():
    global username, email
    if request.method == "POST":
        username = request.form["Name"]
        email = request.form['Email']
        # print(username, email)
        key_value = user.userlogin(email)
        global key
        key = key_value
        print(key, "in login")
        print(type(key))
        # print(keys)
        return render_template("entercode.html" )
    else:
        return render_template("login.html")


@app.route('/entercode' , methods = ['POST', 'GET'])
def code():
    global username, email
    if request.method == "POST" :
        userinput = request.form['enteredcode']
        print(userinput)
        global key
        print(key ,"in code")
        print(type(userinput) , userinput, key)
        if int(userinput) == key:
            database.add_user(username, email)
            # print(username)
            # print(key)
            flash("Account created Sucessfully.")

            if data:
                print(data  , " in the code function.")
                save_cell(username, email, data , start_date)
            time.sleep(.5)
            print("in code",username, email)
            return redirect(url_for('habitTracker' , username = username , email = email))
            # return habitTracker(username , email)
        
        else:
            flash("Input Mismatched Try Again" )
            return render_template("entercode.html")
    else:            
        return render_template("entercode.html")


if __name__ == "__main__":
    app.run(debug= True)