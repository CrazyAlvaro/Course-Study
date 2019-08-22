(define (f-recursive n)
  (cond ((< n 3) n)
        (else (+ (f-recursive (- n 1))
                 (* 2 (f-recursive (- n 2)))
                 (* 3 (f-recursive (- n 3)))))))

(define (f n)
  (cond ((< n 3) n)
        (else (f-iter 0 1 2 n))))

(define (f-iter a b c count)
  (cond ((= count 0) a)
        (else (f-iter b c (+ (* 3 a) (* 2 b) c) (- count 1)))))
