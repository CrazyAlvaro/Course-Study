(define (expmod base exp m)
  (cond ((= exp 0) 1)
        ((even? exp)
         (remainder (* (expmod base (/ exp 2) m)
                       (expmod base (/ exp 2) m))
                    m))
        (else
          (remainder (* base (expmod base (- exp 1) m))
                     m))))

; instead of using square, this compute (expmod base (/ exp 2) m) twice,
; (expmod base n m) = 2 * (expmod base (/ n 2) m)
; then the procedure grow O(N) other than O(logN),
; it's a tree recursion instead of a linear recursion
