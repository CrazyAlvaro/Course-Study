#lang r5rs

;; error function
(define (error reason . args)
  (display "Error: ")
  (display reason)
  (for-each (lambda (arg)
              (display " ")
              (write arg))
            args)
  (newline))

(define (stream-filter pred stream)
  (cond ((stream-null? stream) the-empty-stream)
        ((pred (stream-car stream))
         (cons-stream (stream-car stream)
                      (stream-filter pred
                                     (stream-cdr stream))))
        (else (stream-filter pred (stream-cdr stream)))))

(define (stream-for-each proc s)
  (if (stream-null? s)
      'done
      (begin (proc (stream-car s))
             (stream-for-each proc (stream-cdr s)))))

(define (display-line x)
  (newline)
  (display x))

(define (display-stream s)
  (stream-for-each display-line s))

(define (cons-stream a b)
  (cons a (delay b)))
(define (stream-car s) (car s))
(define (stream-cdr s) (force (cdr s)))

(define (stream-ref s n)
  (if (= n 0)
      (stream-car s)
      (stream-ref (stream-cdr s) (- n 1))))

(define (stream-null? s) (null? s))
(define the-empty-stream '())

(define (stream-map proc s)
  (if (stream-null? s)
      the-empty-stream
      (cons-stream (proc (stream-car s))
                   (stream-map proc (stream-cdr s)))))

(define (stream-enumerate-interval low high)
  (if (> low high)
      the-empty-stream
      (cons-stream
        low
        (stream-enumerate-interval (+ low 1) high))))

(newline)
(display "3.5.2 Infinite Streams")
(define (integers-starting-from n)
  (cons-stream n (integers-starting-from (+ n 1))))

(define integers (integers-starting-from 1))

(define (fibgen a b)
  (cons-stream a (fibgen b (+ a b))))

(define fibs-gen (fibgen 0 1))

; add-streams
(define (add-streams s1 s2)
  (stream-map + s1 s2))

; Fibonacci number
(define fibs
  (cons-stream 0
               (cons-stream 1
                            (add-streams (stream-cdr fibs)
                            fibs))))

(define (scale-stream stream factor)
  (stream-map (lambda (x) (* x factor)) stream))

(define double (cons-stream 1 (scale-stream double 2)))

;;;;;;;;;;;;  Exercise ;;;;;;;;;;;;

(newline)
(display "Exercise 3.53")
; '(1 2 4 8 ...)

(newline)
(display "Exercise 3.54")
(define (mul-streams s1 s2)
  (stream-map * s1 s2))

(define factorials
  (cons-stream 1
               (mul-streams factorials
                            (stream-cdr integers))))

(newline)
(display "Exercise 3.55")
(define (partial-sums stream)
  (define (sums prev s)
    (let ((curr-val (+ prev (stream-car s))))
      (cons-stream curr-val
                  (sums curr-val (stream-cdr s)))))

  (sums 0 stream))

; alternative
(define (partial-sums-alt s)
  (add-streams s (cons-stream 0 (partial-sums s))))

(newline)
(display "Exercise 3.56")
(define S (cons-stream 1 (merge (merge (scale-stream S 2)
                                       (scale-stream S 3))
                                (scale-stream S 5))))

(newline)
(display "Exercise 3.57")
; I think the key here is that, if we use memo-proc, then all
; cons-stream will result to the same stream fib-stream we created at first,
; while if there's no such memo-proc, we will have to create new fib-stream as
; which will be exponential time

(newline)
(display "Exercise 3.58")
(define (expand num den radix)
  (cons-stream
    (quotient (* num radix) den)
    (expand (remainder (* num radix) den) den radix)))

(expand 1 7 10)
; 10/7 30/7 20/7 60/7 40/7 50/7 10/7 ...

(expand 3 8 10)
; 30/8 60/8 40/8 10 0 0 0...

(newline)
(display "Exercise 3.59")
; a
(define (integrate-series s)
  (stream-map / s integers))

(define exp-series
  (cons-stream 1 (integrate-series exp-series)))

; b
(define sine-series (cons-stream 0 (integrate-series cosine-series)))
(define cosine-series (cons-stream 1 (integrate-series (scale-stream sine-series -1))))

(newline)
(display "Exercise 3.60")
(define (mul-series s1 s2)
  (cons-stream (* (stream-car s1)
                  (stream-car s2))
               (add-streams (add-streams (scale-stream (stream-cdr s2)
                                                       (stream-car s1))
                                         (scale-stream (stream-cdr s1)
                                                       (stream-car s2)))
                            (mul-series (stream-cdr s1) (stream-cdr s2)))))

(newline)
(display "Exercise 3.61")
; NOTE: for S with constant 1
(define (invert-unit-series S)
  (cons-stream 1
               (scale-stream (mul-series (stream-cdr S)
                                         (invert-unit-series S))
                             -1)))

(newline)
(display "Exercise 3.62")
(define (div-series numer-series denom-series)
  (let ((denom-c (stream-car denom-series)))
    (if (= denom-c 0)
        (error "Denominator has zero constant -- DIV_SERIES" denom-series)
        (scale-stream (mul-series numer-series
                                  (invert-unit-series (scale-stream denom-series
                                                                    (/ 1 denom-c))))
                      (/ 1 denom-c)))))

(define tane-series (div-series sine-series cosine-series))
