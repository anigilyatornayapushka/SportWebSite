import flask


app: flask.Flask = flask.Flask(__name__)


@app.get('/')
def homepage():
	return flask.render_template('information_pages/homepage.html')


@app.get('/privacy-policy/')
def privacy_policy():
	return flask.render_template('information_pages/privacy-policy.html')


@app.get('/terms-of-use/')
def terms_of_use():
	return flask.render_template('information_pages/terms-of-use.html')


@app.get('/faq/')
def faq():
	return flask.render_template('information_pages/faq.html')


@app.get('/profile/')
def profile():
	return flask.render_template('auths/profile.html')


@app.get('/login/')
def login():
	return flask.render_template('auths/login.html')


@app.get('/register/')
def register():
	return flask.render_template('auths/register.html')


@app.get('/restore-password/')
def restore_password():
	return flask.render_template('auths/restore-password.html')


@app.get('/change-password/')
def change_password():
	return flask.render_template('auths/change-password.html')


if __name__ == '__main__':
	app.run(host='localhost', port=5000, debug=True)
