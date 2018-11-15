exports.perimeter  = (x, y) => (2*(x+y))
exports.area = (x, y) => (x*y)

// Pattern, callback(error, object)

module.exports = (x, y, callback) => {
  // pass in callback function accept two variables, object(err), or object
  if (x <= 0 || y <= 0)
    setTimeout(() =>
      callback(new Error("Rectangle dimensions should be greater than zero: \
        l = " + x + ", and b = " + y),
        null),
      2000);
  else {
    setTimeout(() =>
      // no error, pass back object
      callback(null, {

        // closure function access x, y
        perimeter: () => (2*(x+y)),
        area: () => (x*y)
      }),
      2000);
  }
}
