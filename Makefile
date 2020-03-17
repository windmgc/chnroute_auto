TIME_NOW=$(shell date -u '+%Y-%m-%d %H:%M:%S')

sync: sync_apnic_latest generate_chnroutes

sync_apnic_latest:
	wget 'https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest' -O 'delegated-apnic-latest'

generate_chnroutes:
	src/chnroutes.py

update_repo:
	git pull origin master
	git add .
	git commit -m "Auto updated $(TIME_NOW)"
	git push origin master
