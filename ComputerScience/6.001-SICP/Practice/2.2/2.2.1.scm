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
;;(scheme-report-environment -1))  ;; we hope that this will signal an error

(define list-1 (list 1 3 5 7))
(display (list-ref list-1 2))

;; 2.17
(define (last-pair items)
  (if (null? (cdr items))
    items
    (last-pair (cdr items))))

(define nil '())

;; 2.18
(define (reverse items)
  (if (null? items)
    nil
    (append (reverse (cdr items)) (list (car items)))))

;; iterative
(define (reverse-iterative items)
  (define (iter items result)
    (if (null? items)
      result
      (iter (cdr items) (cons (car items) result))))
  (iter items nil))

;; 2.19
;; The order doesn't matter,
(define us-coins (list 50 25 10 5 1))
(define uk-coins (list 100 50 20 10 5 2 1 0.5))

(define (cc amount coin-values)
  (cond ((= amount 0) 1)
        ((or (< amount 0) (no-more? coin-values)) 0)
        (else
          (+ (cc amount
                 (except-first-denomination coin-values))
             (cc (- amount
                    (first-denomination coin-values))
                 coin-values)))))

(define (except-first-denomination items)
  (if (null? items)
    nil
    (cdr items)))

(define (first-denomination items)
  (if (null? items)
    (error "Expect list not to be null")
    (car items)))

(define (no-more? items)
  (if (>= 0 (length items))
    #t
    #f))

;; > (cc 100 us-coins)
;; 292

;; 2.20
;; Could just use filter or select
(define (same-parity int . numbers)
  (define (filter-func int)
    (if (even? int)
      even?
      odd?))
  (define (select filter-func items)
    (cond ((null? items) nil)
          ((filter-func (car items))
           (cons (car items) (select filter-func (cdr items))))
          (else (select filter-func (cdr items)))))
  (cons int (select (filter-func int) numbers)))

;; > (display (same-parity 1 2 3 4 5 6 7))
;; (1 3 5 7)
;; > (display (same-parity 2 3 4 5 6 7))
;; (2 4 6)

;; 2.21
;; (square-list (list 1 2 3 4))
;; (1 4 9 16)
(define (square n) (* n n))

(define (square-list items)
  (if (null? items)
    nil
    (cons (square (car items))
          (square-list (cdr items)))))

(define (square-list-map items)
  (map square items))

(square-list (list 1 2 3 4))
(square-list-map (list 1 2 3 4))

;; 2.22
(define (square-list-reverse items)
  (define (iter things answer)
    (if (null? things)
      answer
      (iter (cdr things)
            (cons (square (car things))
                  answer))))
  (iter items nil))
;; first one doesn't work because the former ones goes to the end

(define (square-list-wrong items)
  (define (iter things answer)
    (if (null? things)
      answer
      (iter (cdr things)
            (cons answer
                  (square (car things))))))
  (iter items nil))
;; the first is nil(car), it not the correct format

;; 2.23
;; cond can handle multiple expression
(define (for-each proc items)
  (cond ((not (null? items))
         (proc (car items))
         (for-each proc (cdr items)))))

(for-each (lambda (x) (newline) (display x))
          (list 57 321 88))

