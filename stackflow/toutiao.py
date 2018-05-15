# coding=utf8

import requests

import ssl

if hasattr(ssl, '_create_unverified_context'):
      ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.toutiao.com/api/pc/feed/"

querystring = {"max_behot_time":"1526320398","category":"__all__","utm_source":"toutiao","widen":"1","tadrequire":"true","as":"A1658ABF6A83077","cp":"5AFA3370A7C7FE1","_signature":"LDMkXhATdtCGHGTeTgOfoCwzJE"}

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    }

response = requests.request("GET", url, headers=headers, params=querystring, verify='gd_bundle-g2-g1.crt')

print(response.text)
