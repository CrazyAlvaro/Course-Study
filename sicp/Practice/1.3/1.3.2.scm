#lang r5rs
; 1.33

;; filtered-accumulate
(define (filtered-accumulate combiner null-value term a next b filter-predicate?)
  (define (filtered-accum-iter curr result)
    (if (> curr b)
      (combiner result null-value)
      (if (filter-predicate? curr)
        (filtered-accum-iter (next curr)
                             (combiner (term curr) result))
        (filtered-accum-iter (next curr) result))))
  (filtered-accum-iter a null-value))

;; a, the sum of the squares of the prime numbers
(define (sum-of-prime-square a b)
  (filtered-accumulate + 0 square a inc b prime?))

;; b, the product of all the posittive integers less than n that are relatively prime to n
(define (product-of-integers-less-and-prime-to-n n)
  (define (prime-to-n? a)
    (= (gcd a n) 1))
  (filtered-accumulate * 1 identity 1 inc n prime-to-n?))

;; Test
;; no testing at this point

; 1.34
(define (f g) (g 2))

(f f)
(f 2)
(2 2) -> not a procedure

;; application: not a procedure;
;; expected a procedure that can be applied to arguments
;;  given: 2
;;  arguments.:
