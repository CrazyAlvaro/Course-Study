#lang r5rs
;(define (fast-expt b n)
;  (cond ((= n 0) 1)
;        ((even? n) (square (fast-expt b (/ n 2))))
;        (else (* b (fast-expt b (- n 1))))))

(define (even? n)
  (= (remainder n 2) 0))


(define (fast-expt-iter b n)
  (expt-iter 1 b n))

;; have a product ab**n is unchanged from state to state
(define (expt-iter a b n)
  (cond ((= n 0) a)
        ((even? n) (expt-iter a (square b) (/ n 2)))
        (else (expt-iter (* a b) b (- n 1)))))

;; Test
(define (square x)
  (* x x))

(fast-expt-iter 2 0)
(fast-expt-iter 2 1)
(fast-expt-iter 2 2)
(fast-expt-iter 2 3)
(fast-expt-iter 2 10)
