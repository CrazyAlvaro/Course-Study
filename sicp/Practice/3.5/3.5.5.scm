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

(display "Modularity of Functional Programs and Modularity of Objects")
(define remainder
  (let ((x random-init))
    (lambda ()
      (set! x (rand-update x))
      x)))

(define random-numbers
  (cons-stream random-init
               (stream-map rand-update random-numbers)))

(define cesaro-stream
  (map-successive-pairs (lambda (r1 r2) (= (gcd r1 r2) 1))
                        random-numbers))

(define (map-successive-pairs f s)
  (cons-stream
    (f (stream-car s) (stream-car (stream-cdr s)))
    (map-successive-pairs f (stream-cdr (stream-cdr s)))))

(define (monte-carlo experiment-stream passed failed)
  (define (next passed failed)
    (cons-stream
      (/ passed (+ passed failed))
      (monte-carlo
        (stream-cdr experiment-stream) passed failed)))
  (if (stream-car experiment-stream)
      (next (+ passed 1) failed)
      (next passed (+ failed 1))))

(define pi
  (stream-map (lambda (p) (sqrt (/ 6 p)))
              (monte-carlo cesaro-stream 0 0)))

(newline)
(display "Exercise 3.81")
(define (random-generator cmds)
  (define (random-help num commands)
    (let ((cmd (stream-car commands)))
      (cond ((eq? cmd 'generate)
             (cons-stream num
                          (random-help (rand-update num)
                                       (stream-cdr commands))))
            ((and (pair? cmd) (eq? (car cmd) 'reset))
             (cons-stream (cdr cmd)
                          (random-help (rand-update (cdr cmd)
                                       (stream-cdr commands))))))))
  (random-help random-init cmds))

(newline)
(display "Exercise 3.82")
(define (random-number-pairs x1 x2 y1 y2)
  (cons-stream (cons (random-in-range x1 x2)
                     (random-in-range y1 y2))
               (random-number-pairs x1 x2 y1 y2)))

(define (estimate-integral-stream P x1 x2 y1 y2)
  (let ((area (* (- x2 x1) (- y2 y1)))
        (randoms (random-number-pairs x1 x2 y1 y2)))
    (scale-stream (monte-carlo (stream-map P random-init) 0 0) area)))
