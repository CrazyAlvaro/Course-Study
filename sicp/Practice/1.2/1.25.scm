; Yes, it's correct
;
; Handle long number will slow down the process

(define (expmod base exp m)
  (remainder (fast-expt base exp) m))

(define (fast-expt base exp)
  (cond ((= exp 0) 1)
        ((even? exp) (square (fast-expt base (/ exp 2))))
        (else (* base (fast-expt base (- exp 1))))))

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
; 1013 *** .01
; 1019 *** 0.
; 10007 *** .52
; 10009 *** .51
; 10037 *** .51
;
; remaining are too slow to compute
