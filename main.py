from flask import Flask, render_template



app = Flask(__name__)




@app.route("/")
def home():

    list_item = ["Assignment" , "Work" , "Physical Exercise", "Project1", "Project2" ,"Today's learning", "A good thing", "A bad thing", "Note"]


    return render_template("index.html", activities = list_item)









if __name__ == "__main__":

    app.run(debug= True)