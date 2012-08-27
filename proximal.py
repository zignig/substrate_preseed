#!/usr/bin/python
import web
import redis,urllib2,string,os,json

conf = json.load(open('proximal.conf'))
print conf
try:
	os.stat('cache')
except:
	os.mkdir('cache')

r = redis.Redis(conf['redis'],db=2)

urls = (
	'/debian/pool/(.*)', 'pool',
	'/debian/dists/(.*)', 'dist',
	'/postinstall','postinstall',
	'/firstboot','firstboot',
	'/d-i/(.*)','preseed',
	'/','front_page'
	)

app = web.application(urls, globals())
proxy = conf['mirror']
render = web.template.render('templates')
password = conf['password'] 
ttl = 86400

class front_page:
	def GET(self):
		#return render.wheezy(password,proxy)
		return web.ctx.host

class pool:        
	def GET(self, name): 
		tmp = string.split(name,'/')
		if not name:
			name = 'index.html'
		if r.exists('pool:'+name):
			return r.get('pool:'+name)
		else:
			cache_file = 'cache'+os.sep+tmp[-1]
			print cache_file
			try:
				print 'open '+cache_file
				print os.stat(cache_file)
				f = open(cache_file)
				data = f.read()
				r.set('pool:'+name,data)
				return data
			except:
				print proxy+'/debian/pool/'+name
				try:
					req = urllib2.urlopen('http://'+proxy+'/debian/pool/'+name)
					data = req.read() 
					print req.info()
					f = open(cache_file,'w')
					f.write(data)
					f.close()
					r.set('pool:'+name,data)
					r.expire('pool:'+name,ttl)
					return data
				except:
					return web.notfound()
				
class dist:        
	def GET(self, name): 
		tmp = string.split(name,'/')
		if not name:
			name = 'index.html'
		if r.exists('dist:'+name):
			return r.get('dist:'+name)
		else:
			try:
				print proxy+'debian/dists/'+name
				req = urllib2.urlopen('http://'+proxy+'/debian/dists/'+name)
				data = req.read()
				r.set('dist:'+name,data)
				r.expire('dist:'+name,ttl)
				
				return data
			except:
				return 

class preseed:
	def GET(self,name):
		return render.wheezy(password,web.ctx.host)
	
class postinstall:
	def GET(self):
		return render.postinstall(web.ctx.host) 

class firstboot:
	def GET(self):
		return render.firstboot(web.ctx.host)

if __name__ == "__main__":
	app.run()
