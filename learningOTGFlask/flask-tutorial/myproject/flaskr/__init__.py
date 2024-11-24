import os

from flask import Flask

#application factory
def create_app(test_config = None):

    app = Flask(__name__, instance_relative_config=True)
    from . import db
    db.init_app(app)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        #load the isntance config if it exits
        app.config.from_pyfile('config.py', silent=True)

    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)

    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return "Hello world"

    @app.route('/home')
    def home():
        return "THIS IS THE HOME PAGE"
    @app.route('/<name>')
    def suyog(name):

        # return "<h1 style='background-color:DodgerBlue'> Suyong randi ko ban ho muji bhode khate sala </h1>"
        return """<marquee>
            <h1 style="background-color:DodgerBlue; text-align:center"> {name=name} </h1>
            </marquee>
        """
        return """
 <html>
<head>
    <title>SUYOG Fullscreen</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background-color: black;
        }

        h1 {
            font-size: 100px;
            font-weight: bold;
            text-align: center;
            color: white;
            text-shadow: 2px 2px 4px black;
            animation: colorChange 5s infinite alternate;
        }

        @keyframes colorChange {
            0% { color: red; }
            25% { color: green; }
            50% { color: blue; }
            75% { color: yellow; }
            100% { color: purple; }
        }
    </style>
</head>
<body>
    <h1>SUYOG</h1>
</body>
</html>
"""

    from . import auth
    app.register_blueprint(auth.bp)
    return app


