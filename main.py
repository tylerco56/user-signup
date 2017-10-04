from flask import Flask, request, redirect, render_template

app = Flask(__name__)

app.config['DEBUG'] = True 

@app.route("/")
def index():
    return render_template("user_signup.html")

def count_space(word):
    for letter in word:
        if letter.isspace():
            return True
    return False

def count_at(word):
    for letter in word:
        if letter == "@":
            return True
    return False

def count_period(word):
    for letter in word:
        if letter == ".":
            return True
    return False

@app.route("/", methods=['POST'])
def validate():
    username = request.form["username"]
    password = request.form['password']
    verify_password = request.form['verify-password']
    email = request.form["email"]

    username_error = ""
    username_error_flag = False
    password_error = ""
    verify_password_error = ""
    erase_passwords = False
    email_error = ""
    email_error_flag = False

    if not username:
        username_error = "Please Enter an User Name."
        username_error_flag = True

    if count_space(username):
        username_error = "Username must not contain spaces."

    if not username_error_flag:    
        if len(username) < 3 or len(username) > 20:
            username_error = "Username must be 3 - 20 characters"

    if not password:
        password_error = "Please Enter a Password."

    if count_space(password):
        password_error = "Password must not contain spaces."
        erase_passwords = True

    if len(password) < 3 or len(password) > 20:
        password_error = "Password must be 3 - 20 characters"
        erase_passwords = True
    
    if not verify_password:
        verify_password_error = "Please Enter Another Password to Verify."
        erase_passwords = True

    if count_space(verify_password):
        verify_password_error = "Password must not contain spaces."
        erase_passwords = True

    if len(verify_password) < 3 or len(verify_password) > 20:
        verify_password_error = "Password must be 3 - 20 characters"
        erase_passwords = True

    if not password == verify_password:
        password_error = "Your passwords do not match."
        verify_password_error = "Your passwords do not match."
        erase_passwords = True

    if erase_passwords:
        password = ""
        verify_password = ""

    if count_space(email):
        email_error = "Email may not contain spaces."
        email_error_flag = True

    if (email and not email_error_flag) and (len(email) < 3 or len(email) > 20):
        email_error = "Email must be 3 - 20 characters."
    
    if (email and not email_error_flag) and (not count_at(email) or not count_period(email)):
        email_error = "Email must contain a @ and .", email_error_flag

    if not username_error and not password_error and not verify_password_error and not email_error:
        return redirect('/welcome-page?username=' + username)
    else:
        return render_template("user_signup.html",username=username, password=password, verify_password=verify_password, email=email, username_error=username_error, password_error=password_error, verify_password_error=verify_password_error, email_error=email_error)

@app.route("/welcome-page")
def valid_signup():
    username = request.args.get("username")
    return render_template("welcome.html", username=username)


app.run()
