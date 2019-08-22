;; 1.17
(define (* a b)
  (define (double a) (+ a a))
  (define (halve a) (/ a 2))
  (cond ((= b 0) 0)
        ((even? b) (* (double a) (halve b)))
        (else (+ a (* a (- b 1))))))

;; 1.18
(define (* a b)
  (define (double a) (+ a a))
  (define (halve a) (/ a 2))

  (define (fast-multiplication a b sum )
    (cond ((= 0 b) sum)
          ((even? b) (fast-multiplication (double a) (halve b) sum))
          (else (fast-multiplication a (- b 1) (+ sum a)))))

  (fast-multiplication a b 0))

;; Test
(* 2 32)
(* 3 21)
(* 2 0)
(* 0 3)
