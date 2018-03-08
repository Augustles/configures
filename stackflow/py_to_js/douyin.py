# coding=utf8

import js2py
import ipdb

xigua_raw_js = '''
'''

douyin_js ='''
function decode(link) {
  var c = Math.random().toString(10).substring(2)
  , a = generateStr(link + "@" + c).toString(10);
  console.log('hi');
  console.log(c, a);
  return [c, a];

}
function generateStr(a) {
  var c = function() {
      for (var d = 0, f = new Array(256), g = 0; 256 != g; ++g) {
          d = g,
          d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
          d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
          d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
          d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
          d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
          d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
          d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
          d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
          f[g] = d
      }
      return "undefined" != typeof Int32Array ? new Int32Array(f) : f
  }()
    , b = function(g) {
      for (var j, k, h = -1, f = 0, d = g.length; f < d; ) {
          j = g.charCodeAt(f++),
          j < 128 ? h = h >>> 8 ^ c[255 & (h ^ j)] : j < 2048 ? (h = h >>> 8 ^ c[255 & (h ^ (192 | j >> 6 & 31))],
          h = h >>> 8 ^ c[255 & (h ^ (128 | 63 & j))]) : j >= 55296 && j < 57344 ? (j = (1023 & j) + 64,
          k = 1023 & g.charCodeAt(f++),
          h = h >>> 8 ^ c[255 & (h ^ (240 | j >> 8 & 7))],
          h = h >>> 8 ^ c[255 & (h ^ (128 | j >> 2 & 63))],
          h = h >>> 8 ^ c[255 & (h ^ (128 | k >> 6 & 15 | (3 & j) << 4))],
          h = h >>> 8 ^ c[255 & (h ^ (128 | 63 & k))]) : (h = h >>> 8 ^ c[255 & (h ^ (224 | j >> 12 & 15))],
          h = h >>> 8 ^ c[255 & (h ^ (128 | j >> 6 & 63))],
          h = h >>> 8 ^ c[255 & (h ^ (128 | 63 & j))])
      }
      return h ^ -1
  };
  return b(a) >>> 0
}
'''

t = '//ib.365yg.com/video/urls/v/1/toutiao/mp4/fed2e9939d4744d0b5b97e83787966b2'
js2py.eval_js('console.log("Hi")')
js = js2py.eval_js(douyin_js)
ipdb.set_trace()
pre_t = '/'.join(t.split('/')[3:])
print pre_t
value = js(t)
url = 'https://ib.365yg.com%s&s=%s&callback=tt_playertopyy'%(value[0], value[1])
print url
