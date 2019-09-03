#lang r5rs

(display "2.5.3")
(display "Exercise 2.87")
(define (install-polynomial-package)
  ;; internal procedures
  ;; representation of poly
  (define (make-polynomial variable term-list)
    (cons variable term-list))
  (define (variable p) (car p))
  (define (term-list p) (cdr p))


  (define (tag p) (attach-tag 'polynomial p))
  (put 'add '(polynomial polynomial)
       (lambda (p1 p2) (tag (add-poly p1 p2))))
  (put 'mul '(polynomial polynomial)
       (lambda (p1 p2) (tag (mul-poly p1 p2))))
  (put 'make 'polynomial
       (lambda (var terms) (tag (make-polynomial var terms))))
  (put '=zero? '(polynomial)
       (lambda (p) (empty-termlist? (term-list p))))
  'done)

(display "Exercise 2.88")
(define (negate x) (apply-generic 'negate x))

(define (install-polynomial-package-ext)
  (define (negate-poly p)
    (make-polynomial (variable p)
                     (map
                       (lambda (term)
                         (make-term
                           (order term)
                           (negate (coeff term))))
                       (term-list p))))

  (define (sub-poly p1 p2)
    (if (same-variable? (variable p1) (variable p2))
        (make-polynomial (variable p1)
                   ; add the negateative of number equals subract this number
                   (add-terms (term-list p1)
                              (term-list (negate p2))))))
  (put 'negate '(polynomial) negate)
  'done)

(display "Exercise 2.89")
(define (first-term term-list)
  (make-term (- (length term-list) 1) (car term-list)))

(define (adjoin-term term term-list)
  (cond ((=zero? (coeff term) term-list)
        ((equal? (length term-list) (order term))
         (cons (coeff term) term-list))
        (else
          (adjoin-term term (cons 0 term-list))))))

(display "Exercise 2.90")
; need to change all the term/term-list level to generic procedures
(define (adjoin-term term term-list) (apply-generic 'adjoin-term term term-list))
(define (the-empty-termlist) '())
(define (first-term term-list) (apply-generic 'first-term term-list))
(define (rest-terms term-list) (apply-generic 'rest-terms term-list))
(define (empty-termlist? term-list) (apply-generic 'empty-termlist? term-list))
(define (order term) (apply-generic 'order term))
(define (coeff term) (apply-generic 'coeff term))

(define (make-sparse-term order coeff)
  ((get 'make-sparse-term) order coeff))
(define (make-dense-term order coeff)
  ((get 'make-dense-term order coeff)))

; Make first-term and adjoin-term generic
(define (install-sparse-term-list-package)
  (define (adjoin-term term term-list)
    (if (=zero? (coeff term)
        term-list
        (cons term term-list))))

  ; Interface to the rest of the system
  (define (tag-term x) (attach-tag 'sparse-term x))
  (define (tag-term-list x) (attch-tag 'sparse-term-list x))
  (put 'order 'sparse-term (lambda (term) (car term)))
  (put 'coeff 'sparse-term (lambda (term) (cdr term)))
  (put 'adjoin-term '(sparse-term sparse-term-list)
    (lambda (term lst) (tag-term-list (adjoin-term term lst))))
  (put 'first-term 'sparse-term-list (lambda (lst) (tag-term (car lst))))
  (put 'rest-terms 'sparse-term-list (lambda (lst) (tag-term-list (cdr lst))))
  (put 'empty-termlist? 'sparse-term-list (lambda (lst) (null? lst)))
  'done)

(define (install-dense-term-lisst-package)
  (define (adjoin-term term term-list)
    (cond ((=zero? (coeff term) term-list)
          ((equal? (length term-list) (order term))
           (cons (coeff term) term-list))
          (else
            (adjoin-term term (cons 0 term-list))))))
  (define (first-term term-list)
    (make-term (- (length term-list) 1) (car term-list)))

  ; Interface
  (define (tag-term x) (attach-tag 'dense-term x))
  (define (tag-term-list lst) (attch-tag 'dense-term-list lst))
  (put 'order 'dense-term (lambda (term) (car term)))
  (put 'coeff 'dense-term (lambda (term) (cdr term)))
  (put 'adjoin-term '(dense-term dense-term-list)
    (lambda (term lst) (tag-term-list (adjoin-term term lst))))
  (put 'first-term 'dense-term-list (lambda (lst) (tag-term (first-term lst))))
  (put 'rest-terms 'dense-term-list (lambda (lst) (tag-term-list (cdr lst))))
  (put 'empty-termlist? 'dense-term-list (lambda (lst) (null? lst)))
  'done)

(display "Exercise 2.91")
; Return quotient and remainder
(put 'negate 'term-list
  (lambda (term-lst)
    (map
      (lambda (term)
        (make-term (order term) (negate (coeff term))))
      term-lst)))

(define (div-terms L1 L2)
  (if (empty-termlist? L1)
      (list (the-empty-termlist) (the-empty-termlist))
      (let ((t1 (first-term L1))
            (t2 (first-term L2)))
        (if (> (order t2) (order t1))
            (list (the-empty-termlist) L1)
            (let ((new-c (div (coeff t1) (coeff t2)))
                  (new-o (- (order t1) (order t2)))
                  (new-term (make-term new-o new-c)))
              (let ((rest-of-result
                    (div-terms (add-terms L1
                                 (negate
                                   (mul-terms
                                     (adjoin-term new-term the-empty-termlist)
                                     L2)))
                               L2)))
                (list
                  (adjoin-term new-term (car rest-of-result))
                  (cadr rest-of-result))))))))


(define (div-poly P1 P2)
  (if (same-variable? (variable P1) (variable P2))
      (make-poly (variable P1)
                 (div-terms (term-list P1)
                            (term-list P2)))
      (error "Polys not in same var -- DIV-POLY"
             (list P1 P2))))

(display "Exercise 2.92")
; NOTE: skip 

(display "Exercise 2.93")
(define (install-rational-package)
  ;; internal procedures
  (define (numer x) (car x))
  (define (denom x) (cdr x))
  (define (make-rat n d) (cons n d))
  (define (add-rat x y)
    (make-rat (add (mul-terms (numer x) (denom y))
                   (mul-terms (numer y) (denom x)))
              (mul (denom x) (denom y))))
  (define (sub-rat x y)
    (make-rat (sub (mul-terms (numer x) (denom y))
                   (mul-terms (numer y) (denom x)))
              (mul (denom x) (denom y))))
  (define (mul-rat x y)
    (make-rat (mul (numer x) (numer y))
              (mul (denom x) (denom y))))
  (define (div-rat x y)
    (make-rat (mul (numer x) (denom y))
              (mul (denom x) (numer y))))

  ;; interface to the rest of the system
  (define (tag x) (attach-tag 'rational x))
  (put 'add '(rational rational)
       (lambda (x y) (tag (add-rat x y))))
  (put 'sub '(rational rational)
       (lambda (x y) (tag (sub-rat x y))))
  (put 'mul '(rational rational)
       (lambda (x y) (tag (mul-rat x y))))
  (put 'div '(rational rational)
       (lambda (x y) (tag (div-rat x y))))
  (put 'make 'rational
       (lambda (x y) (tag (make-rat x y))))
  'done)

(define (make-rational n d)
  ((get 'make 'rational) n d))

(define p1 (make-polynomial 'x '((2 1) (0 1))))
(define p2 (make-polynomial 'x '((3 1) (0 1))))
(define rf (make-rational p2 p1))

(display "Exercise 2.94")
(define (remainder-terms a b)
  (cadr (div-terms a b)))
(define (gcd-terms a b)
  (if (empty-termlist? b)
      a
      (gcd-terms b (remainder-terms a b))))

(define (greatest-common-divisor a b)
  (apply-generic 'greatest-common-divisor a b))

(put 'greatest-common-divisor '(scheme-number scheme-number)
  (lambda (a b) (gcd a b)))

(define (gcd-poly p1 p2)
  (if (same-variable? (variable p1) (variable p2))
      (make-polynomial (variable p1)
                       (gcd-terms (term-list p1)
                                  (term-list p2)))
      (error "not the same variable -- GCD-POLY" (list p1 p2))))

(put 'greatest-common-divisor '(polynomial polynomial)
  (lambda (a b) (tag (gcd-poly a b))))

(display "Exercise 2.95")
(define p1 (make-polynomial 'x '((2 1) (1 -2) (0 1))))
(define p2 (make-polynomial 'x '((2 11) (0 7))))
(define p3 (make-polynomial 'x '((1 13) (0 5))))

(display "Exercise 2.96")
; NOTE: skip

(display "Exercise 2.97")
; NOTE: skip
