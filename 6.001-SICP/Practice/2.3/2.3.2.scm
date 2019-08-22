#lang r5rs

(define (variable? x) (symbol? x))

(define (same-variable? v1 v2)
  (and (variable? v1) (variable? v2) (eq? v1 v2)))

(define (sum? x)
  (and (pair? x) (eq? (car x) '+)))

(define (addend e) (cadr e))

(define (augend e) (caddr e))

; (define (make-sum a1 a2) (list '+ a1 a2))
(define (=number? exp num)
  (and (number? exp) (= exp num)))

(define (make-sum a1 a2)
  (cond ((=number? a1 0) a2)
        ((=number? a2 0) a1)
        ((and (number? a1) (number? a2)) (+ a1 a2))
        (else (list '+ a1 a2))))

(define (product? e)
  (and (pair? e) (eq? (car e) '*)))

(define (multiplier e) (cadr e))

(define (multiplicand e) (caddr e))

(define (make-product m1 m2)
  (cond ((or (=number? m1 0) (=number? m2 0)) 0)
        ((=number? m1 1) m2)
        ((=number? m2 1) m1)
        ((and (number? m1) (number? m2)) (* m1 m2))
        (else (list '* m1 m2))))

(newline)
(display "Exercise 2.56")
(newline)
(define (exponentiation? x)
  (and (pair? x) (eq? (car x) '**)))

(define (base e)
  (cadr e))

(define (exponent e)
  (caddr e))

(define (make-exponentiation base exponent)
  (cond ((=number? base 1) 1)
        ((=number? exponent 0) 1)
        ((=number? exponent 1) base)
        (else
          (list '** base exponent))))

(define (error a b)
  (display a)
  (display b)
  (newline))

(define (deriv exp var)
  (cond ((number? exp) 0)
        ((variable? exp)
         (if (same-variable? exp var) 1 0))
        ((sum? exp)
         (make-sum (deriv (addend exp) var)
                   (deriv (augend exp) var)))
        ((product? exp)
         (make-sum
           (make-product (multiplier exp)
                         (deriv (multiplicand exp) var))
           (make-product (deriv (multiplier exp) var)
                         (multiplicand exp))))
        ((exponentiation? exp)
         (make-product (exponent exp)
                       (make-product
                         (make-exponentiation
                           (base exp)
                           (- (exponent exp) 1))
                         (deriv (base exp) var))))
        (else (error "unknown expression type -- DERIV" exp))))


; Test
(display (deriv '(+ x 3) 'x))
(newline)
(display (deriv '(* x y) 'x))
(newline)
(display (deriv '(* (* x y) (+ x 3)) 'x))
(newline)
(display (deriv '(** x 5) 'x))
(newline)

(display "Exercise 2.57")
(newline)
(define (augend-ext sum)
  (if (> (length sum) 3)
    (cons '* (cddr sum))
    (caddr sum)))

(define (multiplicand-ext e)
  (if (> (length e) 3)
    (cons '* (cddr e))
    (caddr e)))

(define (deriv-ext exp var)
  (cond ((number? exp) 0)
        ((variable? exp)
         (if (same-variable? exp var) 1 0))
        ((sum? exp)
         (make-sum (deriv (addend exp) var)
                   (deriv (augend-ext exp) var)))
        ((product? exp)
         (make-sum
           (make-product (multiplier exp)
                         (deriv (multiplicand-ext exp) var))
           (make-product (deriv (multiplier exp) var)
                         (multiplicand-ext exp))))
        ((exponentiation? exp)
         (make-product (exponent exp)
                       (make-product
                         (make-exponentiation
                           (base exp)
                           (- (exponent exp) 1))
                         (deriv (base exp) var))))
        (else
          (error "unknown expression type -- DERIV" exp))))

(display (deriv-ext '(* x y (+ x 3)) 'x))
(newline)

(display "Exercise 2.58")
(newline)
(display "a")
(newline)
; assume + and * always takes two arguments and
; that expressions are fully parenthesized.
; (x + (3 * (x + (y + 2))))
(define (sum? x)
  (and (pair? x) (eq? (cadr x) '+)))

(define (addend e) (car e))

(define (augend e) (caddr e))

(define (make-sum a1 a2)
  (cond ((=number? a1 0) a2)
        ((=number? a2 0) a1)
        ((and (number? a1) (number? a2)) (+ a1 a2))
        (else (list 'a1 + a2))))

(define (product? e)
  (and (pair? e) (eq? (cadr e) '*)))

(define (multiplier e) (car e))

(define (multiplicand e) (caddr e))

(define (make-product m1 m2)
  (cond ((or (=number? m1 0) (=number? m2 0)) 0)
        ((=number? m1 1) m2)
        ((=number? m2 1) m1)
        ((and (number? m1) (number? m2)) (* m1 m2))
        (else (list 'm1 * m2))))

(newline)
(display (deriv '(x + (3 * (x + (y + 2)))) 'x)) ; -> 4
(newline)
(display (deriv '(x + (3 * (x + (y + 2)))) 'y)) ; -> 3

(display "b")
(newline)
; standard algebraic notation
; (x + 3 * (x + y + 2))
(define (sum? x)
  (and (pair? x) (eq? (cadr x) '+)))

(define (addend e) (car e))
(define (augend e) (cddr e))

(define (make-sum a1 a2)
  (cond ((=number? a1 0) a2)
        ((=number? a2 0) a1)
        ((and (number? a1) (number? a2)) (+ a1 a2))
        (else (list 'a1 + a2))))

(define (product? e)
  (and (pair? e) (eq? (cadr e) '*)))

(define (multiplier e) (car e))

(define (multiplicand e) (cddr e))

(define (make-product m1 m2)
  (cond ((or (=number? m1 0) (=number? m2 0)) 0)
        ((=number? m1 1) m2)
        ((=number? m2 1) m1)
        ((and (number? m1) (number? m2)) (* m1 m2))
        (else (list 'm1 * m2))))

