
from flask import Flask , render_template, session, request, redirect, url_for, jsonify
import psycopg2, hashlib, os

app = Flask(__name__) 
app.secret_key = os.urandom(24)

def fetchQueryResult(query, parameters):
    con = psycopg2.connect(
        database="bpoonpnh",
        user="bpoonpnh",
        password="Ghp8K45LAum643dO0wX8eFMtnjntZz5L",
        host="isabelle.db.elephantsql.com",
        port= '5432'
    )

    cur_object = con.cursor()

    cur_object.execute(query, parameters)

    result = cur_object.fetchall()

    return result

def executeQueryResult(query, parameters):
    con = psycopg2.connect(
        database="bpoonpnh",
        user="bpoonpnh",
        password="Ghp8K45LAum643dO0wX8eFMtnjntZz5L",
        host="isabelle.db.elephantsql.com",
        port= '5432'
    )

    cur_object = con.cursor()

    cur_object.execute(query, parameters)

    con.commit()

    return True

def getEncryptedPassword(password):
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hash_password = hash_object.hexdigest()
    return hash_password


@app.route('/')
def index():

    #print(fetchQueryResult("Select * from customer"))

    #print(getEncryptedPassword("deku"))




    return render_template('index.html')


@app.route('/signup' , methods = ['POST'])
def signup():
    email = request.form['email']
    cname = request.form['cname']
    password = request.form['password']

    enc_password = getEncryptedPassword(password)

    print(enc_password)

    query = "INSERT INTO customer (cName, st_address, city, state, zipcode, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s);"

    parameters = (cname, request.form['st_address'], request.form['city'], request.form['state'], request.form['zipcode'], email, enc_password)

    result = executeQueryResult(query, parameters)

    print(result)
    
    if result == True:
        print('Register Successful !')
        #Storing details in session variables.
        session['email'] = email
        session['username'] = cname
        session['loggedIn'] = True
        return jsonify({'flag' : 1})
    else:
        print("Registration Unsuccessful !")
        return jsonify({'flag' : 0})

@app.route('/login' , methods = ['POST'])
def login():
    email = request.form['email']
    password = request.form['password']   

    result = ["karthik", "rajkarthik9@gmail.com"]

    
    if not result == None:
        #Storing details in session variables.
        session['email'] = result[3]
        session['username'] = result[1]
        session['password'] = password
        session['loggedIn'] = True
        return jsonify({'flag' : 1})
    else: 
        return jsonify({'flag' : 0})

if __name__ == '__main__':
    app.run(debug = True)