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

(newline)
(display "3.5.3 Exploiting the Stream Paradigm")
(define (sqrt-improve x)
  (average guess (/ x guess)))

(define (sqrt-stream x)
  (define guesses
    (cons-stream 1.0
                 (stream-map (lambda (guess)
                               (sqrt-improve guess x))
                             guesses)))
  guesses)

(newline)
(display "sequence accelerator")
(define (euler-transform s)
  (let ((s0 (stream-ref s 0))
        (s1 (stream-ref s 1))
        (s2 (stream-ref s 2)))
    (cons-stream (- s2 (/ (square (- s2 s1))
                          (+ s0 (* -2 s1) s2)))
                 (euler-transform (stream-cdr s)))))

(newline)
(display "Exercise 3.63")
; since the original version makes use of memorization,
; but the straight way doesn't

(newline)
(display "Exercise 3.64")
(define (stream-limit s tolerance)
  (define (stream-limit-help curr stream)
    (let ((remain-s (stream-cdr stream))
          (next (stream-car remain-s)))
      (if (< (abs (- curr next))
             tolerance)
          second
          (stream-limit-help second remain-s))))
  (stream-limit-help (stream-car s)
                     (stream-cdr s)))

; another way use stream-ref
(define (stream-limit-ref s tolerance)
  (if (< (abs (- (stream-ref s 0) (stream-ref 1))) tolerance)
      (stream-ref s 1)
      (stream-limit-ref (stream-cdr s) tolerance)))

(newline)
(display "Exercise 3.65")
(define (ln2-summands n)
  (cons-stream (/ 1.0 n)
               (stream-map - (ln2-summands (+ n 1)))))

(define ln2-stream
  (partial-sums (ln2-summands 1)))

(newline)
(display "Exercise 3.66")
; How many pairs before (1,100)?
; (99 + 98) * 2 + 1 + 1 = 196

; before (99,100)
; ((1 * 2 + 1) * 2 + 1) ....

; before (100, 100)
; 100: 1
; 99: 2
; 98: L100+L99+1 = 3
; 97: L100+L99+L98+1
; ...
; it's partial-sums + 1

(newline)
(display "Exercise 3.67")
(define (pairs s t)
  (cons-stream
    (list (stream-car s) (stream-car t)
    (interleave
      (interleave (stream-map (lambda (x) (list (stream-car s) x))
                              (stream-cdr t))
                  (stream-map (lambda (x) (list (stream-car t) x))
                              (stream-cdr s)))
      (pairs (stream-cdr s) (strem-cdr t))))))

(newline)
(display "Exercise 3.68")
;It's the same as i <= j

(newline)
(display "Exercise 3.69")
(define (triples s t u)
  (cons-stream
    (list (stream-car s) (stream-car t) (stream-car u))
    (interleave
      (stream-map (lambda (x) (cons (stream-car s) x))
                  (pairs (s t)))
      (triples
        (stream-cdr s)
        (stream-cdr t)
        (stream-cdr u)))))

(define triples-stream (triples integers integers integers))

(define (pythagorean-triples triples-stream)
  (stream-filter
    (lambda (triples)
      (= (square (caddr triples))
         (+ (square (car triples)) (square (cadr triples)))))
    triples-stream))

(newline)
(display "Exercise 3.70")
(define (merge-weighted s1 s2 weight)
  (cond ((stream-null? s1) s2)
        ((stream-null? s2) s1)
        (else
          (let ((s1car (stream-car s1))
                (s2car (stream-car s2))
                (s1car-weight (weight s1car))
                (s2car-weight (weight s2car)))
            (cond ((< s1car-weight s2car-weight)
                   (cons-stream s1car (merge-weighted (stream-cdr s1) s2 weight)))
                  ((> s1car-weight s2car-weight)
                   (cons-stream s2car (merge-weighted s1 (stream-cdr s2) weight)))
                  (else
                    (cons-stream s1car
                                 (merge-weighted (stream-cdr s1)
                                                 (stream-cdr s2)))))))))

(define (weighted-paris s t weight)
  (cons-stream
    (list (stream-car s) (stream-car t))
    (merge-weighted
      (stream-map (lambda (x) (list (stream-car s) x))
                  (stream-cdr t))
      (weighted-paris (stream-cdr s) (stream-cdr t) weight)
      weight)))

; a
(weighted-paris integers integers +)

; b
(define filtered-integers
  (stream-filter (lambda (x)
                   (not
                     (or (even? x)
                         (zero? (remainder x 3))
                         (zero? (remainder x 5)))))
                 integers))

(weighted-paris filtered-integers
                filtered-integers
                (lambda (x)
                  (let ((i (car x)) (j (cadr x)))
                    (+ (* 2 i)
                       (* 3 j)
                       (* 5 i j)))))

(newline)
(display "Exercise 3.71")
(define (cube x) (* x x x))
(define (cube-sum p)
  (let ((i (car p))
        (j (cadr p)))
    (+ (cube i) (cube j))))

(define sorted-pairs
  (weighted-paris integers
                  integers
                  (lambda (x) (cube-sum x))))

(define (ramanujan s pre)
  (let ((curr (stream-car (cube-sum sorted-pairs))))
    (cond ((= pre curr)
           (cons-stream curr
                        (ramanujan (stream-cdr s) curr)))
          (else (ramanujan (stream-cdr s) num)))))

(newline)
(display "Exercise 3.72")
; similar problem skip

(newline)
(display "Streams as signals")
(define (integral integrand initial-value dt)
  (define int
    (cons-stream initial-value
                 (add-streams (scale-stream integrand dt)
                              int)))
  int)

(newline)
(display "Exercise 3.73")
(define (RC R C dt)
  (lambda (i-stream v0)
    (add-streams (scale-stream i-stream R)
                 (integral (scale-stream i-stream (/ 1 C)) v0 dt))))

(newline)
(display "Exercise 3.74")
(define zero-crossings
  (stream-map sign-change-detector sense-data (cons-stream 0 zero-crossings)))

(newline)
(display "Exercise 3.75")
(define (make-zero-crossings input-stream last-value last-avpt)
  (let ((avpt (/ (+ (stream-car input-stream) last-value) 2)))
    (cons-stream (sign-change-detector avpt last-avpt)
                 (make-zero-crossings (stream-cdr input-stream)
                                      (stream-car input-stream)
                                      avpt))))

(newline)
(display "Exercise 3.76")
(define (smooth input-stream)
  (define (smooth-help stream last-value)
    (let ((avpt (/ (+ (stream-car stream) last-value) 2)))
      (cons-stream avpt (smooth-help (stream-cdr stream) (stream-car stream)))))
  (smooth-help (stream-cdr input-stream) (stream-car input-stream)))

; another more elegant way
(define (smooth-1 input-stream)
  (stream-map (lambda (a b) (/ (+ a b) 2)) input-stream (stream-cdr input-stream)))

(define (zero-crossings-modular input-stream)
  (stream-map sign-change-detector input-stream (stream-cdr input-stream)))

(define smoothed-zero-crossings-modular
  (zero-crossings-modular (smooth-1 sense-data)))
