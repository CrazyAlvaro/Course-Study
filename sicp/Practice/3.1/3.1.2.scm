#lang r5rs
(#%require (only racket/base random))

(define (estimate-pi trials)
  (sqrt (/ 6 (monte-carlo trials cesaro-test))))

(define (cesaro-test)
  (= (gcd (random) (random)) 1))

(define random-init 10)

(define (rand-update x)
  (let ((n 4232)
        (m 322))
    (remainder (* m x) n)))

(define (estimate-pi-1 trials)
  (sqrt (/ 6 (random-gcd-test trials random-init))))

; NOTE: used rand-update instead of rand
(define (random-gcd-test trials initial-x)
  (define (iter trials-remaining trials-passed x)
    (let ((x1 (rand-update x)))
      (let ((x2 (rand-update x1)))
        (cond ((= trials-remaining 0)
               (/ trials-passed trials))
              ((= (gcd x1 x2) 1)
               (iter (- trials-remaining 1)
                     (+ trials-passed 1)
                     x2))
              (else
                (iter (- trials-remaining 1)
                      trials-passed
                      x2))))))
  (iter trials 0 initial-x))

(display "Exercise 3.5")
(newline)
(define (random-in-range low high)
  (let ((range (- high low)))
    (+ low (* (random) range))))

(define (monte-carlo trials experiment)
  (define (iter trials-remaining trials-passed)
    (cond ((= trials-remaining 0)
           (/ trials-passed trials))
          ((experiment)
           (iter (- trials-remaining 1) (+ trials-passed 1)))
          (else
            (iter (- trials-remaining 1) trials-passed))))
  (iter trials 0))

(define (within-circle x y)
  (<= (+ (expt (- x 5) 2)
         (expt (- y 7) 2))
      (expt 3 2)))

(define (estimate-integral P x1 x2 y1 y2 trials)
  (define (experiment)
    (within-circle (random-in-range x1 x2)
                   (random-in-range y1 y2)))
  (monte-carlo trials experiment))

(newline)
(display "Estimate-pi: ")
(display (* (estimate-integral within-circle 2 8 4 10 1000000) 4.0))

(display "Exercise 3.6")
(define (rand)
  (let ((ran-num random-init))
    (define (rand-reset num)
      (set! ran-num num))
    (define (rand-new)
      (begin (set! ran-num (rand-update ran-num))
             ran-num))

    (define (dispatch m)
      (cond ((eq? m 'generate) rand-new)
            ((eq? m 'reset) rand-reset)
            (else (error "Unknown request -- RAND"
                         m))))
    dispatch)
