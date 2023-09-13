from flask import Flask, render_template
from flask_socketio import SocketIO
import json
from flask import request, Response
from flask_cors import CORS
from raven_real_time import Raven

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='http://104.131.126.10:1000')



#  Send Notification API

raven = Raven()

@app.route('/api/search', methods=['POST'])
def test():
    
    CATEGORY = request.json['CATEGORY']
    SOURCE_NAME = request.json['SOURCE_NAME']
    SEARCH_STRING = request.json['SEARCH_STRING']
    ENTITY_NAME = request.json['ENTITY_NAME']
    TOPIC = request.json['TOPIC']
    GROUP = request.json['GROUP']
    TYPE = request.json['TYPE']
    FACT_LEVEL = request.json['FACT_LEVEL']
  

    raven.raven_pack(SEARCH_STRING,ENTITY_NAME,TOPIC,GROUP,
                            TYPE,
                            FACT_LEVEL,
                            CATEGORY,
                            SOURCE_NAME)

    # return Response(response='hihi', status=200)


@app.route('/api/send', methods=['POST'])
def test_emit():

    data = {
        'TIMESTAMP_UTC': request.json['TIMESTAMP_UTC'],
        'ENTITY_NAME': request.json['ENTITY_NAME'],
        'TOPIC': request.json['TOPIC'],
        'GROUP': request.json['GROUP'],
        'TYPE': request.json['TYPE'],
        'EVENT_SENTIMENT_SCORE': request.json['EVENT_SENTIMENT_SCORE'],
        'EVENT_RELEVANCE': request.json['EVENT_RELEVANCE'],
        'FACT_LEVEL': request.json['FACT_LEVEL'],
        'CATEGORY': request.json['CATEGORY'],
        'SOURCE_NAME': request.json['SOURCE_NAME'],
        'HEADLINE': request.json['HEADLINE'],

                    }

    socketio.emit('notification', data)

    res = json.dumps(data)

    return Response(response=res, status=200, content_type="application/json")

    # return Response(response='hihi', status=200)




# app.post('/send-notification', (req, res) => {
#     const notify = {data: req.body};
#     socket.emit('notification', notify); // Updates Live Notification
#     res.send(notify);
# });



if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True, port=5200)