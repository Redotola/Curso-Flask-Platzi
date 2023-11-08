from flask import Flask, request, make_response, redirect

app = Flask(__name__) # the app name is the name of the current file

@app.route('/') # route of the function is working
def index():
    
    user_ip = request.remote_addr # obtain the ip of the user
    response = make_response(redirect('/hello')) # the index redirect to 'hello' route
    response.set_cookie("user_ip", user_ip) # set the cookie in the browser with a name
    return response
    
@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip') # obtain the cookie from the browser
    return f"Hello World Platzi, tu IP es {user_ip}"

if __name__ == "__main__": # if the file is explicit execute the server run
    app.run(port = 5500, host = "0.0.0.0", debug = True)
