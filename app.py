from flask import Flask, render_template, request, redirect, url_for , flash , jsonify ,session
import sqlite3
import bcrypt
from flask_session import Session
from maip_client import MaipClient
from maip_context import MaipContext
from datetime import datetime
from maip_builder import MaipBuilder


app = Flask(__name__)
app.config['SECRET_KEY'] = 'halohalohalo123'   

DATABASE = 'users_info.db'
CHAT_DATABASE = 'chat.db'

app.config["SESSION_PERMANENT"]=False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)




#It provides to hash to password.
def generate_password_hash(password):
    salt=bcrypt.gensalt()
    hashed=bcrypt.hashpw(password.encode(),salt)
    return hashed,salt


def connect_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def connect_chat_db():
    conn = sqlite3.connect(CHAT_DATABASE)
    return conn


#Chat için TABLO YOKSA OLUŞTURUR !
def Create_Tables_Chat():
    conn=connect_chat_db()
    cursor=conn.cursor()
    cursor.execute('''
             CREATE TABLE IF NOT EXISTS chat (
                   user_id INTEGER,
                   message TEXT NOT NULL,   
                   CTXID INTEGER NOT NULL,
                   ROLE  TEXT NOT NULL,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                   )      
                   
    ''')  

    conn.commit()
    conn.close()


#Chat için DATABASE'e CHATİ kayıt eder.
def Save_Chat(user_id, message, context_id, role):
    conn=connect_chat_db()
    cursor=conn.cursor()
    
    cursor.execute('''

        INSERT INTO chat (user_id, message, CTXID, role)
        VALUES (?,?,?,?)
    
''',(user_id, message, context_id, role))
    
    conn.commit()
    conn.close()



#Kullanıcının chat'e yazdığı mesaj şu anda user_messsage'nın içinde duruyor. Bunu Client kısmına atmamız gerekiyor.
@app.route('/new_chat', methods=['POST'])
def submit():
                  
    data= request.json
    user_message=data.get('user_message')
    user_id =session.get('user_id')
    generatedContext = None
    if session['csid'] and session['clid']:
        tmpMaipClient = MaipClient("ip address", port, session['csid'], session['clid'])
        generatedContext = MaipContext(tmpMaipClient, session['ctxid'], session['active_model'])

        session["messages"].append({"User" : user_message})
        tmpMessageId = generatedContext.set_input("User", user_message)
        if tmpMessageId == 0:
            session['msgids'] = []
            generatedContext.reactivate_context()
            for messageDict in session["messages"]:
                for msgRole, msgContent in messageDict.items():
                    tmpMessageId = generatedContext.set_input(msgRole, msgContent)
                    session['msgids'].append(tmpMessageId)
        else:
            session['msgids'].append(tmpMessageId)

        Save_Chat(user_id, user_message, session['ctxid'], "User")
    else:
        return render_template('sign_up.html')

    words=""

    #Tek tek kelimeyi alıp arayüze gönderir.
    bot_message_status_code=generatedContext.execute_input(session["msgids"])
    words += bot_message_status_code[0]
    while True:
        bot_message_status_code= generatedContext.get_next()
        status_code = bot_message_status_code[1]
        if status_code != some_status_code: #It is classified information
            break
        
        word = bot_message_status_code[0]
        words += word

    session["messages"].append({"Assistant" : words})
    session["msgids"].append(generatedContext.set_input("Assistant", words))
    Create_Tables_Chat()
    Save_Chat(user_id, words, generatedContext.get_CTXID() , "Assistant")


    return jsonify({
        "message": "Veri alindi",
        "User_message": user_message,
        "Bot_message": words
    }), 200

# Anasayfa
@app.route('/')
def home():
    return render_template('main.html')


@app.route('/user-home')
def user_home():
    return render_template('user_home.html')

@app.route('/new_chat')
def home_to_chat():
    Create_Tables_Chat()
    if session['clid']:
        tmpMaipClient = MaipClient("ip address", port, session['csid'], session['clid'])
        programModel = tmpMaipClient.get_program_models()
        myModels = tmpMaipClient.get_model_list()
        activeModel = ""
        if len(myModels):
            activeModel = myModels[0]
            pass
        else:
            tmpMaipClient.acquire_model(programModel[0])
            activeModel = programModel[0]
        session['msgids'] = []
        session['messages'] = []
        generatedContext = tmpMaipClient.create_context(activeModel, 7000)
        session['ctxid'] = generatedContext.get_CTXID()
        session['messages'].append({"System" : "You are a helpful assistant."})
        session['active_model'] = activeModel
        session['msgids'].append(generatedContext.set_input("System","You are a helpful assistant."))
        user_id =session.get('user_id')
        Save_Chat(user_id, "You are a helpful Assistant.", session['ctxid'], "System")
    else:
        return render_template('sign_up.html') 
    return render_template('new_chat.html')



@app.route('/sign_in' , methods=['GET'])
def home_to_sign_in():
    return render_template('sign_in.html')

@app.route('/logout')
def log_out():
    print("Session temizlendi.")
    session.clear()
    print(f"Current session data:{session}")
    return redirect(url_for('home'))



@app.route('/sign_up' , methods=['GET'])
def home_to_sign_up():
    return render_template('sign_up.html')


# Sign Up sayfası
@app.route('/sign_up', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username_input']
        password = request.form['password_input']
        email = request.form['email_input']

        
        hash_total=generate_password_hash(password)
    

        conn = connect_db()
        cursor =conn.cursor() 
        cursor.execute('''    
                       
        CREATE TABLE IF NOT EXISTS users_info (
              id integer PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE NOT NULL,
              password TEXT NOT NULL,
              pass_salt TEXT NOT NULL,
              email TEXT UNIQUE NOT NULL,
              CSID integer UNIQUE,
              CLID integer UNIQUE                                    
                )  
        ''')
        conn.commit()

        tmpClient = MaipClient("ip address",port)

        tmpClient.create_client()
        CSID=tmpClient.get_CSID()
        CLID=tmpClient.get_CLID()

        cursor.execute('''
                INSERT INTO users_info(username,password,pass_salt,email,CSID,CLID)
                VALUES (?,?,?,?,?,?)
        ''',(username,hash_total[0],hash_total[1],email,CSID,CLID)) #Bilgileri database'e girer.

        conn.commit() 
        conn.close() 


        session['csid'] = CSID
        session['clid'] = CLID
        session['username'] = username #OTURUMU BAŞLATIR ......
        
        #Verileri txt'ye yazar.
        with open('users.txt', 'a') as file:
            file.write(f'Username: {username}, Password: {hash_total[0]}, Email: {email}\n')

        return redirect(url_for('user_home'))
    return render_template('sign_up.html')


@app.route('/sign_in', methods=['POST'])
def Sign_In():
    
    if request.method =='POST':
        username = request.form['username_input']
        password = request.form['password_input']


        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users_info WHERE username = ?',(username,))
        user=cursor.fetchone()
       

        if user and bcrypt.checkpw(password.encode(),user[2]):
            session['csid'] = user[5]
            session['clid'] = user[6]
            session['username']=username
            session['user_id'] = user[0] #user_id'yi oturuma kayıt ediyoruz.
            conn.close() #database kapatılır.
            print(f"GİRİŞ YAPTIK - Username: {session['username']}, User ID: {session['user_id']}")
            return redirect(url_for('user_home'))
        else:
            print("ERRORRRRRRRR ")
            return redirect(url_for('main'))
        
    return render_template('sign_in.html')    


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=0000, debug=True) #burayı değiştirdim.
    app.run(debug=True)
