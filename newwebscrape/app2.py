from bs4 import BeautifulSoup
from flask import Flask, redirect, jsonify, request, url_for, render_template, flash,make_response,url_for
import os
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO,send
PEOPLE_FOLDER = os.path.join('static', 'people_photo')

app = Flask(__name__) 


file = open("C:/Users/ashok/Downloads/flood.html","r")

file_text = file.read()

parsed_html = BeautifulSoup(file_text, 'html.parser')

Present_Water_Level=parsed_html.find_all('div',class_='wl')

current_water_level=Present_Water_Level[0].text.strip()

curent_Water_Level=float(current_water_level)

print("curent_Water_Level=",current_water_level)

print("Warning_Level= 32.68")

print("Danger_Level= 33.68")

print("Highest_Flood_Level=34.72")


app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
@app.route('/index1')
def show_index1():
  full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'bgplogo.png')
  
  return render_template("index1.html", user_image = full_filename,variable=current_water_level,)
  
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index1.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
    
        


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='people_photo/' + filename), code=301)


@app.route('/chat1')
def chat1():
    return (render_template('chat1.html'))

def messageRecived():
  print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json, callback=messageRecived )

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
        socketio.run(app)
        
    
