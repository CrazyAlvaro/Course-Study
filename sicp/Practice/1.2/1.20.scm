; Normal order evaludation is lazy evaluation which evaluate until needed,
(define (gcd a b)
  (if (= b 0)
    a
    (gcd b (remainder a b))))

(gcd 206 40)
(if (= 40 0))

(gcd 40 (remainder 206 40))
(if (= 6 0))

(gcd (remainder 206 40) (remainder 40 (remainder 206 40)))
(if (= 4 0))

(gcd (remainder 40 (remainder 206 40)) (remainder (remainder 206 40) (remainder 40 (remainder 206 40))))
(if (= 2 0))

(gcd (remainder (remainder 206 40) (remainder 40 (remainder 206 40))) (remainder (remainder 40 (remainder 206 40)) (remainder (remainder 206 40) (remainder 40 (remainder 206 40)))))

; total 18 remainders include if evaluation


; applicative-order evaluation
(gcd 206 40)

(gcd 40 (remainder 206 40))

(gcd 40 6)

(gcd 6 (remainder 40 6))

(gcd 6 4)

(gcd 4 (remainder 6 4))

(gcd 4 2)

(gcd 2 (remainder 4 2))

(gcd 2 0)

2

; total 4 remainders performed
