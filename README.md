# CHNROUTE_AUTO

This repo provides raw routing table for China networks(chnroute), including both ipv4 and ipv6.

Trusted data was provided by APNIC, [APNIC Delegated List].

Data provided by this repo aims to fill the gap after the breakup of [ip.cn chnroute list], and will be updated every hour.

## How to use the chnroute_auto data

You can simply download or include the data anywhere you want:

[CHNROUTE_AUTO IPv4 DATA]

[CHNROUTE_AUTO IPv6 DATA]

Or you can clone this repo and sync for yourself:

```
$ make sync     # Download the latest delegated apnic data and generate chnroute-v4 and chnroute-v6
```

## Bugs and Issues

Issues and pull requests are welcome.


[APNIC Delegated List]:https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest
[ip.cn chnroute list]:http://f.ip.cn/rt/chnroutes.txt
[CHNROUTE_AUTO IPv4 DATA]:https://github.com/windmgc/chnroute_auto/raw/master/chnroute-v4
[CHNROUTE_AUTO IPv6 DATA]:https://github.com/windmgc/chnroute_auto/raw/master/chnroute-v6
