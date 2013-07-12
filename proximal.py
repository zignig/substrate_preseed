#!/usr/bin/python
import web
import urllib2,string,os,json,uuid,crypt,random,string
import sqlite3

conf = json.load(open('/opt/substrate_preseed/proximal.conf'))
#database = sqlite3.connect('/opt/test.db')
#cur = database.cursor()
db = web.database(dbn='sqlite',db='/opt/db/test.db')

urls = (
	'/menu/(.*)','menu',
	'/postinstall/(.*)','postinstall',
	'/firstboot/(.*)','firstboot',
	'/prsd/(.*)','preseed',
	'/d-i/(.*)','preseed',
	'/boot','chain',
	'/boot/(.*)','boot',
	'/class/(.*)','machine_type',
	'/menu/(.*)','menu',
	'/','front_page'
	)

app = web.application(urls, globals())

proxy = conf['mirror']
render = web.template.render('/opt/substrate_preseed/templates')
password = conf['password']
suite = conf['suite']
salt_master = conf['salt_master']
net_boot_path = 'http://debian.org/debian/wheezy/main/installer-i386/current/images/netboot/debian-installer/i386/'
#net_boot_path = 'sid/main/installer-i386/current/images/cdrom/'

def check_mac(mac):
	data = db.where('machines',mac=mac)
	if len(data.list()) == 0:
		return True 
	else:
		return False 

def check_status(mac):
	data = db.where('machines',mac=mac)
	d = data.list().pop()
	status = d['status']
	if status == 1:
		return True
	else:
		return False

def insert_mac(mac,name):
	if check_mac(mac):
		db.insert('machines',name=name,mac=mac,status=0)
		return True
	else:
		return False

def password_hash(password,salt_length=4):
	salt_string = ''
	for i in range(salt_length):
		salt_string = salt_string + random.choice(string.letters)
	salt = '$1$'+salt_string+'$' #1 is md5 hash
	return crypt.crypt(password,salt)

class menu:
	def GET(self,name):
<<<<<<< HEAD
		print name
		return render.menu(conf['servers'],name,web.ctx.host)
=======
		parts = name.split('/')
		if check_mac(parts[0]):
			return render.menu(conf['servers'],parts[-1],web.ctx.host)
		else:
			if check_status(parts[0]):
				return render.hard_drive(parts[-1],web.ctx.host)
			else:
				return render.ipxe(parts[-1],web.ctx.host)
>>>>>>> 45f22dc9128db3cc6c027c3745951d1d2a122e22

class front_page:
	def GET(self):
		return render.frontpage(web.ctx.host)

class machine_type:
	def GET(self,name):
		parts = name.split('/')
		insert_mac(parts[1],parts[0])
		return render.ipxe(name,web.ctx.host)

class preseed:
	def GET(self,name):
		parts = name.split('/')
		return render.wheezy(password_hash(password),web.ctx.host,suite,machine_name,mac_address)
	
class postinstall:
	def GET(self,name):
		return render.postinstall(web.ctx.host,salt_master,machine_name)

class firstboot:
	def GET(self,name):
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
		return data

application = web.application(urls, globals()).wsgifunc()

if __name__ == "__main__":
	app.run()
