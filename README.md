substrate_preseed
=================

A debian preseed and package cache using redis and webpy

This program will install a vanilla copy of unstable debian with no interaction

#WARNING , WILL FORMAT WITH NO QUESTIONS
(you have been warned)

#Software

Software needed to run 

[redis](http://redis.io)

[webpy](http://webpy.org)

[salt](http://saltstate.org)

apt-get install python-redis redis-server python-webpy

# Usage 

get the iPXE boot iso


# Virtual auto boot

If you have a recent version of KVM the virtuals have the ipxe.org firmware

it is now possible to boot directly from the firmware. 

control B to enter firmware 

iPXE>dhcp 

gets a IP address

iPXE>chain http://server:8080/boot

wait a while ..... debian box with a password as defined in the config file

###references 

http://www.50ply.com/blog/2012/07/16/automating-debian-installs-with-preseed-and-puppet/

http://wiki.debian.org/DebianInstaller/Preseed

http://ipxe.org/cmd/chain
