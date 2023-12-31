from flask import Flask,render_template,request,redirect,url_for


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/save_data', methods=['GET'])
def save_data():
    regno = request.args['regno']
    name= request.args['name']
    standard = request.args['class']
    math = request.args['math']
    science = request.args['science']
    computer = request.args['computer']
    print(regno,name,standard,math,science,computer)
    
    return redirect(url_for('home'))

app.run()