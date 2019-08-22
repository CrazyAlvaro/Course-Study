#lang r5rs
(define (dis arg)
  (newline)
   (display arg))

;; error function
(define (error reason . args)
  (display "Error: ")
  (display reason)
  (for-each (lambda (arg)
              (display " ")
              (write arg))
            args)
  (newline))

(display "Exercise 3.7")
(define (make-account balance pass-origin)
  (define (withdraw amount)
    (if (>= balance amount)
        (begin (set! balance (- balance amount))
               balance)
        "Insufficient funds"))

  (define (deposit amount)
    (set! balance (+ balance amount))
    balance)

  (define (make-joint another-pass)
    (dispatch another-pass))

  (define (dispatch password)
    (lambda (pass m)
      (if (eq? pass password)
        (cond ((eq? m 'withdraw) withdraw)
              ((eq? m 'deposit) deposit)
              ((eq? m 'make-joint) make-joint)
              (else (error "Unknown request -- MAKE-ACCOUNT"
                           m)))
        (lambda (x)
          "Incorrect password"))))

  (dispatch pass-origin))

(define (make-joint origin-acc origin-pass ano-pass)
  ((origin-acc origin-pass 'make-joint) ano-pass))

; Test
(define acc (make-account 100 'mypass))
(dis ((acc 'mypass 'withdraw) 40))
(dis ((acc 'incorrect 'withdraw) 50))
(define ano-acc (make-joint acc 'mypass 'newpass))
(dis ((ano-acc 'newpass 'withdraw) 10))
(dis ((ano-acc 'incorrect 'withdraw) 10))
(dis ((acc 'mypass 'withdraw) 10))

(newline)
(display "Exercise 3.8")
(define m
  (let ((called #f))
    (lambda (x)
      (if called
        0
        (begin
          (set! called #t)
          x)))))

(define n
  (let ((called #f))
    (lambda (x)
      (if called
        0
        (begin
          (set! called #t)
          x)))))
(newline)
(display (+ (m 0) (m 1)))
(newline)
(display (+ (n 1) (n 0)))
