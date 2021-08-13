this_file = "venv/bin/activate_this.py"

exec(open(this_file).read(), {"__file__": this_file})


from flask import Flask, render_template, send_file


application = Flask(__name__)


# Config options - Make sure you created a 'config.py' file.

# application.config.from_object('config')

# To get one variable, tape app.config['MY_VARIABLE']


@application.route("/tiles/<zoom>/<x>/<y>/")
def tiles(zoom, y, x):

    default = "tiles\\default.png"

    filename = "tiles\\%s\\%s\\%s.png" % (zoom, x, y)

    return send_file(filename)

    """

    if os.path.isfile(filename):

        return send_file(filename)

    else:

        return send_file(default)

    """


@application.route("/")
def index():

    return render_template("index.html")


@application.route("/export/")
def export():

    return send_file()
