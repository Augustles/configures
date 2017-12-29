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
  var df = new Buffer(f, 'base64').toString()
  console.log(df);
  return df;
}
console.log('hi')
var s = "13f0aHRGj3cwtNP0cDovL212dmlkZW8xMC5tZWl0dWRhdGEuY29tLzVhM2Y5OTRmN2E5MjU3OTk2X0gyNjRfMTMubXA0P2s9MDJlNzdkOTYwODc1MDk2YjQ4ZjMyYzQ2OWU0N2ZmMGUmdD01YTRkwLln2mgSWY2IyNg=="
console.log(decode(s))
