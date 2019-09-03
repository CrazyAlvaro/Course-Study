(define (next n)
  (cond ((= n 2) 3)
        (else (+ n 2))))

(define (prime? n)
  (= (smallest-divisor n) n))

(define (smallest-divisor n)
  (find-divisor n 2))

(define (find-divisor n test-divisor)
  (cond ((> (square test-divisor) n) n)
        ((divides? test-divisor n) test-divisor)
        (else (find-divisor n (next test-divisor)))))

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

(search-for-primes 100000000000 100000000053)

;; 100000000003 *** .36
;; 100000000019 *** .37
;; Search completed


;; Ratio is around 1.61 less than 2
;; one potential explaination is that other operations also consume some time,
;; like print to stdout, that time is not changed, so overal improvement should
;; be less then ratio of 2, (only part of the time is half of original, overall
;; should be more than half of original)
