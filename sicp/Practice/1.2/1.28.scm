(define (miller-rabin n)
  (miller-rabin-test (- n 1) n))

; test all integer less than n
(define (miller-rabin-test a n)
  (cond ((= a 0) #t)
        ((= (expmod a (- n 1) n) 1) (miller-rabin-test (- a 1) n))
        (else #f)))


(define (expmod base exp m)
  (cond ((= exp 0) 1)
        ((even? exp)
         (let ((x (expmod base (/ exp 2) m)))
           ; indicate a nontrivial-square-root? found by return 0
           (if (nontrivial-square-root? x m) 0 (remainder (square x) m))))
        (else
          (remainder (* base (expmod base (- exp 1) m))
                     m))))

; a number not equal to 1 or n - 1 whose square is congruent to 1 modulo n (book is incorrect)
(define (nontrivial-square-root? a n)
  (cond ((= a 1) #f)
        ((= a (- n 1)) #f)
        (else (= (remainder (square a) n) 1))))

(display (miller-rabin 2)   ) ;#t
(display (miller-rabin 3)   ) ;#t
(display (miller-rabin 4)   ) ;#f
(display (miller-rabin 5)   ) ;#t
(display (miller-rabin 7)   ) ;#t
(display (miller-rabin 561) ) ;#f
(display (miller-rabin 1105)) ;#f
(display (miller-rabin 1729)) ;#f
