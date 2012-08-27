substrate_preseed
=================

A debian preseed and package cache using redis and webpy

#Software

Software needed to run 

[redis](http://redis.io)
[webpy](http://webpy.org)

apt-get install python-redis redis-server python-webpy

# Usage 

download the wheezy boot iso , or install a pxe environment 

select automatic install and add 

url=this.server:8080

to the kernel boot line

press enter

###references 

http://www.50ply.com/blog/2012/07/16/automating-debian-installs-with-preseed-and-puppet/
