#lang r5rs
;; 1.6
;; I think it will work fine
;; Incorrected, as running the program it gets infinitly loop
;; ### ANSWER ### because new-if is a method, scheme intepreter use applicative evaludate
;; and then evaluate all arguments, which means else-clause always got evaluated, which cause
;; a infinitly tailing recursive call

;; 1.7
;; For small number: 0.0001,
;; if the good-enough? is 0.001, then the diff is even more than the small number itself
;;
;; For large number:
;; The abs diff may always greater than 0.001 and never ends with good_enough
(define (good-enough? guess x)
  (< (abs (- (square guess) x)) 0.001))

(define (average x y)
  (/ (+ x y) 2.0))

(define (improve guess x)
  (average guess (/ x guess)))

(define (new-good-enough? guess x)
  (< (/ (abs (- guess (improve guess x)))
        guess)
     0.001))

(define (sqrt-iter guess x)
  (if (new-good-enough? guess x)
    guess
    (sqrt-iter (improve guess x)
               x)))

(define (sqrt x)
  (sqrt-iter 1.0 x))

;; > (sqrt 0.01)
;; 0.10000052895642693
;; > (sqrt 0.0001)
;; 0.010000714038711746

;; 1.8
(define (square x) (* x x))

(define (cube-root-iter guess x)
  (if (cube-root-good-enough? guess x)
      guess
      (cube-root-iter (cube-root-improve guess x)
                      x)))

(define (cube-root-improve guess x)
  (/ (+ (/ x (square guess))
        (* 2 guess))
     3.0))

(define (cube-root-good-enough? guess x)
  (< (/ (abs (- guess (cube-root-improve guess x)))
        guess)
     0.001))

;; > (cube-root-iter 1 10)
;; 2.1544959251533746
;; > (cube-root-iter 3 0.04)
;; 0.3420003820884027
