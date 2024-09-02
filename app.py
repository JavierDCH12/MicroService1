from flask import Flask, request, jsonify

app =Flask(__name__)


#REGISTER
@app.route('/register', methods=['POST'])
def register():
    data=request.json
    username = data.get('username')
    passwd = data.get('password')
    
    return jsonify({'message':f'User {username} registered in successfully! '}), 201 #CREATED CODE 


#LOGIN
@app.route('/login', methods=['POST'])
def login():
    data=request.json
    
    username=data.get('username')
    passwd=data.get('password')
    
    return jsonify({'message' : f'User {username} logged in successfully" '}), 200 #SUCCESS CODE




#RUN APP
if __name__=="__main__":
    app.run(debug=True)
    