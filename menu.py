#!/usr/bin/python

import yaml 
import string,os


class menu_item(yaml.YAMLObject):
	yaml_tag = '!menu_item'

	def __init__(self,name,tag,link):
		self.name = name
		self.tag = tag
		self.link = link

	def show(self,parent):
		txt = ':'+self.tag+'\n'
		txt = txt +  self.link + '\n' 
		txt = txt + 'goto '+parent + '\n\n'
		return txt

	def item(self):
		return 'item '+self.tag+' '+self.name+'\n'
	
class menu(yaml.YAMLObject):
	yaml_tag = '!menu'
	def __init__(self,title='Menu',tag='start'):
		self.title = title
		self.tag = tag 
		self.items = []

	def __repr__(self):
		return self.show()

	def add_item(self,item):
		self.items.append(item)
	
	def item(self):
		return 'item '+self.tag+' > '+self.title+'\n'

	def show(self,parent=''):
		txt = ':'+self.tag+'\n'
		txt = txt + 'menu ' + self.title + '\n' 
		# return the menu links
		for i in self.items:
			txt = txt + i.item()
		if parent != '':
			txt = txt + 'item ' + parent +' < '+parent+'\n'
		txt = txt + 'choose --timeout 10000 selected\n'
		txt = txt + 'goto ${selected}\n\n'
		# return the menu items:
		for i in self.items:
			txt = txt + i.show(self.tag)
		return txt

	def boot_menu(self):	
		txt = '#!ipxe\n\n'
		#txt = txt + 'dhcp\n\n'
		txt = txt + self.show()
		return txt
	
	def save(self,file_name='menu.yaml'):
		f = open('menu.yaml','w')
		f.write(yaml.dump(self))
		

def get_menu(file_name='menu.yaml'):
	return yaml.load(open(file_name).read())

m = get_menu()
print m.boot_menu()
#f = open('./substrate.ipxe','w')
#f.write(m.boot_menu(''))
