#lang r5rs

(display "3.5 Streams")

;; error function
(define (error reason . args)
  (display "Error: ")
  (display reason)
  (for-each (lambda (arg)
              (display " ")
              (write arg))
            args)
  (newline))

(newline)
(display "3.5.1 Streams Are Delayed Lists")
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
(display "Exercise 3.50")
(define (stream-map-n proc . argstreams)
  (if (stream-null? (car argstreams))
      the-empty-stream
      (cons-stream
        (apply proc (map stream-car argstreams))
        (apply stream-map
               (cons proc (map stream-cdr argstreams))))))

(newline)
(display "Exercise 3.51")
(define (show x)
  (display-line x)
  x)

(define x (stream-map show (stream-enumerate-interval 0 10)))

(newline)
(display "stream-ref x 5")
(newline)
(display (stream-ref x 5))

(newline)
(display "stream-ref x 7")
(newline)
(display (stream-ref x 7))

(newline)
(display "Exercise 3.52")
(define sum 0)
(define (accum x)
  (set! sum (+ x sum))
  sum)
(newline)
(display "accum: ")
(display sum)

(define seq (stream-map accum (stream-enumerate-interval 1 20)))
(newline)
(display "seq: ")
(display sum)

(define y (stream-filter even? seq))
(newline)
(display "stream-filter even: ")
(display sum)

(define z (stream-filter (lambda (x) (= (remainder x 5) 0))
          seq))

(newline)
(display "stream-filter 5 times: ")
(display sum)

(newline)
(display "stream-ref y 7: ")
(stream-ref y 7)
(display sum)

(display-stream z)
(newline)
(display "display-stream z: ")
(display sum)
