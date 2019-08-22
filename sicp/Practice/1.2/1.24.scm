;; (define (prime? n)
;;   (= (smallest-divisor n) n))
;;
;; (define (smallest-divisor n)
;;   (find-divisor n 2))
;;
;; (define (find-divisor n test-divisor)
;;   (cond ((> (square test-divisor) n) n)
;;         ((divides? test-divisor n) test-divisor)
;;         (else (find-divisor n (+ test-divisor 1)))))
;;
;; (define (divides? a b)
;;   (= (remainder b a) 0))

;; computes the exponential of a number modulo another number
(define (expmod base exp m)
  (cond ((= exp 0) 1)
        ((even? exp)
         (remainder (square (expmod base (/ exp 2) m))
                    m))
        (else
          (remainder (* base (expmod base (- exp 1) m))
                     m))))

;; Fermat test
(define (fermat-test n)
  (define (try-it a)
    (= (expmod a n n) a))
  (try-it (+ 1 (random (- n 1)))))

(define (fast-prime? n times)
  (cond ((= times 0) true)
        ((fermat-test n) (fast-prime? n (- times 1)))
        (else false)))

(define (prime? n)
  (fast-prime? n 100))

(define (timed-prime-test n)
  (start-prime-test n (runtime)))

(define (start-prime-test n start-time)
  (if (prime? n)
    (report-prime n (- (runtime) start-time))))

(define (report-prime n elapsed-time)
  (newline)
  (display n)
  (display " *** " )
  (display elapsed-time))

;; search-for-primes
(define (search-for-primes start end)
  (define (search-next start end)
    (if (<= start end) (timed-prime-test start))
    (if (<= start end) (search-next (+ start 2) end)
      (newline)))
  (search-next (if (even? start) (+ start 1) start)
               (if (even? end) (- end 1) end))
  (display "Search completed"))

(timed-prime-test 1009)
(timed-prime-test 1013)
(timed-prime-test 1019)
(timed-prime-test 10007)
(timed-prime-test 10009)
(timed-prime-test 10037)
(timed-prime-test 100003)
(timed-prime-test 100019)
(timed-prime-test 100043)
(timed-prime-test 1000003)
(timed-prime-test 1000033)
(timed-prime-test 1000037)
(timed-prime-test 1000000007)
(timed-prime-test 1000000009)
(timed-prime-test 1000000021)
(timed-prime-test 10000000019)
(timed-prime-test 10000000033)
(timed-prime-test 10000000061)
(timed-prime-test 100000000003)
(timed-prime-test 100000000019)
(timed-prime-test 100000000057)
(timed-prime-test 1000000000039)
(timed-prime-test 1000000000061)
(timed-prime-test 1000000000063)

; 1009 *** 0.
; 1013 *** 0.
; 1019 *** 0.
; 10007 *** .01
; 10009 *** 0.
; 10037 *** 0.
; 100003 *** 0.
; 100019 *** 9.999999999999998e-3
; 100043 *** 0.
; 1000003 *** 0.
; 1000033 *** 1.0000000000000002e-2
; 1000037 *** 0.
; 1000000007 *** 1.0000000000000002e-2
; 1000000009 *** 0.
; 1000000021 *** 9.999999999999995e-3
; 10000000019 *** 1.0000000000000009e-2
; 10000000033 *** 9.999999999999995e-3
; 10000000061 *** 9.999999999999995e-3
; 100000000003 *** 1.0000000000000009e-2
; 100000000019 *** 0.
; 100000000057 *** 9.999999999999995e-3
; 1000000000039 *** 9.999999999999995e-3
; 1000000000061 *** 1.0000000000000009e-2
; 1000000000063 *** 1.0000000000000009e-2

; Since we test 100 times for all number, time doesn't diff a lot between
; numbers, they seem all close to each other, 100 Log(n), log(n) increase very slow
; For large number, it has significant difference between Log(n) and sqrt(n)
