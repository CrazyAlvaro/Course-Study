#lang racket
; data-directed programming

; dispatch on tag

; -> maintaining a table to index each procedure with several dimension key, no need to change the existing procedure

(display "2.4.3")
(display "Exercise 2.73")
(define (derive exp var)
  (cond ((number? exp) 0)
        ((variable? exp) (if (same-variable? exp var) 1 0))
        (else ((get 'deriv (operator exp)) (operands exp)
                                           (var)))))

(define (operator exp) (car exp))

(define (operands exp) (cdr exp))

; a, we dispatch number and single variable, then use data-directed style to invoke
; specific procedure to perfrom operation, since there's no operator for number and single variable

; b
(define (install-sum-deriv)
  ;; internal procesure
  (define (addend exp)
    (car exp))
  (define (augend exp)
    (cdr exp))
  (define (sum-deriv operands var)
    (make-sum (deriv (addend operands) var)
              (deriv (augend operands) var)))

  ;; interface to the rest of the system
  (put 'deriv '+ sum-deriv)
  'done)

(define (install-product-deriv)
  ;; internal procedure
  (define (multiplicand exp)
    (car exp))
  (define (multiplier exp)
    (cdr exp))
  (define (product-deriv operands var)
    (make-sum
      (make-product (multiplicand operands)
                    (deriv (multiplier operands) var))
      (make-product (deriv (multiplicand operands) var)
                    (multiplier operands))))

  ;; interface to the rest of the system
  (put 'deriv '* product-deriv)
  'done)

; c
(define (install-exponent)
  (define (base exp)
    (car exp))
  (define (exponent exp)
    (cdr exp))
  (define (exponent-deriv operands var)
    (make-product (exponent operands)
                  (make-product
                    (make-exponentiation
                      (base operands)
                      (- (exponent operands) 1))
                  (deriv (base operands) var))))

  ;; interface to the rest of the system
  (put 'deriv '** exponent-deriv)
  'done)

; d
; only the put method on each install procedure need change

(display "Exercise 2.74")
; a b c
(define (get-record person-file)
  (apply-generic 'get-record person-file))

(define (get-salary record)
  (apply-generic 'get-salary record))

(define (find-employee-record employee-name files)
  (if (null? files)
      '()
      (let ((record (car files)))
        (if ((apply-generic 'match-name record) employee-name record)
            record
            (find-employee-record employee-name (cdr files))))))

;; individual division file
(define (install-divisionA-package)
  ;; internal procesures
  (define (get-record file)
    ('implementation))
  (define (get-salary record)
    ('implementation))
  (define (make-person-file info)
    ('implementation))
  (define (make-record info)
    ('implementation))
  (define (match-name name record)
    ('implementation))

  (define (tag x) (attach-tag 'divisionA x))
  (put 'get-record 'divisionA get-record)
  (put 'get-salary 'divisionA get-salary)
  (put 'match-name 'divisionA match-name)
  (put 'make-person-file 'divisionA
    (lambda (info) (tag (make-person-file info))))
  (put 'make-record 'divisionA
    (lambda (info) (tag (make-record info))))
  'done)

; d
; install its own tagged procedure

; Message passing

(display "Exercise 2.75")
(define (make-from-mag-ang mag ang)
  (define (dispatch op)
    (cond ((eq? op 'real-part) (* mag (cos ang)))
          ((eq? op 'imag-part) (* mag (sin ang)))
          ((eq? op 'magnitude) mag)
          ((eq? op 'angle) ang)
          (else
            (error "Unkown op -- MAKE_FROM_MAG_ANG" op))))
  dispatch)


(display "Exercise 2.76")
; generic operation with explicit dispatch
;type added: every procedure need to changed, since we dispatch on types
;operation added: not much pain through, only need to add operation on different type, and have a dispatch procedure

; data-directed style
;type added: central procedure don't have to change, only this type need to install it to procedure table
;operation added: only need to install this specific operation, and central system as well

; message-passing-style
;type added: only this type specific operation need to be added
;operation added: every procedure has to be added new procedure


; 1 new type must often be added: I will choose either data-directed or message-passing-style

; 2 new operations must often be added: then I think any of the three need to change quite a bit,
; but the data-directed seems to have less impact on existing operations, so I will choose this one
