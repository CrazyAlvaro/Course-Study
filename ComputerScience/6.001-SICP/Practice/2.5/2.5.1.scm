#lang r5rs

(display "2.5.1")
(display "Exercise 2.77")
; apply-generic called twice:
; First: use tag 'complex' to get procedure: magnitude again, but with 'complex' tag stripped off
; Second: use tag 'rectangluar' to get procedure magnitude with rectangluar package(not the generic one),
; get the result

(display "Exercise 2.78")
(define (attach-tag type-tag contents)
  (cond ((number? contents) contents)
        ((symbol? contents) contents)
        (else (cons type-tag contents))))

(define (type-tag datum)
  (cond ((number? datum) 'scheme-number)
        ((symbol? datum) 'scheme-symbol)
        ((pair? datum) (car datum))
        (else (error "Bad tagged datum -- TYPE-TAG" datum))))

(define (contents datum)
  (cond ((number? datum) datum)
        ((symbol? datum) datum)
        ((pair? datum) (cdr datum))
        (else (error "Bad tagged datum -- CONTENTS" datum))))

(display "Exercise 2.79")
(define (equ? x y) (apply-generic 'equ? x y))

(define (install-equ?-package)
  (define (rational-equ? x y)
    (= (* (numer x) (denom y))
       (* (demom x) (numer y))))
  (define (complex-equ? x y)
    (and (= (real-part x)
            (real-part y))
         (= (imag-part x)
            (imag-part y))))

  (put 'equ? '(scheme-number scheme-number) eq?)
  (put 'equ? '(rational rational) rational-equ?)
  (put 'equ? '(complex complex) complex-equ?)
  'done)

(display "Exercise 2.80")
(define (=zero? x) (apply-generic '=zero x))

(define (install-=zero?-package)
  (put '=zero? '(scheme-number)
    (lambda (x) (= x 0)))
  (put '=zero? '(rational)
    (lambda (x) (= (numer x) 0))
  (put '=zero? '(complex)
    (lambda (x) (= (magnitude x) 0))))
  'done)
