
#lang r5rs

(define tolerance 0.00001)

(define (close-enough? x y)
  (< (abs (- x y)) 0.001))

(define (fixed-point f first-guess)
  (define (close-enough? v1 v2)
    (< (abs (- v1 v2)) tolerance))
  (define (try guess)
    (let ((next (f guess)))
      (if (close-enough? guess next)
        next
        (try next))))
  (try first-guess))

(define dx 0.00001)

(define (deriv g)
  (lambda (x)
    (/ (- (g ( + x dx)) (g x))
       dx)))

(define (newton-transform g)
  (lambda (x)
    (- x (/ (g x) ((deriv g) x)))))

(define (newtons-method g guess)
  (fixed-point (newton-transform g) guess))


(define (square x) (* x x))

(define (sqrt x)
  (newtons-method (lambda (y) (- (square y) x))
                  1.0))


;; 1.40
(define (cube a b c)
  (lambda (x)
    (+ (* x x x)
       (* a (* x x))
       (* b x)
       c)))

;; 1.41
(define (double f)
  (lambda (x) (f (f x))))

(define (inc x) (+ x 1))

(((double (double double)) inc) 5)

;; (double double) -> (double (double x))
;; (double (double double)) -> (double (double (double (double x))))

;; > (((double (double double)) inc) 5)
;; 21

;; 1.42
(define (compose f g)
  (lambda (x) (f (g x))))

((compose square inc) 6)

;; > ((compose square inc) 6)
;; 49

;; 1.43

;; need return a procedure
;; (define (repeated f n)
;;   ;; assert n > 0
;;   (if (= 1 n)
;;     (lambda (x) (f x))
;;     (repeated (compose f f) (- n 1))))

;; Excercise require return a procedure
(define (repeated f n)
  (if (= 1 n)
    f
    (compose (repeated f (- n 1)) f)))

((repeated square 2) 5)

;; 1.44
(define (smooth f)
  (lambda (x)
    (/ (+ (f (- x dx))
          (f x)
          (f (+ x dx)))
       3.0)))

(define (n-fold-smooth f n)
  (repeated smooth n) f)

;; 1.45
;; Well, it seems others provide solution that the times
;; require for average-damp is the floor of (log2 N), no idea why it's this

;; Then I realize we can create a procedure to help us figure out
(define (average x y) (/ (+ x y) 2.0))

(define (average-damp f)
  (lambda (x) (average x (f x))))

(define (nth-root num n average-damp-times)
  (fixed-point
    ((repeated average-damp average-damp-times)
     (lambda (y) (/ num (expt y (- n 1)))))
    1.0))

;; Know  2->1, 3->1, 4->2

; > (nth-root 16 2 1)
; 4.000000000000051
; > (nth-root 8 3 1)
; 1.9999981824788517
; > (nth-root 16 4 1)
; NOT CONVERGE
; > (nth-root 16 4 2)
; 2.0000000000021965
; > (nth-root 32 5 2)
; 2.000001512995761
; > (nth-root 64 6 2)
; 2.0000029334662086
; > (nth-root 128 7 2)
; 2.0000035538623377
; > (nth-root 256 8 2)
; NOT CONVERGE
; > (nth-root 256 8 3)
; 2.0000000000039666
; > (nth-root 512 9 3)
; 1.9999997106840102

;; up to now, let's guess, the significant point is 4 and 8
;; seem to have something to do with pow(2, n),
;; let's try this

; > (nth-root 1000 15 3)
; 1.5848887552366278
; > (nth-root 1000 16 3)
; NOT CONVERGE

;; now, it's not hard to see the pattern,
;; the N times average-damp is applicable up to pow(2,N+1) - 1
;; then comes to N = floor(log2 N)
(define (compute-nth-root x n)
  (fixed-point
    ((repeated average-damp (floor (/ (log n) (log 2))))
     (lambda (y) (/ x (expt y (- n 1)))))
    1.0))

; > (compute-nth-root 16 4)
; 2.0000000000021965
; > (compute-nth-root 32 5)
; 2.000001512995761
; > (compute-nth-root 1000 16)
; 1.5399265260594954

;; 1.46
(define (iterative-improve good-enough? improve)
  (define (improve-help guess)
    (if (good-enough? guess)
      guess
      (improve-help (improve guess))))
  (lambda (x) (improve-help x)))

;; rewrite sqrt
(define (sqrt-new x)
  ((iterative-improve
     (lambda (y) (close-enough? y (/ x y)))
     (average-damp (lambda (y) (/ x y)))) 1.0))

;; rewrite fixed-point
(define (fixed-point-new f first-guess)
  ((iterative-improve
     (lambda (y) (close-enough? y (f y)))
     f) first-guess))

; > (sqrt-new 8)
; 2.8284685718801468
; > (sqrt-new 16)
; 4.000000636692939
; > (fixed-point-new (lambda (y) (+ (sin y) (cos y))) 1.0)
; 1.2583003677191482
