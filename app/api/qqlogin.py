import random
import urllib
import urllib2
import json
from flask import session

class QQLogin(object):

	app_id = '100397745'
	app_key = '673dbdf46fa7a0f8debb6a7fca5fe3dc'
	get_auth_code_url = "https://graph.qq.com/oauth2.0/authorize"
	get_access_token_url = "https://graph.qq.com/oauth2.0/token"
	get_openid_url = "https://graph.qq.com/oauth2.0/me"
	get_user_info_url = 'https://graph.qq.com/user/get_user_info'

	def login(self):
		args = {
			'response_type': 'code',
			'client_id': self.app_id,
			'redirect_uri': 'http://www.v5snj.com/connect/callback/qq',
			'state': str(random.random()),
			'scope': ''
		}

		session['qqlogin_status'] = args['state']

		login_url = self.get_auth_code_url + '?' + urllib.urlencode(args)

		return login_url

	def login_callback(self, request):
		code = request.args.get('code')
		state = request.args.get('state')

		# if state != session.pop('qqlogin_status', None):
		# 	return None

		args = {
			'grant_type': 'authorization_code',
			'client_id': self.app_id,
			'redirect_uri': 'http://www.v5snj.com/connect/callback/qq',
			'client_secret': self.app_key,
			'code': code
		}

		token_url = self.get_access_token_url + '?' + urllib.urlencode(args)
		res = self.get(token_url)
		access_token = res.split('&')[0].split('=')[1]

		openid_url = self.get_openid_url + '?access_token=' + access_token
		res = self.get(openid_url)
		res = res.split('"')
		openid = res[7]
		
		args = {
			'access_token': access_token,
			'oauth_consumer_key': self.app_id,
			'openid': openid
		}
		userinfo_url = self.get_user_info_url + '?' + urllib.urlencode(args)
		res = self.get(userinfo_url)
		userinfo = json.loads(res)

		return {'access_token': access_token, 'openid': openid, 'userinfo': userinfo}

	def get(self, url):
		return urllib2.urlopen(url).read()





