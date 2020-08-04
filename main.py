from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    send_from_directory,
    flash,
    session,
)
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd
from ServeClient import serve

app = Flask(__name__)
app.config["SECRET_KEY"] = "nyu"


class FileForm(FlaskForm):
    file = FileField()
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    form = FileForm()
    if form.validate():
        analysis = serve(request.files["file"])
        if analysis == -1:
            flash(
                "This file didn't work. Make sure you're submitting the .csv version of the official excel sheet."
            )
            return redirect(url_for("index"))
        else:
            # the file analysis.pdf was written to the /tmp directory
            return send_from_directory("/tmp", filename="analysis.pdf", as_attachment=True)
    return render_template("index.html", form=form)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

