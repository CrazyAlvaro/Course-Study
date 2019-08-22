#lang r5rs
;; 2.1 A better version of make-rat, normalize the sign
(define (make-rat n d)
  (let ((g ((if (> d 0) + -) (gcd n d))))
    (cons (/ n g) (/ d g))))

;; 2.2
;; Make a point
(define (make-point x y) (cons x y))

(define (x-point point) (car point))

(define (y-point point) (cdr point))

;; Make a segment
(define (make-segment start end)
  (cons start end))

(define (start-segment segment)
  (car segment))

(define (end-segment segment)
  (cdr segment))

(define (average a b)
  (/ (+ a b) 2))

(define (midpoint-segment segment)
  (let ((s-point (start-segment segment))
        (e-point (end-segment segment)))
    (make-point (average (x-point s-point)
                         (x-point e-point))
                (average (y-point s-point)
                         (y-point e-point)))))

(define (print-point p)
  (newline)
  (display "(")
  (display (x-point p))
  (display ",")
  (display (y-point p))
  (display ")"))

;; Test
(define point-a (make-point 3 2))
(define point-b (make-point 5 8))
(define point-c (make-point 9 0))
(define point-d (make-point 1 2))

(define seg-a (make-segment point-a point-b))
(define seg-b (make-segment point-c point-d))

(print-point point-a)
(print-point point-b)
(print-point (midpoint-segment seg-a))

;; (3,2)
;; (5,8)
;; (4,5)

(define (square x)
  (* x x))

(define (segment-length segment)
  (let ((point-a (car segment))
        (point-b (cdr segment)))
    (sqrt (+ (square (- (car point-a) (car point-b)))
             (square (- (cdr point-a) (cdr point-b)))))))

;; 2.3
;; Rectangl, define with left and up segment (including two points)

(define (make-rectangle left-seg right-seg)
  (cons left-seg right-seg))

(define (rectangle-perimeter rectangle)
  (* 2 (+ (segment-length (car rectangle))
          (segment-length (cdr rectangle)))))

(define (rectangle-area rectangle)
  (* (segment-length (car rectangle))
     (segment-length (cdr rectangle))))

;; another representation for rectangle
;; (define (make-rectangle up-seg down-seg)
;;   (cons up-seg down-seg))

(define up-left    (make-point 0 5))
(define up-right   (make-point 4 5))
(define down-left  (make-point 0 0))
(define down-right (make-point 4 0))
(define my-rec
  (make-rectangle (make-segment up-left down-left)
                  (make-segment up-left up-right)))

(define (print-rec rec)
  (newline)
  (display "Length: ")
  (display (segment-length (car rec)))
  (display " Width : ")
  (display (segment-length (cdr rec))))

(print-rec my-rec)

(newline)
(display (rectangle-area my-rec))
(newline)
(display (rectangle-perimeter my-rec))

;; 2.4
;; (car (cons x y))
;; -> (car (lambda (m) (m x y)))
;; -> ((lambda (m) (m x y)) (lambda (p q) p))
;; Consider (lambda (p q) p) as (m) pass in first lambda function
;; -> (((lambda(p q) p) x y))
;; -> (x)
;; (define (cdr z)
;;   (z (lambda (p q) q)))

;; 2.5
(define (my-cons x y)
  (* (expt 2 x)
     (expt 3 y)))

(define (my-car pair)
  (define (help pair a)
    (cond ((= 0 (remainder pair 2))
           (help (/ pair 2) (+ a 1)))
          (else a)))
  (help pair 0))

(define (my-cdr pair)
  (define (help pair b)
    (cond ((= 0 (remainder pair 3))
           (help (/ pair 3) (+ b 1)))
          (else b)))
  (help pair 0))

;; Test
(newline)
(display (my-cons 3 4))
(newline)
(display (my-car (my-cons 3 4)))
(newline)
(display (my-cdr (my-cons 3 4)))
(newline)

;; 2.6
(define (inc n) (+ n 1))

(define zero (lambda (f) (lambda (x) x)))

;; n times
(define (add-1 n)
  (lambda (f)
    (lambda (x)
      (f ((n f) x)))))

;; > ((zero inc) 0)
;; 0
;; > ((zero inc) 3)
;; 3

(add-1 zero)
(add-1 (lambda (f) (lambda (x) x)))
(lambda (f) (lambda (x) (f (((lambda (f) (lambda (x) x)) f) x))))
(lambda (f) (lambda (x) (f ((lambda (x) x) x))))
(lambda (f) (lambda (x) (f x)))

;; Show as example
;; (define one (add-1 zero))
;; (define two (add-1 one))
;; > ((one inc) 1)
;; 2
;; > ((one inc) 5)
;; 6
;; > ((two inc) 4)
;; 6
;; > ((two inc) 8)
;; 10

;; apply f once
(define one (lambda (f) (lambda (x) (f x))))

;; Also can being applicative from (add-1 one)
(define two (lambda (f) (lambda (x) (f (f x)))))

(define (add-church m n)
  (lambda (f) (lambda (x) ((m f) ((n f) x)))))

;; > (((add-church one two) inc) 8)
;; 11


;; functions show in textbook

(define (add-interval x y)
  (make-interval (+ (lower-bound x) (lower-bound y))
                 (+ (upper-bound x) (upper-bound y))))

(define (mul-interval x y)
  (let ((p1 (* (lower-bound x) (lower-bound y)))
        (p2 (* (lower-bound x) (upper-bound y)))
        (p3 (* (upper-bound x) (lower-bound y)))
        (p4 (* (upper-bound x) (upper-bound y))))
    (make-interval (min p1 p2 p3 p4)
                   (max p1 p2 p3 p4))))


(define (div-interval x y)
  (mul-interval
    x
    (make-interval (/ 1.0 (upper-bound y))
                   (/ 1.0 (lower-bound y)))))

;; 2.7
;; lower bound, upper bound
(define (make-interval a b)
  (cons a b))

(define (upper-bound interval)
  (cdr interval))

(define (lower-bound interval)
  (car interval))

;; 2.8
;; Lower-bound is lower of x - upper of y
;; Upper-bound is upper of x - lower of y
(define (sub-interval x y)
  (make-interval (- (lower-bound x)
                    (upper-bound y))
                 (- (upper-bound x)
                    (lower-bound y))))

;; 2.9
;; definition of interval width
(define (interval-width interval)
  (/ (- (upper-bound interval)
        (lower-bound interval))
     2))

(define interval-1 (make-interval 1.5 5.5))
(define interval-2 (make-interval 5.5 9.5))
(define interval-3 (make-interval 3.5 8.5))
(define interval-4 (make-interval 0.5 6.5))

;; For sum or difference, it's the same, sum of the original width
(interval-width (sub-interval interval-1 interval-2))
(interval-width (add-interval interval-1 interval-2))
(+ (interval-width interval-1) (interval-width interval-2))

;; (interval-width (sub-interval interval-1 interval-2))
;; (interval-width (add-interval interval-1 interval-2))
;; (+ (interval-width interval-1) (interval-width interval-2))
;; 4.0
;; 4.0
;; 4.0


;; For multiplication or division, it's not of function of
;; arguments
(interval-width (mul-interval interval-1 interval-2))
(interval-width (div-interval interval-1 interval-2))

;; (interval-width (mul-interval interval-1 interval-2))
;; (interval-width (div-interval interval-1 interval-2))
;; 22.0
;; 0.42105263157894735

;; error function
(define (error reason . args)
  (display "Error: ")
  (display reason)
  (for-each (lambda (arg)
              (display " ")
              (write arg))
            args)
  (newline))
  ;;(scheme-report-environment -1))  ;; we hope that this will signal an error

;; 2.10
(define (span-zero interval)
  (if (>= 0 (* (lower-bound interval) (upper-bound interval)))
    #t
    #f))

(define (div-interval-message x y)
  (if (span-zero y)
    (error "Division error (interval spans 0)" y)
    (mul-interval
      x
      (make-interval (/ 1.0 (upper-bound y))
                     (/ 1.0 (lower-bound y))))))

(define interval-0 (make-interval -1 2))
(div-interval-message interval-1 interval-0)

;; 2.11
;; Nine cases: 0 could be on the left, right or in between of two endpoints
;; 3 * 3 = 9

;;  x    y          min                     max
;;  - -  - -        ux * uy                 lx * ly
;;  - -  - +        lx * uy                 lx * ly
;;  - -  + +        lx * uy                 ux * ly
;;  - +  - -        ux * uy                 lx * ly
;;  - +  - +        min(lx * uy, ux * ly)   max(lx * ly, ux * uy)
;;  - +  + +        lx * uy                 ux * uy
;;  + +  - -        ux * uy                 lx * ly
;;  + +  - +        ux * ly                 ux * uy
;;  + +  + +        lx * ly                 ux * uy

(define (interval-case interval)
  (cond ((and (< (lower-bound interval) 0) (< (upper-bound interval) 0))
         1)
        ((and (< (lower-bound interval) 0) (> (upper-bound interval) 0))
         2)
        ((and (> (lower-bound interval) 0) (> (upper-bound interval) 0))
         3)))

;; (define (mul-interval x y)
;;   ;; nine cases
;;   (cond () ()))

;; 2.12
(define (center i)
  (/ (+ (lower-bound i) (upper-bound i)) 2))

(define (width i)
  (/ (- (upper-bound i) (lower-bound i)) 2))

(define (make-center-percent center percent-tolerance)
  (let ((width (* center percent-tolerance)))
    (make-interval (- center width) (+ center width))))

(define (percent interval)
  (/ (width interval) (center interval)))

;; 2.13
(define interval-s-1 (make-center-percent 2.5 0.01))
(define interval-s-2 (make-center-percent 5.5 0.01))

(percent (mul-interval interval-s-1 interval-s-2))
;; 0.0199980001999799

;; Make a guess, percent = percent 1 + percent 2
(define interval-s-3 (make-center-percent 2.5 0.007))
(define interval-s-4 (make-center-percent 5.5 0.003))
(percent (mul-interval interval-s-3 interval-s-4))
(percent (mul-interval interval-s-2 interval-s-4))
;; 0.00999979000440992
;; 0.012999610011699593

;; So percent new = percent 1 + percent 2
;; From mathmatics: (x + &a)*(y + &b) = xy + &ay + &bx + &a&b
;; new percent = &a/x + &b/y = percent 1 + percent 2

;; 2.14
(define (par1 r1 r2)
  (div-interval (mul-interval r1 r2)
                (add-interval r1 r2)))

(define (par2 r1 r2)
  (let ((one (make-interval 1 1)))
    (div-interval
      one (add-interval (div-interval one r1)
                        (div-interval one r2)))))

(define val-1 (make-center-percent 2.0 0.02))
(define val-2 (make-center-percent 5.0 0.015))

(display (par1 val-1 val-2))
(newline)
(display (par2 val-1 val-2))

;; Two intervals are very different
;; (1.35671117357695 . 1.5037037037037038)
;; (1.4020334059549744 . 1.4550948699929727)

;; Explaination:
;; par1 has more computation to exagerate the precision,

(newline)
(display "Identity is not 1.0")
(newline)
(display val-1)
(newline)
(display (div-interval val-1 val-1))
(newline)
(display (div-interval val-1 val-2))

;; 2.15
;; Yes, I think she's right

;; 2.16
;; I think to solve this problem is beyong my expection from learning this textbook :)
