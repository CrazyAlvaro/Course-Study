#lang r5rs
(display "3.3.1 Mutable List Structure")

(newline)
(display "Exercise 3.12")
; (b)
; (b c d)
(define (last-pair x)
  (if (null? (cdr x))
      x
      (last-pair (cdr x))))


(newline)
(display "Exercise 3.13")
; the procedure never stops, infinite loop
(define (make-cycle x)
  (set-cdr! (last-pair x) x)
  x)

(newline)
(display "Exercise 3.14")
; Reverse x

; v (a)
; w (d c b a)
(define (mystery x)
  (define (loop x y)
    (if (null? x)
        y
        (let ((temp (cdr x)))
          (set-cdr! x y)
          (loop temp x))))
  (loop x '()))

(define v (list 'a 'b 'c 'd))
(define w (mystery v))
(newline)
(display v)
(newline)
(display w)

(newline)
(display "Exercise 3.15")

(newline)
(display "Exercise 3.16")
; z1 z2
(define x (list 'a 'b))

(define z1 (cons x x))
(define z2 (cons (list 'a 'b) (list 'a 'b)))

(define (count-pairs x)
  (if (not (pair? x))
      0
      (+ (count-pairs (car x))
         (count-pairs (cdr x))
         1)))

(newline)
(display (count-pairs z1))
(newline)
(display (count-pairs z2))
; while z1 is 3

(define z3 '(a b c))
(newline)
(display (count-pairs z3))

(define a '(b))
(define b (cons a a))
(define z4 (list b))
(newline)
(display (count-pairs z4))

(define z7 (cons b b))
(newline)
(display (count-pairs z7))

(newline)
(display "Exercise 3.17")
(define (my-count-pairs pairs)
  (let ((traversed-pairs '()))
    (define (traversed? pair)
      (if (memq pair traversed-pairs)
          0
          (begin
            (set! traversed-pairs (cons pair traversed-pairs))
            1)))

    (define (count ps)
      (if (not (pair? ps))
          0
          (+ (count (car ps))
             (count (cdr ps))
             (traversed? ps))))
    (count pairs)))


(newline)
(display (my-count-pairs z1))
(newline)
(display (my-count-pairs z2))
(newline)
(display (my-count-pairs z3))
(newline)
(display (my-count-pairs z4))
(newline)
(display (my-count-pairs z7))

(newline)
(display "Exercise 3.18")
(define (contains-loop? pairs)
  (let ((visited-pairs '()))
    (define (visited? pair)
      (if (memq pair visited-pairs)
          #t
          (begin
            (set! visited-pairs (cons pair visited-pairs))
            #f)))
    (define (loop? pr)
      (if (not (pair? pr))
          #f
          (if (visited? pr)
              #t
              (loop? (cdr pr)))))
    (loop? pairs)))

(newline)
(display (contains-loop? z7))
(newline)
(define cycle-z7 (make-cycle z7))
(display (contains-loop? cycle-z7))

(newline)
(display "Exercise 3.19")
; use two pointers
(define (contains-loop-constant? pair-list)
  (define (loop-detection slow fast)
    (cond ((or (not (pair? fast)) (not (pair? slow))) #f)
          ((eq? fast slow) #t)
          (else
            (if (not (pair? (cdr fast)))
                #f
                (loop-detection (cdr slow) (cdr (cdr fast)))))))
  (loop-detection pair-list (cdr pair-list)))

(newline)
(display (contains-loop-constant? z7))
(newline)
(display (contains-loop-constant? cycle-z7))

(newline)
(display "Exercise 3.20")
