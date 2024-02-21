from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send
import random
from string import ascii_uppercase
'''have to add client data'''


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
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("tempface.html", error="Room wa shindeiru")
        
        if join != False and not code:
            return render_template("tempface.html", error="mf enter a goddamn code")
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members":0, "messages":[]}
        elif code not in rooms:
            return render_template("tempface.html", error="No room", code=code, name=name)
    
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))
    
    return render_template("tempface.html")

@app.route("/chat")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))
    
    return render_template("chat.html", code=room, messages=rooms[room]["messages"])

@sio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return 
    
    join_room(room)
    send({"message": "welcome", "name": name}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@sio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left"}, to=room)
    print(f"{name} left the room {room}")
    
@sio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    
    content = {
        "name" : session.get("name"),
        "message": data["data"]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get("name")} said: {data['data']}")

if __name__ == "__main__":
    sio.run(app, port='8000', debug=True)