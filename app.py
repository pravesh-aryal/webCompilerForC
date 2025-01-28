from flask import Flask, request
from flask import render_template
import subprocess


#grab the text from user and save to .c file program.c

    


#definition of output file
output_file = "program"

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/run/", methods=['GET', 'POST'])
def run_code():
    print("The code is running when the button is clicked.")
    c_file = "code.c"
    code = request.form['programByUser']
    with open('code.c', 'w') as f:
        f.write(code)

    #when runCode clicked
    try:
        subprocess.run(
            ["gcc", c_file, "-o", output_file],
            check = True
        )

        #run the compiled exec.
        result = subprocess.run(
            ["./" + output_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        #output string to be displayed to the user
        output_string = result.stdout.decode()

    except subprocess.CalledProcessError as e:
        output_string = "Compilation error: "

    return render_template("home.html", code_result = output_string)





#executes when user runs the code
# @app.route("/run")
# def run():
#     #need to create a file with the text provided by the user
