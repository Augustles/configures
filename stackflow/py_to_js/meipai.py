# coding=utf8

import base64
import js2py

meipai_raw_js = '''
b.decodeMp4 = {
    getHex: function(a) {
        return {
            str: a[h](4),
            hex: a[h](0, 4)[i]("").reverse().join("")
        }
    },
    getDec: function(a) {
        var b = parseInt(a, 16).toString();
        return {
            pre: b[h](0, 2)[i](""),
            tail: b[h](2)[i]("")
        }
    },
    substr: function(a, b) {
        var c = a[h](0, b[0])
          , d = a[k](b[0], b[1]);
        return c + a[h](b[0])[j](d, "")
    },
    getPos: function(a, b) {
        return b[0] = a.length - b[0] - b[1],
        b
    },
    decode: function(a) {
        var b = this.getHex(a)
          , c = this.getDec(b.hex)
          , d = this[k](b.str, c.pre);
        return g.atob(this[k](d, this.getPos(d, c.tail)))
    }
};
'''

meipai_js = '''
function decode(a) {
  var h = "substring",
    i = "split",
    k = 'substr',
    j='replace';
  var getHex = function(a) {
      return {
          str: a[h](4),
          hex: a[h](0, 4)[i]("").reverse().join("")
      }
  };
  var getDec = function(a) {
      var b = parseInt(a, 16).toString();
      return {
          pre: b[h](0, 2)[i](""),
          tail: b[h](2)[i]("")
      }
  };
  var substr = function(a, b) {
      var c = a[h](0, b[0])
        , d = a[k](b[0], b[1]);
      return c + a[h](b[0])[j](d, "")
  };
  var getPos = function(a, b) {
      return b[0] = a.length - b[0] - b[1],
      b
  };
  var b = getHex(a),
    c = getDec(b.hex),
    d = substr(b.str, c.pre),
    e = getPos(d, c.tail),
    f = d[k](e);
  // var df = new Buffer(f, 'base64').toString()
  // console.log(df);
  return f;
}
'''
def decode(encoded_string):
    def getHex(param1):
        return {
            'str': param1[4:],
            'hex': ''.join(list(param1[:4])[::-1]),
        }

    def getDec(param1):
        loc2 = str(int(param1, 16))
        return {
            'pre': list(loc2[:2]),
            'tail': list(loc2[2:]),
        }

    def substr(param1, param2):
        loc3 = param1[0: int(param2[0])]
        loc4 = param1[int(param2[0]): int(param2[0]) + int(param2[1])]
        return loc3 + param1[int(param2[0]):].replace(loc4, "")

    def getPos(param1, param2):
        param2[0] = len(param1) - int(param2[0]) - int(param2[1])
        return param2

    dict2 = getHex(encoded_string)
    dict3 = getDec(dict2['hex'])
    str4 = substr(dict2['str'], dict3['pre'])
    #  print substr(str4, getPos(str4, dict3['tail']))
    return base64.b64decode(substr(str4, getPos(str4, dict3['tail'])))

s = '3ef1aHR0cDovwL212dmlkZW8xMC5tZWl0dWRhdGEuY29tLzVhM2U1YzNhMzBlN2Y4NDg3X0gyNjRfMTMubXA0P2s9ODgwMmFjMjFjN2Y4NzdkMGYzZWJiNzFlODFiMzA5ZjImdD01YTRkYzkcdZmNA=='
s = "f671aHR0cWxOPjE5tZDovL212dmlkZW8xMS5tZWl0dWRhdGEuY29tLzVhM2U1MDRhNzNjZjUxNzkyX0gyNjRfNy5tcDQ/az1lZDI3Y2Q3NjliYmJiZTdmZDI4ZTc4NDAzYTc1ZTFhNyZ0PTVmMcrwIc2ohNGRjYWIy"
s = "13f0aHRGj3cwtNP0cDovL212dmlkZW8xMC5tZWl0dWRhdGEuY29tLzVhM2Y5OTRmN2E5MjU3OTk2X0gyNjRfMTMubXA0P2s9MDJlNzdkOTYwODc1MDk2YjQ4ZjMyYzQ2OWU0N2ZmMGUmdD01YTRkwLln2mgSWY2IyNg=="
t = decode(s)
print t

js2py.eval_js('console.log("Hi")')
js = js2py.eval_js(meipai_js)
value = js(s)
print value
print base64.b64decode(value)
