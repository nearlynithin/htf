from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, join_room, leave_room, send
import random
from string import ascii_uppercase

'''have to add client data'''

app = Flask(__name__)
app.config["SECRET_KEY"] = "ThisIsForTheRuntimeERROR"
sio = SocketIO(app)

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

@app.route("/", methods=['POST', 'GET'])
def chat():
    session.clear()
    room = generate_unique_code(4)
    rooms[room] = {"members":0, "messages":[]}

    session["room"] = room
    
    return render_template("chat.html")

@sio.on("connect")
def connect(auth):
    room = session.get("room")
    if not room:
        return
    if room not in rooms:
        leave_room(room)
        return 
    
    join_room(room)
    send({"message": "welcome"}, to=room)
    rooms[room]["members"] += 1
    print(f"joined room {room}")

@sio.on("disconnect")
def disconnect():
    room = session.get("room")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    print(f"left the room {room}")
    
@sio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    
    content = {
        "message": data["data"]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{data['data']}")

if __name__ == "__main__":
    sio.run(app, port='8000', debug=True)