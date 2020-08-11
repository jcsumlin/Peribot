import os
import sqlite3
from functools import wraps

from flask import Flask, redirect, url_for, render_template, g, flash
from flask import request
from flask_discord import DiscordOAuth2Session, exceptions
from flask_wtf import FlaskForm, CsrfProtect
from flask_wtf.csrf import CSRFError
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['FLASK_DEBUG'] = '1'

app = Flask(__name__)
app.config.from_object(__name__)
csrf = CsrfProtect(app)

app.secret_key = b"random bytes representing flask secret key"

app.config["DISCORD_CLIENT_ID"] = 0  # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = ""  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = ""  # Redirect URI.

discord = DiscordOAuth2Session(app)


def query_db(query, req_type="GET", args=(), one=False):
    try:
        if req_type == "GET":
            cur = g.db.execute(query, args)
            rv = [dict((cur.description[idx][0], value)
                       for idx, value in enumerate(row)) for row in cur.fetchall()]
            return (rv[0] if rv else None) if one else rv
        elif req_type == "PUT":
            g.db.execute(query, args)
            g.db.commit()
    except sqlite3.Error as error:
        flash("Failed to update sqlite table", error)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            discord.fetch_user()
        except exceptions.Unauthorized:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def before_request():
    g.db = sqlite3.connect("cogs/peribot.db")
    g.db.row_factory = sqlite3.Row
    try:
        g.user = discord.fetch_user()
    except Exception:
        pass


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.errorhandler(CSRFError)
def csrf_error(reason):
    return render_template('error.html', reason=reason)

@app.route("/logout/")
def logout():
    discord.revoke()
    return redirect(url_for("index"))


@app.route("/login/")
def login():
    return discord.create_session()

@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for(".me"))


def save_settings(prefix, server_id):
    return query_db(f"UPDATE server_settings SET prefix = ? WHERE server_id = {server_id};", req_type="PUT", args=prefix)


def find_server(server_id):
    servers = discord.fetch_guilds()
    for a_server in servers:
        if a_server.id == server_id:
            return a_server


@app.route("/server/<int:server_id>", methods=['GET', 'POST'])
@login_required
def server(server_id):
    form = ServerSettings()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.', 'error')
            return redirect(url_for(".me"))
        else:
            save_settings(form.prefix.data, server_id)
            flash("Successfully Saved!", 'success')
    this_server = find_server(server_id)
    server = query_db(f"SELECT * FROM server_settings WHERE server_id = {server_id}")
    if len(server) > 0:
        server = server[0]
    else:
        flash("Peribot is not on this server! Please invite it", "info")
        return redirect(url_for('.me'))
    server['data'] = this_server
    user = discord.fetch_user()
    return render_template('single_server.html',
                           logged_in=True,
                           display_subnav=True,
                           user=user,
                           server=server,
                           form=form,
                           header="Server Settings | " + server['server_name'])


@app.route("/server/")
@login_required
def me():
    g.user = discord.fetch_user()
    can_add_servers = []
    servers = discord.fetch_guilds()
    for server in servers:
        if server.permissions_value & 0x20 != 0:
            can_add_servers.append(server)
    return render_template('dashboard.html',  logged_in=True, display_subnav=False, user=g.user, servers=can_add_servers, header="Dashboard")


@app.route("/")
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error="404! Page Not Found!", msg=error), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template('error.html', error="500! Internal Server Error", msg=error), 500


class ServerSettings(FlaskForm):
    prefix = StringField('Prefix:', validators=[DataRequired()])
    save = SubmitField('Save')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80" )
