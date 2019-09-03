;; 1.2
(/
  (+ 5 4
     (- 2
        (- 3
           (+ 6 (/ 4 5)))))
  (* 3
     (- 6 2)
     (- 2 7)))

;; 1.3
(define (square a) (* a a))

(define (square-of-larger-two a b c)
  (cond ((> a b) (+ (square a)
                    (cond ((> c b) (square c))
                          (else (square b)))))
        (else (+ (square b)
                 (cond ((> a c) (square a))
                       (else (square c)))))))

;; 1.4

;; If b is positive, a + b, else a - b

;; 1.5

;; (define (p) (p))
;;
;; (define (test x y)
;;    (if (= x 0)
;;        0
;;        y))


;;(test 0 (p))
;; applicative-order( evaluate both operator and operands at the same time after substitution )
;; evaluate both test and (p), got an error,
;; because (p) is infinitely expanded to itself

;; normal-order( substitue operands expression until it got all primitive operators then evaluate)
;; (if (= 0 0)
;;      0
;;      (p))
;; 0 return
;;

