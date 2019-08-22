#lang r5rs

; 1.29
(define (cube x) (* x x x))

(define (inc n) (+ n 1))

(define (sum term a next b)
  (if (> a b)
    0
    (+ (term a )
       (sum term (next a) next b))))

;;(define (simpson-integral f a b n)
;;  (define h (/ (- b a) n))
;;  (define (yk n)
;;    (f (+ a
;;          (* n h))))
;;  (define (simpson-sum a b term count n)
;;    (if (> count n)
;;      0
;;      (cond ((or (= 1 count) (= n count))
;;             (+ (yk count)
;;                (simpson-sum a b term (+ count 1) n)))
;;            ((= 0 (remainder count 2))
;;             (+ (* 2 (yk count))
;;                (simpson-sum a b term (+ count 1) n)))
;;            (else
;;             (+ (* 4 (yk count))
;;                (simpson-sum a b term (+ count 1) n))))))
;;  (* (/ h 3.0)
;;     (simpson-sum a b f 0 n)))

;; revise condition with more elegant way and using regular sum
(define (simpson-integral f a b n)
  (define h (/ (- b a) n))
  (define (yk k)
    (f (+ a (* k h))))
  (define (simpson-term k)
    (* (yk k)
       (cond ((or (= k 0) (= k n))
              1)
             ((= 1 (remainder k 2))
              4)
             (else 2))))
  (* (/ h 3.0)
     (sum simpson-term 0 inc n)))

;; > (simpson-integral cube 0 1 100)
;; 0.25
;; > (simpson-integral cube 0 1 1000)
;; 0.25

;; Another way is to seperate y0 yn with the others

; 1.30
(define (sum term a next b)
  (define (iter a result)
    (if (> a b)
      result
      (iter (next a) (+ result (term a)))))
  (iter a 0))

; 1.31
;; iterative
(define (product term a next b)
  (define (product-iter a result)
    (if (> a b)
      result
      (product-iter (next a) (* (term a) result))))
  (product-iter a 1))

;; recursive
(define (product-rec term a next b)
  (if (> a b)
    1
    (* (term a)
       (product-rec term (next a) next b))))

(define (inc n) (+ n 1))

(define (identity k) k)

(define (factorial n)
  (product identity 1 inc n))

(define (square k) (* k k))

;; compute pi
(define (pi k)
  (define (pi-term k)
    (if (even? k)
      (/ (+ k 2) (+ k 1))
      (/ (+ k 1) (+ k 2))))
  (* 4.0 (product pi-term 1 inc k)))

;; > (pi 100)
;; 3.1570301764551676
;; > (pi 1000)
;; 3.1431607055322663

; 1.32


;; Recursive
(define (accumulate combiner null-value term a next b)
  (if (> a b)
    null-value
    (combiner (term a)
              (accumulate combiner null-value term (next a) next b))))

;; Iterative
(define (accumulate-iterative combiner null-value term a next b)
  (define (accumulate-iter curr result)
    (if (> curr b)
      result
      (accumulate-iter (next curr) (combiner (term curr) result))))
  (accumulate-iter a null-value))

;; Product
(define (product term a next b)
  (accumulate * 1 term a next b))

;; Sum
(define (sum term a next b)
  (accumulate + 0 term a next b))

(define (sum-iter term a next b)
  (accumulate-iterative + 0 term a next b))

(define (inc x) (+ x 1))

;; simpson-integral for testing
(define (simpson-integral f a b n)
  (define h (/ (- b a) n))
  (define (yk k)
    (f (+ a (* k h))))
  (define (simpson-term k)
    (* (yk k)
       (cond ((or (= k 0) (= k n))
              1)
             ((= 1 (remainder k 2))
              4)
             (else 2))))
  (* (/ h 3.0)
     (sum simpson-term 0 inc n)))

(define (cube x) (* x x x))

;; > (sum cube 1 inc 3)
;; 36
;; > (sum-iter cube 1 inc 3)
;; 36

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
