;; method new-if all arguments always got evaluated,
;; since sqrt-iter-new's second new-if argument is a recursive function call
;; it will be a tailing recursive call infinitly

(define (new-if predicate then-clause else-clause)
  (cond (predicate then-clause)
        (else else-clause)))

(define (good-enough? guess x)
  (< (/ (abs (- guess (improve guess x)))
        guess)
     0.001))

(define (sqrt-iter-new guess x)
  ;;(print "\n sqrt-iter was called with " guess " " x "\n")
  (new-if (good-enough? guess x)
          guess
          (sqrt-iter-new (improve guess x)
                     x)))

(define (sqrt-iter guess x)
  (if (good-enough? guess x)
    guess
    (sqrt-iter (improve guess x)
               x)))

(define (improve guess x)
  (average guess (/ x guess)))

(define (average x y) (/ (+ x y) 2))

(define (print . args)
  (cond ((not (null? args))
         (display (car args))
         (apply print (cdr args)))))
