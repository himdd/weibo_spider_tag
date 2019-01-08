#!/usr/bin/python
#coding=utf-8
import urllib
import urllib2
import types

# 下载页面
def getHtml(url):
	#proxy_support = urllib2.ProxyHandler({"http":"111.62.251.68"})
	#opener = urllib2.build_opener(proxy_support)
	#urllib2.install_opener(opener)
	#page = urllib2.urlopen(url)
	page = urllib.urlopen(url)
	html = page.read()
	return html

def getHtmlBYHeader(url):
	req = urllib2.Request(url)
	#req.add_header('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
	#req.add_header('Cookie', 'ALF=1524614421; SCF=Al2w2h2jx-fB3Ir8eewxsE9_FMTG5e4IZis4p5Slhc7b8bt3hfsqqkhWfem5K00VZeYxMUlxloabxFxjzUR_lro.; SUB=_2A253BWyvDeThGeRJ41cU8y7JzTiIHXVUBnTnrDV6PUNbktANLUiikW0qDq8WvthtIWqoWTIbFx1X0QoD_g..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF6D.gcYIoU3THy2GwO7YJ55JpX5KMhUgL.FozN1h-fe05fSoB2dJLoIpUeUgSfMEH8SCHFeF-RxbH8SEHWSE-RBntt; SUHB=0G0_XfKU_1U24U; SSOLoginState=1510022422; _T_WM=bb1b7258def0f6db0c0a960bc210b96a; H5:PWA:UID=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076036142740988%26fid%3D1076036142740988%26uicode%3D10000011')
	req.add_header('User-agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')
	req.add_header('Cookie', '_T_WM=0b6994d5c4c6711f4438b3f715d14d52; MLOGIN=1; ALF=1549269816; SCF=AiVit9qqs411Vq5h1N-dVvHm4deflYyLCCWOswtjmZcxMqVimcqSek7GNDN_0y3Z4qs6JOup_r7Ek6bLRKpqR3w.; SUB=_2A25xNB5tDeRhGeVO7lcQ-S_KwjmIHXVS1qIlrDV6PUJbktAKLRLakW1NTWgI7WJTDjhM_WGIwfpqi6l9OfLbF5Tp; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW3G7E1M5x7G2G9Z5XIBBk55JpX5K-hUgL.Foe7SK-p1K2c1K-2dJLoI7HQIgf.95tt; SUHB=0h1ZWSfJ20LNfP; SSOLoginState=1546677822; WEIBOCN_FROM=1110006030')
	res = urllib2.urlopen(req)
	html = res.read()
	return html

def urlencode(val):
    if isinstance(val,unicode):
        return urllib.quote_plus(str(val))
    return urllib.quote_plus(val)

# d = {'a':[{'objec':{'url':'http...'}}], b:'11'}
# json_get(d, ['a', 0, 'objec', 'url'], 'err')  # 'http...'
# json_get(d, ['b'], 'err') # err
# json_get(d, ['a', '0', 'object', 'url'], 'not') # not
def json_get(json, l_key, default):
    ret = json
    for k in l_key:
        if type(k) is types.IntType:
            if k < 0: return default
            if not (type(ret) is types.ListType): return default
            if len(ret) <= k: return default
        elif type(k) is types.StringType:
            if not (type(ret) is types.DictType): return default
            if not ret.has_key(k): return default
        else:
            return default
        ret = ret[k]

    return ret

