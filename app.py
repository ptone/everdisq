import re

from flask import Flask, render_template, redirect, abort

from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form, TextField, ValidationError

app = Flask(__name__)

app.config['BOOTSTRAP_USE_MINIFIED'] = True
app.config['BOOTSTRAP_USE_CDN'] = True
app.config['BOOTSTRAP_FONTAWESOME'] = True
app.config['SECRET_KEY'] = 'devkey'

app.config.from_object(__name__)
app.config.from_envvar('FLASKAPP_SETTINGS', silent=True)

Bootstrap(app)


def valid_url(string):
    return re.match('http(s){0,1}://www.evernote.com/shard/.+',
           string, re.I) is not None


class URLForm(Form):
    url = TextField('Evernote share URL',
            description='Please enter Evernote share URL.')

    def validate_url(form, field):
            if not valid_url(field.data):
                raise ValidationError('This does not appear to be ' /
                        'a valid Evernote Share URL')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url = form.url.data
        return redirect("/note/{}".format(url))

    return render_template('index.html',
            form=form,
            )


@app.route('/note/<path:noteurl>/')
def view_note(noteurl):
    print noteurl
    if not valid_url(noteurl):
        abort(404)
    return render_template('view.html', url=noteurl)

if '__main__' == __name__:
    app.run(debug=True, host='0.0.0.0', port=80)
