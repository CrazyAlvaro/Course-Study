; a <- a + b
; b <- a
;
; This is a transformation, to n times
;
; a <- bq + aq + ap
; b <- bp + aq
;
;
; p = 0, q = 1


; p' = sqrt(p) + sqrt(q)
; q' = sqrt(q) + 2pq

(define (fib n)
  (fib-iter 1 0 0 1 n))

(define (fib-iter a b p q count)
  (cond ((= count 0) b)
        ((even? count)
         (fib-iter a
                   b
                   (+ (square p) (square q))
                   (+ (square q) (* 2 p q))
                   (/ count 2)))
        (else (fib-iter (+ (* b q) (* a q) (* a p))
                        (+ (* b p) (* a q))
                        p
                        q
                        (- count 1)))))
