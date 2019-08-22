#lang r5rs

;; error function
(define (error reason . args)
  (display "Error: ")
  (display reason)
  (for-each (lambda (arg)
              (display " ")
              (write arg))
            args)
  (newline))

(display "Streams and Delayed Evaluation")
(define (integral delayed-integrand initial-value dt)
  (define int
    (cons-stream initial-value
                 (let ((integrand (force delayed-integrand)))
                   (add-streams (scale-stream integrand dt)
                                int))))
  int)

(define (solve f y0 dt)
  (define y (integral (delay dy) y0 dt))
  (define dy (stream-map f y))
  y)

(newline)
(display "Exercise 3.77")
(define (integral delayed-integrand initial-value dt)
  (cons-stream initial-value
              (let ((integrand (force delayed-integrand)))
                (if (stream-null? integrand)
                    the-empty-stream
                    (integral (delay (stream-cdr integrand))
                              (+ (* dt (stream-car integrand))
                                 initial-value)
                              dt))))

(newline)
(display "Exercise 3.78")
(define (solve-2nd a b dt y0 dy0)
  (define y (integral (delay dy) y0 dt))
  (define dy (integral (delay ddy) dy0 dt))
  (define ddy (add-streams
                (scale-stream dy a)
                (scale-stream y b)))
  y)

(newline)
(display "Exercise 3.79")
(define (sovle-2nd-gen dt y0 dy0 f)
  (define y (integral (delay dy) y0 dt))
  (define dy (integral (delay ddy) dy0 dt))
  (define ddy (stream-map f dy y))
  y)

(newline)
(display "Exercise 3.80")
(define (RLC R L C dt)
  (lambda (vc0 il0)
    (define vc (integral (delay dvc) vc0 dt))
    (define dvc (scale-stream il (/ -1 C)))
    (define il (integral (delay dil) il0 dt))
    (define dil
      (add-streams
        (scale-stream vc (/ 1 L))
        (scale-stream il (/ (- 0 R) L))))
    (cons vc il)))
