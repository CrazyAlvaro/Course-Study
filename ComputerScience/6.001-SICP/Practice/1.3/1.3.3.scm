#lang r5rs

; 1.35

;;f -> 1 + 1/x
;;
;;x = 1 + 1/x -> x = (1 + sqrt(5))/2

(define tolerance 0.00001)
(define (fixed-point f first-guess)
  (define (close-enough? v1 v2)
    (< (abs (- v1 v2)) tolerance))
  (define (try guess)
    (let ((next (f guess)))
      (if (close-enough? guess next)
        next
        (try next))))
  (try first-guess))

(fixed-point (lambda (x) (+ 1 (/ 1 x))) 1.0)

;; > (fixed-point (lambda (x) (+ 1 (/ 1 x))) 1.0)
;; 1.6180327868852458

; 1.36
(define (inc n) (+ n 1))

(define tolerance 0.00001)
(define (fixed-point f first-guess)
  (define (close-enough? v1 v2)
    (< (abs (- v1 v2)) tolerance))
  (define (print-result counter result)
    (display "Number of steps: ")
    (display counter)
    (display " Result: ")
    (display result))
  (define (try guess counter)
    (let ((next (f guess)))
      (if (close-enough? guess next)
        (print-result counter next)
        (try next (inc counter)))))
  (try first-guess 1))

(display "Regular: ")
(fixed-point (lambda (x) (/ (log 1000) (log x))) 2)

; Number of steps: 34 Result: 4.555532270803653

(newline)
(display "With average damping: ")
(define (average x y) (/ (+ x y) 2.0))
; With average damping
(fixed-point (lambda (x) (average x (/ (log 1000) (log x)))) 2)
; Number of steps: 9 Result: 4.555537551999825

;; Exercise 1.37

(define (inc k) (+ k 1))

(define (cont-frac n d k)
  (define (frac-term count)
    (if (> count k)
      0
      (/ (n count)
         (+ (d count) (frac-term (inc count))))))
  (frac-term 1))


(define (close-enougth? x y)
  (< (abs (- x y)) 0.0001))

(define golden-ratio
  (/ (+ 1 (sqrt 5))
     2))

(define (try k)
  (if (close-enougth?
        (cont-frac (lambda (i) 1.0)
                   (lambda (i) 1.0)
                   k)
        (/ 1.0 golden-ratio))
    (display k)
    (try (inc k))))

(try 1)

; 10

(define (dec n) (- n 1))

(define (cont-frac-iter n d k)
  (define (term count)
    (/ (n count) (d count)))
  (define (cont-step k result)
    (if (< k 1)
      result
      (cont-step (dec k)
                 (/ (n k)
                    (+ (d k) result)))))
  (cont-step k 0))

(cont-frac-iter (lambda (i) 1.0)
                (lambda (i) 1.0)
                10)

; 0.6179775280898876

;; Exercise 1.38

(define (natural-number n)
  (+ 2
     (cont-frac (lambda (i) 1.0)
                (lambda (i)
                  (if (= (remainder i 3) 2)
                    (* 2 (/ (+ i 1) 3))
                    1))
                n)))

(natural-number 100)

; > (natural-number 100)
; 2.7182818284590455

;; Exercise 1.39
(define (tan-cf x k)
  (cont-frac (lambda (i)
               (if (= i 1) x (- (* x x))))
             (lambda (i)
               (- (* i 2.0) 1))
             k))
