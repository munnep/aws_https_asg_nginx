# Let's Encrypt

This README describes how to create valid certificates to use for websites using Let's Encrypt. Using Let's Encrypt enables you to create free certificates. 

You will use a vagrant box to have a server on which to create the certificates and test them. 

# Prerequisites

Vagrant [See documentation](https://www.vagrantup.com/docs/installation)  
Virtualbox [See documentation](https://www.virtualbox.org/wiki/Downloads)


# Create Let's Encrypt certificates

- in AWS create a valid DNS record in route53 
```
patrick.bg.hashicorp-success.com	A	Simple	-	
192.168.56.33
```
- test it
```
nslookup patrick.bg.hashicorp-success.com

Server:		127.0.0.53
Address:	127.0.0.53#53

Non-authoritative answer:
Name:	patrick.bg.hashicorp-success.com
Address: 192.168.56.33

```

- create a vagrantfile to create a test server with nginx
```
vagrant up
```

## Vagrant machine

- login to the machine
```
vagrant ssh
```
- install certbot
```
# install certbot if not installed
sudo apt-get update
sudo apt-get install -y certbot
```
- create a certificate to use for the website
```  
# generate a certificate for our domain
# use manual challenge, and we will create a dns entry manually
certbot -d patrick.bg.hashicorp-success.com --manual --preferred-challenges dns certonly
```
certbot -d patrick.bg.hashicorp-success.com --manual --preferred-challenges dns certonly
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator manual, Installer None
Obtaining a new certificate
Performing the following challenges:
dns-01 challenge for patrick.bg.hashicorp-success.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NOTE: The IP of this machine will be publicly logged as having requested this
certificate. If you're running certbot in manual mode on a machine that is not
your server, please ensure you're okay with that.

Are you OK with your IP being logged?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: Y

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please deploy a DNS TXT record under the name
_acme-challenge.patrick.bg.hashicorp-success.com with the following value:

6uoMl-Y22itwfK74iIF0kcKkZFJ_mzLc2ui-W21iiLk

Before continuing, verify the record is deployed.
```
- create this DNS TXT record in aws route53
```
_acme-challenge.patrick.bg.hashicorp-success.com

```
- Check in a different terminal. Can take 10 minutes or more
```
dig TXT _acme-challenge.patrick.bg.hashicorp-success.com

; <<>> DiG 9.11.3-1ubuntu1.11-Ubuntu <<>> TXT _acme-challenge.patrick.bg.hashicorp-success.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40007
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;_acme-challenge.patrick.bg.hashicorp-success.com. IN TXT

;; ANSWER SECTION:
_acme-challenge.patrick.bg.hashicorp-success.com. 300 IN TXT "0IOUxCsL8ZU64U6SlEFWwfq7HtrY8UCUL7HM6qNVZL0"

;; Query time: 27 msec
;; SERVER: 192.168.0.1#53(192.168.0.1)
;; WHEN: Mon Apr 04 16:34:56 CEST 2022
;; MSG SIZE  rcvd: 133


- continue by pressing ENTER
```
Waiting for verification...
Cleaning up challenges

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/patrick.bg.hashicorp-success.com/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/patrick.bg.hashicorp-success.com/privkey.pem
   Your cert will expire on 2022-05-09. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot
   again. To non-interactively renew *all* of your certificates, run
   "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le

```
- Backup the certificate files
```
cp -apL /etc/letsencrypt/live/patrick.bg.hashicorp-success.com /vagrant
```

## Test the NGINX configuration with the certificates
- install nginx
```
sudo apt-get install -y nginx
```
- configure nginx with following configuration
```
vi /etc/nginx/sites-enabled/default 
```
```
# Default server configuration
server {
	listen 80 default_server;
	listen [::]:80 default_server;

	# SSL configuration
	#
	listen 443 ssl default_server;
	listen [::]:443 ssl default_server;

	ssl_certificate /etc/letsencrypt/live/patrick.bg.hashicorp-success.com/fullchain.pem; # managed by Certbot
	ssl_certificate_key /etc/letsencrypt/live/patrick.bg.hashicorp-success.com/privkey.pem; # managed by Certbot

	root /var/www/html;
	index index.html index.htm index.nginx-debian.html;
	server_name _;

	location / {
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
		try_files $uri $uri/ =404;
	}
}
```
- restart the nginx server
```
service nginx restart
```
- in a web browser you should now see a valid environment  

