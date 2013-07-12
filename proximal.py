#!/usr/bin/python
import web
import urllib2,string,os,json,uuid,crypt,random,string
import sqlite3

web.config.debug = True 
conf = json.load(open('/opt/substrate_preseed/proximal.conf'))
db = web.database(dbn='sqlite',db='/opt/data_preseed/test.db')

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
	'/finished/(.*)','finished',
	'/','front_page'
	)

app = web.application(urls, globals())

proxy = conf['mirror']
render = web.template.render('/opt/substrate_preseed/templates')
password = conf['password']
suite = conf['suite']
salt_master = conf['salt_master']

# TODO add downloader for these files on first boot
kernel = "http://ftp.debian.org/debian/dists/stable/main/installer-i386/current/images/netboot/debian-installer/i386/linux"
initrd = "http://ftp.debian.org/debian/dists/stable/main/installer-i386/current/images/netboot/debian-installer/i386/initrd.gz"

# convert to class for abstraction
# class machine:

def get_info(mac):
	data = db.where('machines',mac=mac)
	return data.list().pop()

def check_mac(mac):
	data = db.where('machines',mac=mac)
	if len(data.list()) == 0:
		return True 
	else:
		return False 

def set_status(mac):
	db.update('machines',where='mac = $mac',status=1,vars=locals())

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
		parts = name.split('/')
		if check_mac(parts[0]):
			return render.menu(conf['servers'],parts[-1],web.ctx.host)
		else:
			if check_status(parts[0]):
				return render.hard_drive(parts[-1],web.ctx.host)
			else:
				return render.ipxe(parts[-1],web.ctx.host)

class front_page:
	def GET(self):
		return render.frontpage(web.ctx.host)

class machine_type:
	def GET(self,name):
		parts = name.split('/')
		insert_mac(parts[1],parts[0])
		return render.ipxe(web.ctx.host,name)

class preseed:
	def GET(self,name):
		parts = name.split('/')
		mac_address = parts[-1]
		machine = get_info(mac_address)
		return render.wheezy(password_hash(password),web.ctx.host,suite,machine['name'],mac_address)
	
class postinstall:
	def GET(self,name):
		parts = name.split('/')
		mac_address = parts[-1]
		machine = get_info(mac_address)
		return render.postinstall(web.ctx.host,salt_master,mac_address)

class firstboot:
	def GET(self,name):
		parts = name.split('/')
		mac_address = parts[-1]
		machine = get_info(mac_address)
		return render.firstboot(web.ctx.host,salt_master,machine['name'],mac_address)


class finished:
	def GET(self,name):
		parts = name.split('/')
		mac_address = parts[-1]
		set_status(mac_address)
		return

class boot:
	def GET(self,name):
		# return boot binaries
		if name == 'linux' or name == 'initrd.gz':
			try:
				os.stat(conf['storage']+os.sep+name)
			 	data = open(conf['storage']+os.sep+name).read()
				return data	
			except:
				return 'fail'
			
		
		

application = web.application(urls, globals()).wsgifunc()

if __name__ == "__main__":
	app.run()
