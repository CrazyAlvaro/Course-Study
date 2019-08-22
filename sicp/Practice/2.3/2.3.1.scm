#lang r5rs

(define (memq item x)
  (cond ((null? x) #f)
        ((eq? item (car x)) x)
        (else (memq item (cdr x)))))

(display (memq 'apple '(pear banana prune)))
(newline)
(display (memq 'apple '(x (apple sauce) y apple pear)))
(newline)

(newline)
(display "Exercise 2.53")
(newline)
(display (list 'a 'b 'c))
; (a b c)

(newline)
(display (list (list 'george)))
; ((george))

(newline)
(display (cdr '((x1 x2) (y1 y2))))
; ((y1 y2))

(newline)
(display (cadr '((x1 x2) (y1 y2))))
;(y1 y2)

(newline)
(display (pair? (car '(a short list))))
; #f

(newline)
(display (memq 'red '((red shoes) (blue socks))))
; #f

(newline)
(display (memq 'red '(red shoes blue socks)))
; (red shoes blue socks)

(newline)
(display "Exercise 2.54")
(define (equal? list_a list_b)
  (if (and (pair? list_a) (pair? list_b))
    (and (equal? (car list_a) (car list_b))
         (equal? (cdr list_a) (cdr list_b)))
    (eq? list_a list_b)))

(newline)
(display (equal? '(this is a list) '(this (is a) list)))
(newline)
(display (equal? '(this is a list) '(this is a list)))

(newline)
(display "Exercise 2.55")
(newline)
(display (car ''abracadabra))
; the first make the interpreter take 'abracadabra as literal, while car get ', which is a quote
; ''abracadabra -> (quote (quote abracadabra))
