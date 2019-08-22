#lang r5rs

(define nil '())

(define (error reason . args)
  (display "Error: ")
  (display reason)
  (for-each (lambda (arg)
              (display " ")
              (write arg))
            args)
  (newline))
;;(scheme-report-environment -1))  ;; we hope that this will signal an error

(define (square n) (* n n))

;; 2.24
(newline)
(display (list 1 (list 2 (list 3 4))))
;;(1 (2 (3 4)))

;; 2.25
(define l-1 (list 1 3 (list 5 7) 9))
(newline)
(display (car (cdr (car (cdr (cdr l-1))))))

(define l-2 (list (list 7)))
(newline)
(display (car (car l-2)))

(define l-3 (list 1 (list 2 (list 3 (list 4 (list 5 (list 6 7)))))))
; (newline)
; (display l-3)
(newline)
(display (car (cdr (car (cdr (car (cdr (car (cdr (car (cdr (car (cdr l-3)))))))))))))

;; 2.26
(define (append-list list1 list2)
  (if (null? list1)
    list2
    (cons (car list1)
          (append-list (cdr list1) list2))))

(define x (list 1 2 3))
(define y (list 4 5 6))
(newline)
(display (append x y))
(newline)
(display (cons x y))
(newline)
(display (list x y))

; (1 2 3 4 5 6)
; ((1 2 3) 4 5 6)
; ((1 2 3) (4 5 6))

;; 2.27
(define xl (list (list 1 2) (list 3 4)))
(newline)
(display xl)
(newline)
(display (reverse xl))

(define (deep-reverse items)
  (cond ((null? items) nil)
        ((not (pair? items)) items)
        (else (append (deep-reverse (cdr items))
                      (list (deep-reverse (car items)))))))

(newline)
(display (deep-reverse xl))

;; 2.28
(define xlist (list (list 1 2) (list 3 4)))

; (define (fringe items)
;   (define (fringe-recursive items ans)
;     (cond ((null? items) nil)
;           ((not (pair? items)) (append ans (list items)))
;           (else (append (fringe (car items))
;                         (fringe (cdr items))))))
;   (fringe-recursive items nil))

(define (fringe items)
  (cond ((null? items) nil)
        ((not (pair? items)) (list items))
        (else (append (fringe (car items))
                      (fringe (cdr items))))))

(newline)
(display (fringe nil))
(newline)
(display (fringe xlist))
(newline)
(display (fringe (list xlist xlist)))

;; 2.29

;; a
;; Constructor: mobile
(define (make-mobile left right)
  (list left right))

(define (left-branch mobile)
  (if (or (null? mobile) (not (pair? mobile)))
    (error "expect a mobile structure")
    (list-ref mobile 0)))

(define (right-branch mobile)
  (if (or (null? mobile) (not (pair? mobile)))
    (error "expect a mobile structure")
    (list-ref mobile 1)))

;; Constructor: branch
(define (make-branch length structure)
  (list length structure))

(define (branch-length branch)
  (if (or (null? branch) (not (pair? branch)))
    (error "Expect a branch")
    (list-ref branch 0)))

(define (branch-structure branch)
  (if (or (null? branch) (not (pair? branch)))
    (error "Expect a branch")
    (list-ref branch 1)))

;; construct a mobile, with
;; left( l 3,  mobile(left: l 4, w 6, right l 3,w 8) ),
;; right (l 2,w 21 )A
;;
;; total-weight: 35
;; balanced

;; b total-weight

(define l-b-l (make-branch 4 6))
;;(define l-b-r (make-branch 3 8))    ;; balanced
(define l-b-r (make-branch 2 8))    ;; not balanced for sub mob, for testing
(define l-m (make-mobile l-b-l l-b-r))
(define l-b (make-branch 3 l-m))
(define r-b (make-branch 2 21))
(define mob (make-mobile l-b r-b))


(define (mobile? struct) (pair? struct))

(define (mobile-weight mobile)
  (if (null? mobile)
    0
    (+ (structure-weight (branch-structure (left-branch mobile)))
       (structure-weight (branch-structure (right-branch mobile))))))

(define (structure-weight struct)
  (cond ((null? struct) 0)
        ((mobile? struct) (mobile-weight struct))
        (else struct)))
(define (total-weight mob)
  (mobile-weight mob))

(total-weight mob)
;; > (total-weight mob)
;; 35

;; c
(define (branch-torque br)
  (cond ((or (null? br) (not (pair? br))) 0)
        (else (* (branch-length br) (structure-weight (branch-structure br))))))

(define (balanced? mob)
  (if (not (mobile? mob))
    #t    ;; if it's not a mob, it's balanced
    (and (= (branch-torque (left-branch mob))
            (branch-torque (right-branch mob)))
         ;; And submobs are also balanced
         (and (balanced? (branch-structure (left-branch mob)))
              (balanced? (branch-structure (right-branch mob)))))))

;; Testing
;;(balanced? mob)

;; d
;; (define (make-mobile left right)
;;   (cons left right))
;;
;; (define (make-branch length structure)
;;   (cons length structure))

;; In this case, we just need to redefine left-branch, right-branch, branch-length and branch-structure, that's all
;; Since the upper layer used API to access mobile and branch, it doesn't need to know the implementation


;; 2.30

;; without using any higher-order procedures
(define (square-tree tree)
  (cond ((null? tree) '())
        ((pair? tree)
         (cons (square-tree (car tree)) (square-tree (cdr tree))))
        (else (square tree))))

;; using map and recursion
(define (square-tree-1 tree)
  (map (lambda (sub-tree)
         ;; map procedure will check null
         (if (pair? sub-tree)
           (square-tree-1 sub-tree)
           (square sub-tree)))
       tree))

(square-tree
  (list 1
        (list 2 (list 3 4) 5)
        (list 6 7)))
;; (1 (4 (9 16) 25) (36 49))

;; > (display (square-tree
;;                (list 1
;;                              (list 2 (list 3 4) 5)
;;                                      (list 6 7))))
;; (1 (4 (9 16) 25) (36 49))

;; > (display (square-tree-1
;;                (list 1
;;                              (list 2 (list 3 4) 5)
;;                                      (list 6 7))))
;; (1 (4 (9 16) 25) (36 49))

;; 2.31
(define (tree-map proc tree)
  (cond ((null? tree) '())
        ((pair? tree) (cons (tree-map proc (car tree))
                            (tree-map proc (cdr tree))))
        (else (proc tree))))

(define (square-tree-2 tree)
  (tree-map square tree))
;; > (display (square-tree-2
;;                (list 1
;;                              (list 2 (list 3 4) 5)
;;                                      (list 6 7))))
;; (1 (4 (9 16) 25) (36 49))

;; 2.32

;; Generate all subsets of a set(a list)
(define (subsets s)
  (if (null? s)
    (list '())
    (let ((rest (subsets (cdr s))))
      ;; apply all subsets of (cdr s), add (car s)
      ;; (subsets s) = (subsets (cdr s)) + (each subset (cdr s) + (car s))
      (append rest (map (lambda (set)
                          (append (list (car s)) set))
                        rest)))))
;      (append rest (map (lambda(set)
;                          (cons set (cons (append set (car s)) '())))
;                        rest)))))

(define my-set (list 1 2 3))
(newline)
(display my-set)
(newline)
(display (subsets my-set))

; (1 2 3)
; (() (3) (2) (2 3) (1) (1 3) (1 2) (1 2 3))

;;;; 2.2.3 Sequence as Conventional Interfaces

(define (accumulate op initial sequence)
  (if (null? sequence)
    initial
    (op (car sequence)
        (accumulate op initial (cdr sequence)))))

