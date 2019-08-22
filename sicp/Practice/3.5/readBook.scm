#lang racket

(define (stream-car stream) (car stream))
(define (stream-cdr stream) (force (cdr stream)))
(define stream-null? null?)
(define the-empty-stream '())
(define-syntax cons-stream
  (syntax-rules ()
    ((cons-stream head tail)
     (cons head (delay tail)))))

; the sum of all the prime numbers in an interval.
(define (sum-primes a b)
  (define (iter count accum)
    (cond ((> count b) accum)
          ((prime? count) (iter (+ count 1) (+ count accum)))
          (else (iter (+ count 1) accum))))
  (iter a 0))

(define (prime? x)
  (define (test divisor)
    (cond ((> (* divisor divisor) x) #t)
          ((= 0 (remainder x divisor)) #f)
          (else (test (+ divisor 1)))))
  (test 2))

; (define (sum-primes a b)
;   (accumulate +
;               0
;               (filter prime? (enumerate-interval a b))))

; (stream-car (cons-stream x y)) = x
; (stream-cdr (cons-stream x y)) = y

(define (stream-ref s n)
  (if (= n 0)
      (stream-car s)
      (stream-ref (stream-cdr s) (- n 1))))

; (define (stream-map proc s)
;   (if (stream-null? s)
;       the-empty-stream
;       (cons-stream (proc (stream-car s))
;                    (stream-map proc (stream-cdr s)))))

(define (stream-map proc . argstreams)
  (if (stream-null? (car argstreams))
      the-empty-stream
      (cons-stream
        (apply proc (map stream-car argstreams))
        (apply stream-map
               (cons proc (map stream-cdr argstreams))))))

(define (stream-for-each proc s)
  (if (stream-null? s)
      'done
      (begin (proc (stream-car s))
             (stream-for-each proc (stream-cdr s)))))

; stream-for-each is useful for viewing streams
(define (display-stream s)
  (stream-for-each display-line s))

(define (display-line x)
  (newline)
  (display x))

; (cons-stream a b) === (cons a (delay b))

(define (stream-filter pred stream)
  (cond ((stream-null? stream) the-empty-stream)
        ((pred (stream-car stream))
         (cons-stream (stream-car stream)
                      (stream-filter pred
                                     (stream-cdr stream))))
        (else (stream-filter pred (stream-cdr stream)))))

(define (stream-enumerate-interval low high)
  (if (> low high)
      the-empty-stream
      (cons-stream
        low
        (stream-enumerate-interval (+ low 1) high))))

(stream-car
  (stream-cdr
    (stream-filter prime?
      (stream-enumerate-interval 10000 1000000))))


; delay
; (delay (exp)) is syntactic sugar for (lambda () (exp))
; (define (force delayed-object)
;   (delayed-object))

(define (memo-proc proc)
  (let ((already-run? #f) (result #f))
    (lambda ()
      (if (not already-run?)
          (begin (set! result (proc))
                 (set! already-run? #t)
                 result)
          result))))


; 3.5.2
;
; define integer
(define (integers-starting-from n)
  (cons-stream n (integers-starting-from (+ n 1))))

(define integers (integers-starting-from 1))

(define (divisible? x y) (= (remainder x y) 0))

(define no-sevens
  (stream-filter (lambda (x) (not (divisible? x 7)))
                 integers))

(define (fibgen a b)
  (cons-stream a (fibgen b (+ a b))))

(define fibs (fibgen 0 1))

; the sieve of Eratosthenes method of construct prime numbers
(define (sieve stream)
  (cons-stream
   (stream-car stream)
   (sieve (stream-filter
            (lambda (x)
             (not (divisible? x (stream-car stream))))
            (stream-cdr stream)))))

(define primes (sieve (integers-starting-from 2)))

(stream-ref primes 50)

; Defining streams implicitly
(define ones (cons-stream 1 ones))

(define (add-streams s1 s2)
  (stream-map + s1 s2))

; Construct stream use the stream has already been constreucted
(define ano-integers (cons-stream 1 (add-streams ones ano-integers)))

(define ano-fibs
  (cons-stream 0
               (cons-stream 1
                            (add-streams (stream-cdr fibs)
                                         fibs))))
(define (scale-stream stream factor)
  (stream-map (lambda (x) (* x factor)) stream))

(define double (cons-stream 1 (scale-stream double 2)))

(stream-ref double 10)

(define ano-primes
  (cons-stream
    2
    (stream-filter prime? (integers-starting-from 3))))

; 3.5.3 Exploiting the Stream Paradigm
(define (sqrt-improve guess x)
  (average guess (/ x guess)))

(define (average a b)
  (/ (+ a b) 2))

(define (sqrt-stream x)
  (define guesses
    (cons-stream 1.0
                 (stream-map (lambda (guess)
                               (sqrt-improve guess x))
                             guesses)))
  guesses)

; (display-stream (sqrt-stream 2))

(define (pi-summands n)
  (cons-stream (/ 1.0 n)
               (stream-map - (pi-summands (+ n 2)))))

(define (partial-sums stream)
  (cons-stream (stream-car stream)
               (add-streams (stream-cdr stream)
                            (partial-sums stream))))

; (display-stream (partial-sums integers))

(define pi-stream
  (scale-stream (partial-sums (pi-summands 1)) 4))

; (display-stream pi-stream)
(define (square v)
  (* v v))

(define (euler-transform s)
  (let ((s0 (stream-ref s 0))       ; Sn-1
        (s1 (stream-ref s 1))       ; Sn
        (s2 (stream-ref s 2)))      ; Sn+1
    (cons-stream (- s2 (/ (square (- s2 s1))
                          (+ s0 (* -2 s1) s2)))
                 (euler-transform (stream-cdr s)))))

; (display-stream (euler-transform pi-stream))
; (display-stream (euler-transform (euler-transform pi-stream)))

; create a stream of streams
(define (make-tableau transform s)
  (cons-stream s
               (make-tableau transform
                             (transform s))))

; get the first element of stream of streams
(define (accelerated-sequence transform s)
  (stream-map stream-car
              (make-tableau transform s)))
(display-stream (accelerated-sequence euler-transform
                                      pi-stream))

; infinite streams of pairs

; solve prime-sum-paris problem
; (stream-filter (lambda (pair)
;                  (prime? (+ (car pair) (cadr pair))))
;                int-pairs)

; so that we need int-pairs that i <= j
; divide the matrix into above the diagonal, first element S-0 T-0,
; the first row and the rest, which is the recursive part S0 T-1..N
; from S-1, T-1

; the first row is:
;(stream-map (lambda (x) (list (stream-car s) x))
            ;(stream-cdr t))

(define (interleave s1 s2)
  (if (stream-null? s1)
      s2
      (cons-stream (stream-car s1)
                   (interleave s2 (stream-cdr s1)))))
(define (pairs s t)
  (cons-stream
    (list (stream-car s) (stream-car t))
    (interleave
      (stream-map (lambda (x) (list (stream-car s) x))
                  (stream-cdr t))
      (pairs (stream-cdr s) (stream-cdr t)))))

; Streams as signals
(define (integral integrand initial-value dt)
  (define int
    (cons-stream initial-value
                 (add-streams (scale-stream integrand dt)
                 int)))
  int)
