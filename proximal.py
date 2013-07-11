#!/usr/bin/python
import web
#import menu
import urllib2,string,os,json,uuid,crypt,random,string

conf = json.load(open('/opt/substrate_preseed/proximal.conf'))
print conf
#try:
#	os.stat('cache')
#except:
#	os.mkdir('cache')

urls = (
	'/postinstall/(.*)','postinstall',
	'/firstboot/(.*)','firstboot',
	'/prsd/(.*)','preseed',
	'/d-i/(.*)','preseed',
	'/boot','chain',
	'/boot/(.*)','boot',
	'/class/(.*)','machine_type',
	'/','front_page'
	)

app = web.application(urls, globals())

proxy = conf['mirror']
render = web.template.render('/opt/substrate_preseed/templates')
password = conf['password']
suite = conf['suite']
salt_master = conf['salt_master']
net_boot_path = 'wheezy/main/installer-i386/current/images/netboot/debian-installer/i386/'
#net_boot_path = 'sid/main/installer-i386/current/images/cdrom/'

def password_hash(password,salt_length=4):
	salt_string = ''
	for i in range(salt_length):
		salt_string = salt_string + random.choice(string.letters)
	salt = '$1$'+salt_string+'$' #1 is md5 hash
	return crypt.crypt(password,salt)

class front_page:
	def GET(self):
		return render.frontpage(web.ctx.host)

class machine_type:
	def GET(self,name):
		print(machine_name)
		return render.ipxe(web.ctx.host,name,'')

class preseed:
	def GET(self,name):
		machine_name = r.get('machine:'+name.split('/')[-1])
		mac_address = name.split('/')[-1]
		return render.wheezy(password_hash(password),web.ctx.host,suite,machine_name,mac_address)
	
class postinstall:
	def GET(self,name):
		machine_name = name.split('/')[-1]
		return render.postinstall(web.ctx.host,salt_master,machine_name)

class firstboot:
	def GET(self,name):
		machine_name = r.get('machine:'+name.split('/')[-1])
		return render.firstboot(web.ctx.host,salt_master,machine_name)

class chain:
	def GET(self):
		print(web.input())
		machine_name = 'mac:'+web.input()['mac']
		return('#!ipxe\n\nexit')
		if r.exists(machine_name):
			return render.ipxe(web.ctx.host,r.get(machine_name),menu)
		else:
			r.set(machine_name,'master')
			return render.ipxe(web.ctx.host,'master',menu)

class boot:
	def GET(self,name):
		d = dist()
		path = net_boot_path+'/'+name
		print path 
		data  = d.GET(path)
		r.expire(path,8*ttl)
		return data

application = web.application(urls, globals()).wsgifunc()

if __name__ == "__main__":
	app.run()
