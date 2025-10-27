from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")  # Povolit přístup z libovolné URL

# Uložíme polohy hráčů {player_id: {'lat':..., 'lon':...}}
players = {}

@app.route('/')
def index():
    return render_template('map.html')

# Přijímání dat od hráčů
@socketio.on('update_position')
def handle_update(data):
    player_id = data.get('player_id')
    if player_id:
        players[player_id] = {
            'lat': data.get('lat'),
            'lon': data.get('lon'),
            'speed': data.get('speed'),
            'cargo': data.get('cargo'),
            'truck_brand': data.get('truck_brand', '–'),
            'truck_model': data.get('truck_model', '–')
        }
        emit('positions', players, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
    
@socketio.on('goodbye', namespace='/')
def handle_goodbye(data):
    player_id = data.get('player_id')
    if player_id and player_id in players:
        players.pop(player_id)
        emit('positions', players, broadcast=True, namespace='/')

