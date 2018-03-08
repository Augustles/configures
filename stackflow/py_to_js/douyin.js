// xigua node执行

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
function decode(link) {
  var c = Math.random().toString(10).substring(2)
  , a = generateStr(link + "@" + c).toString(10);
  console.log(a);
  return [c, a];

}
var t = 'https://www.douyin.com/share/video/6507454755944533256/?region=CN&mid=6477833045666859790&titleType=title&timestamp=1519868747&utm_campaign=client_share&app=aweme&utm_medium=ios&iid=27073835399&utm_source=copy'
decode(t)
