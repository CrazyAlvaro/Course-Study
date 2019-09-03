#lang r5rs

(define (filter predicate sequence)
  (cond ((null? sequence) nil)
        ((predicate (car sequence))
         (cons (car sequence)
               (filter predicate (cdr sequence))))
        (else (filter predicate (cdr sequence)))))

(define (unique-pairs n)
  (flatmap
    (lambda (i)
      (map (lambda (j) (list i j))
           (enumerate-interval 1 (- i 1))))
    (enumerate-interval 1 n)))

(define nil '())

(define (square n)
  (* n n))

(define (accumulate op initial sequence)
  (if (null? sequence)
    initial
    (op (car sequence)
        (accumulate op initial (cdr sequence)))))

;; 2.33
(define (my-map p sequence)
  (accumulate (lambda (x y) (cons (p x) y)) nil sequence))
(define (my-append seq1 seq2)
  (accumulate cons seq2 seq1))
(define (my-length sequence)
  (accumulate (lambda (x y)
                (if (not (null? x))
                  (+ 1 y)
                  (+ 0 y)))
              0 sequence))

;; Testing
(newline)
(display (my-map square (list 1 2 3 4)))
(newline)
(display (my-append (list 3 5 6) (list 8 3 4)))
(newline)
(display (my-length (list 2 9 4)))

;; 2.34
;; (... (a(n)*x + a(n-1)*x + xxx + a(1))*x + a(0))
(define (horner-eval x coefficient-sequence)
  (accumulate (lambda (this-coeff higher-terms)
                (+ this-coeff (* x higher-terms)))
              0
              coefficient-sequence))

;; Testing
;; 1 + 3x + 5x**3 + x**5 at x = 2
(newline)
(display "expecting: 79")
(newline)
(display (horner-eval 2 (list 1 3 0 5 0 1)))

;; 3.35
(define (old-count-leave x)
  (cond ((null? x) 0)
        ((not (pair? x)) 1)
        (else (+ (old-count-leave (car x))
                 (old-count-leave (cdr x))))))

;; transform tree to list
(define (enumerate-tree tree)
  (cond ((null? tree) nil)
        ((not (pair? tree)) (list tree))
        (else (append (enumerate-tree (car tree))
                      (enumerate-tree (cdr tree))))))

(define (count-leave t)
  (accumulate (lambda (node rest)
                (if (null? node)
                  (+ 0 rest)
                  (+ 1 rest)))
              0
              (enumerate-tree t)))
(newline)
(display (count-leave (list 1 (list 4 (list 9 16) 25) (list 36 49))))

;; 3.36
(define (accumulate-n op init seqs)
  (if (null? (car seqs))
    nil
    (cons (accumulate op init (map car seqs))
          (accumulate-n op init (map cdr seqs)))))


(define seq-num `((1 2 3) (4 5 6) (7 8 9) (10 11 12)))
(newline)
(display "expecting: (22 26 30)")
(newline)
(display (accumulate-n + 0 seq-num))

;; 3.37
(define (dot-product v w)
  (accumulate + 0 (map * v w)))

(define (matrix-*-vector m v)
  (map (lambda (row)
         (dot-product v row))
       m))

(define (transpose mat)
  (accumulate-n cons '() mat))

(define (matrix-*-*matrix m n)
  (let ((cols (transpose n)))
    (map (lambda (row)
           (matrix-*-vector cols row))
         m)))

;; 2.38
(define (fold-left op initial sequence)
  (define (iter result rest)
    (if (null? rest)
      result
      (iter (op result (car rest))
            (cdr rest))))
  (iter initial sequence))

(newline)
(newline)
(display "Exercise 2.38")
(newline)
(display (accumulate / 1 (list 1 2 3)))
(newline)
(display (fold-left / 1 (list 1 2 3)))
(newline)
(display (accumulate list nil (list 1 2 3)))
(newline)
(display (fold-left list nil (list 1 2 3)))

;; Property
;; (op (car v) (cdr v)) == (op (cdr v) (car v))

;; 2.39
(define (reverse-right sequence)
  (accumulate (lambda (front reversed-list)
                (append reversed-list (list front)))
              nil
              sequence))

(define (reverse-left sequence)
  (fold-left (lambda (reversed-list front)
               (cons front reversed-list))
             nil
             sequence))

(newline)
(newline)
(display "Exercise 2.39")
(newline)
(display (reverse-right (list 1 2 3 4 5)))
(newline)
(display (reverse-left (list 1 2 3 4 5)))


(newline)
(display "Exercise 2.40")
(define (flatmap proc seq)
  (accumulate append nil (map proc seq)))

(define (enumerate-interval low high)
  (if (> low high)
    nil
    (cons low (enumerate-interval (+ low 1) high))))

(newline)
(display (unique-pairs 5))

(define (prime? x)
  (define (test divisor)
    (cond ((> (* divisor divisor) x) #t)
          ((= 0 (remainder x divisor)) #f)
          (else (test (+ divisor 1)))))
  (test 2))

(define (prime-sum? pair)
  (prime?  (+ (car pair) (cadr pair))))

(define (make-pair-sum pair)
  (list (car pair) (cadr pair) (+ (car pair) (cadr pair))))

(define (prime-sum-pairs n)
  (map make-pair-sum
       (filter prime-sum? (unique-pairs n))))

(newline)
(display (prime-sum-pairs 6))

(newline)
(display "Exercise 2.41")

(define (unique-triples n)
  (flatmap (lambda (i)
             (flatmap
               (lambda (j)
                 (map (lambda (k) (list i j k))
                      (enumerate-interval 1 (- j 1))))
               (enumerate-interval 1 (- i 1))))
           (enumerate-interval 1 n)))

(newline)
(display "Test unique-triples 5")
(newline)
(display (unique-triples 5))

(define (three-sum n sum)
  (filter (lambda (triples) (= sum (accumulate + 0 triples)))
          (unique-triples n)))

(newline)
(display "three-sum 5 12")
(newline)
(display (three-sum 5 12))

(newline)
(display (enumerate-interval 1 5))


(newline)
(display "Test accumulate")
(newline)
(display (accumulate + 0 (list 1 2 3  5)))

(newline)
(display "unique-pairs with append")
(newline)
(display (unique-pairs 5))

; This is without using append then the result will become messed
(define (nested-map n)
  (map (lambda (i)
         (map (lambda (j) (list i j))
              (enumerate-interval 1 (- i 1))))
       (enumerate-interval 1 n)))

(newline)
(display "nested-map")
(newline)
(display (nested-map 5))

(newline)
(display "Exercise 2.42")

(define empty-board (list))
; (newline)
; (display "empty-board")
; (newline)
; (display empty-board)

(define (adjoin-position new-row k rest-of-queens)
  (if (null? rest-of-queens)
    (list new-row)
    (append rest-of-queens (list new-row))))

; (newline)
; (display "adjoin-position")
; (newline)
; (display (adjoin-position 3 8 empty-board))
; (newline)
; (display (adjoin-position 2 8 (list 4 5)))
; (newline)

(define (safe? k positions)
  (define (iter-safe? pos check-pos positions)
    (cond ((or (< pos 0) (null? positions)) #t)
          ; False either same line or diagonal
          ((or (= (list-ref positions pos)
                  (list-ref positions check-pos))
               (= (abs (- (list-ref positions pos) (list-ref positions check-pos)))
                  (abs (- pos check-pos))))
           #f)
          (else (iter-safe? (- pos 1) check-pos positions))))
  (iter-safe? (- k 2) (- k 1) positions))

(define (queens board-size)
  (define (queens-cols k)
    (if (= k 0)
      (list empty-board)
      (filter
        (lambda (positions) (safe? k positions))
        (flatmap
          ; This rest-of-queens is just one positions
          (lambda (rest-of-queens)
            (map (lambda (new-row)
                   (adjoin-position new-row k rest-of-queens))
                 (enumerate-interval 1 board-size)))
          (queens-cols (- k 1))))))
  (queens-cols board-size))

; (newline)
; (display "queens 1: ")
; (display (queens 1))
; (newline)
; (display "queens 2: ")
; (display (queens 2))
; (newline)
; (display "queens 3: ")
; (display (queens 3))
(newline)
(display "queens 4: ")
(display (queens 4))
; (newline)
; (display "queens 5: ")
; (display (queens 5))
; (newline)
; (display "queens 8: ")
; (display (queens 8))

(newline)
(display "Exercise 2.43")

; Each invoke of flatmap will call queens-cols board-size times more in Loise's solution
; So total will be 8^8 times T
