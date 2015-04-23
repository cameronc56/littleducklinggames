#!/usr/bin/env python
from bottle import *
import sqlite3
import hashlib, uuid
import json
import blowfish
import base64
import sendgrid
import os

app = default_app()
cryptoKey = os.environ["CRYPTOKEY"]
conn = sqlite3.connect('login.db')
c = conn.cursor()

#Users table
#c.execute("DROP TABLE Users")
#c.execute("CREATE TABLE Users (username text PRIMARY KEY, passwordHash text NOT Null, passwordSalt text, email text)")
#conn.commit()

################################################################################
@get('/')
def returnIndex():
	return template('index', get_url = app.get_url)
################################################################################
@get('/robots.txt')
def returnRobots():
	return static_file("robots.txt", root="")
################################################################################
@post('/newPost')
def newPost():
	d = request.json
	threadTitle = d["threadTitle"]
	threadBody = d["threadBody"]
	return json.dumps({"threadTitle": threadTitle, "threadBody": threadBody})
################################################################################
@post('/register')
def register():
	d = request.json
	username = d['username']
	password = d['password']
	email = d['email']
	conn = openConn()
	with conn:
		c = conn.cursor()
		if (c.execute("SELECT PasswordSalt, PasswordHash FROM Users WHERE Username = ?",(username,))).fetchone():
			return json.dumps({"error":'Username Taken'})
		else:
			salt = uuid.uuid4().hex
			hash = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
			c.execute("INSERT INTO Users(Username, PasswordHash, PasswordSalt, Email) VALUES(?,?,?,?)", (username, hash, salt, email))
			conn.commit()
			return json.dumps({"error":'Account Created'})
################################################################################
@post('/login')
def login():
	d = request.json
	username = d['username']
	password = d['password']
	conn = openConn()
	with conn:
		c = conn.cursor()
		query = (c.execute("SELECT PasswordHash, PasswordSalt FROM Users WHERE Username = ?",(username,))).fetchone()
		if query:
			DBhash = query[0]
			salt = query[1]
			hash = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
			if hash == DBhash:
				response.set_cookie("session", encode_session_str({"username" : username}))
				return json.dumps({"error":'Logged In'})
			else:
				return json.dumps({"error":'Invalid Credentials'})
		else:
			return json.dumps({"error":'Invalid Credentials'})
################################################################################
@post('/sendEmail')
def sendEmail():
	sendgridUsername = os.environ['USERNAME']
	sendgridPassword = os.environ['PASSWORD']
	d = request.json
	emailName = d['emailName']
	emailAddress = d['emailAddress']
	emailBody = d['emailBody']
	sg = sendgrid.SendGridClient(str(sendgridUsername), str(sendgridPassword))
	message = sendgrid.Mail()
	message.add_to('Cam C <admin@littleducklinggames.com>')
	message.set_subject('Message to the Admin')
	message.set_html('')
	message.set_text(emailBody)
	message.set_from(emailName + " <" + emailAddress + " ")
	status, msg = sg.send(message)
	return json.dumps({"status":status})
################################################################################
@post('/isFavoriteGame')
def isFavoriteGame():
	d = request.json
	username = d["username"]
	gameTitle = d["gameTitle"]
	conn = openConn()
	with conn:
		c = conn.cursor()
		isFavorite = (c.execute("SELECT GameTitle FROM FavoriteGames WHERE Username = ? AND GameTitle  = ?",(username, gameTitle))).fetchone()
		if isFavorite is not None:
			return json.dumps({"isFavorite":"true"})
		elif isFavorite is None:
			return json.dumps({"isFavorite":"false"})
################################################################################
@post('/getAllFavoriteGames')
def getAllFavoriteGames():
	d = request.json
	username = d["username"]
	conn = openConn()
	with conn:
		c = conn.cursor()
		favoriteGames = (c.execute("SELECT GameTitle FROM FavoriteGames WHERE Username = ?", (username, ))).fetchall()
		return json.dumps({"favoriteGames":favoriteGames})
################################################################################
@post('/favoriteGame')
def favoriteGame():
	d = request.json
	username = d["username"]
	gameTitle = d["gameTitle"]
	conn = openConn()
	with conn:
		c = conn.cursor()
		isFavorite = (c.execute("SELECT GameTitle FROM FavoriteGames WHERE Username = ? AND GameTitle  = ?",(username, gameTitle))).fetchone()
		if isFavorite is not None:
			(c.execute("DELETE FROM FavoriteGames WHERE Username = ? AND GameTitle = ?", (username, gameTitle))).fetchone()
		elif isFavorite is None:
			c.execute("INSERT INTO FavoriteGames(Username, GameTitle) VALUES (?, ?)", (username, gameTitle))
	conn.commit()
	return json.dumps({"response":"RESPONSE FROM SERVER"})
################################################################################
@post('/account')
def account():
	session = request.json['session']
	session = decode_session_str(session)
	if is_logged_in(session):
		username = session['username']
		conn = openConn()
		with conn:
			#c = conn.cursor()
			#email = (c.execute("SELECT Email FROM Users WHERE Username = ?",(username,))).fetchone()
			#email = email[0]
			#if(email == None):
			#	email = "No email attached to this Account"
			return json.dumps({"username":username})
	else:
		return json.dumps({"username":"Click To Login"})
################################################################################
@get('/static/js/<filename:re:.*\.js>', name='static/js')
def server_static(filename):
	return static_file(filename, root='static/js')
################################################################################
@get('/static/js/components/<filename:re:.*\.js>', name='static/js/components')
def server_static(filename):
	return static_file(filename, root='/static/js/components')
################################################################################
@get('/static/js/libraries/<filename:re:.*\.js>', name='static/js/libraries')
def server_static(filename):
	return static_file(filename, root='/static/js/libraries')
################################################################################
@get('/static/js/routers/<filename:re:.*\.js>', name='static/js/routers')
def server_static(filename):
	return static_file(filename, root='/static/js/routers')
################################################################################
@get('/static/json/<filename:re:.*\.json>', name='static')
def server_static(filename):
	return static_file(filename, root='static/json')
################################################################################
@get('/static/css/<filename:re:.*\.(css|css.map)>', name='static/css')
def server_static(filename):
	return static_file(filename, root='static/css')
################################################################################
@get('/static/fonts/<filename>')
def server_static(filename):
	return static_file(filename, root='static/fonts', mimetype = 'font/opentype')
################################################################################
@route('/images/<imageName>', name = 'images')
def send_image(imageName):
	return static_file(imageName, root = 'images', mimetype = 'image/png')
################################################################################
def decode_session_str(s):
	if s:
		return json.loads(blowfish.blowfishCTR("d", cryptoKey, base64.b64decode(s)))
	return None
################################################################################
def encode_session_str(d):
	return base64.b64encode(blowfish.blowfishCTR("e", cryptoKey, json.dumps(d)))
################################################################################
def is_logged_in(session):
	return type(session) is dict and session.has_key("username")
################################################################################
def openConn():
	return sqlite3.connect('login.db')
################################################################################
run(host = '0.0.0.0', port = 8443, debug = True, reloader = False)