(define (A x y)
  (cond ((= y 0) 0)
        ((= x 0) (* 2 y))
        ((= y 1) 2)
        (else (A (- x 1)
                 (A x (- y 1))))))

(A 1 10)
;; 2*(A 1 9)
;; 2*2*(A 1 8)
;; ...
;; 2 to 10 = 1024

(A 2 4)
;; (A 1
;;    (A 2 3))
;; (A 1
;;    (A 1
;;       (A 2 2)))
;; (A 1
;;    (A 1
;;       (A 1
;;          (A 2 1))))
;; (A 1
;;    (A 1
;;       (A 1
;;          2))) ;; = 2**2**2**2


(A 3 3)
;; (A 2
;;    (A 3 2))
;; (A 2
;;    (A 2
;;       (A 3 1)))
;; (A 2
;;    (A 2 2))   ;; (A 2 2) -> 2**2 = 4
;; (A 2 4)       ;; (A 2 4) -> 2**2**2**2

(f n) 2n

(g n) 2**n

(h n) (** 2 2 2 ... 2) (n times)