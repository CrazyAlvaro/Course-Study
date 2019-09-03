(define (prime? n)
  (= (smallest-divisor n) n))

(define (smallest-divisor n)
  (find-divisor n 2))

(define (find-divisor n test-divisor)
  (cond ((> (square test-divisor) n) n)
        ((divides? test-divisor n) test-divisor)
        (else (find-divisor n (+ test-divisor 1)))))

(define (divides? a b)
  (= (remainder b a) 0))

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

(search-for-primes 100000000000 100000000093)

;; 100000000003 *** .33999999999999997
;; 100000000019 *** .33999999999999997
;; 100000000057 *** .3400000000000001
;; 100000000063 *** .32999999999999985
;; 100000000069 *** .3400000000000001
;; 100000000073 *** .32000000000000006
;; 100000000091 *** .3799999999999999
;; Search completed

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
; 10007 *** 0.
; 10009 *** 0.
; 10037 *** 0.
; 100003 *** 0.
; 100019 *** 0.
; 100043 *** 0.
; 1000003 *** 0.
; 1000033 *** 1.0000000000000231e-2
; 1000037 *** 0.
; 1000000007 *** 2.9999999999999805e-2
; 1000000009 *** 4.0000000000000036e-2
; 1000000021 *** 4.0000000000000036e-2
; 10000000019 *** .10999999999999988
; 10000000033 *** .10000000000000009
; 10000000061 *** .11000000000000032
; 100000000003 *** .33000000000000007
; 100000000019 *** .34999999999999964
; 100000000057 *** .33000000000000007
; 1000000000039 *** 1.0100000000000002
; 1000000000061 *** 1.0199999999999996
; 1000000000063 *** 1.0100000000000007
