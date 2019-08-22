;; the row: i and col: j element
(define (pascal_element i j)
  (cond ((= j 0) 1)
        ((= j i) 1)
        (else (+ (pascal_element (- i 1) j)
                 (pascal_element (- i 1) (- j 1))))))
