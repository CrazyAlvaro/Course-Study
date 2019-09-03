(load "./readBook.scm")

; Sets as unordered lists
(define (element-of-set? x set)
  (cond ((null? set) #f)
        ((equal? x (car set)) #t)
        (else (element-of-set? x (cdr set)))))

(define (intersection-set set1 set2)
  (cond ((or (null? set1) (null? set2)) '())
        ((element-of-set? (car set1) set2)
         (cons (car set1)
               (intersection-set (cdr set1) set2)))
        (else (intersection-set (cdr set1) set2))))

; 2.59
(define (union-set set1 set2)
  (cond ((null? set1) set2)
        ((element-of-set? (car set1) set2)
         (union-set (cdr set1) set2))
        (else (cons (car set1)
                    (union-set (cdr set1) set2)))))

; 2.60
; duplicate representation
(define (dup-element-of-set? x set)
  (cond ((null? set) #f)
        ((equal? x (car set)) #t)
        (else (dup-element-of-set? x (cdr set)))))

(define (dup-adjoin-set x set) (cons x set))

(define (dup-intersection-set set1 set2)
  (cond ((or (null? set1) (null? set2)) '())
        ((dup-element-of-set? (car set1) set2)
         (cons (car set1)
               (dup-intersection-set (cdr set1) set2)))
        (else (dup-intersection-set (cdr set1) set2))))

(define (dup-union-set set1 set2)
  (append set1 set2))

; time complexity is decreased when dup-adjoin-set is called with constant time,
; while on non-dup version a linear check must be done.
; but thus increase other time complexity since may contain duplicates, will use
; this implementation if duplicates are unlike to happen.

; Sets as ordered lists
(define (ordered-element-of-set? x set)
  (cond ((null? set) #f)
        ((= x (car set)) #t)
        ((< x (car set)) #f)
        (else (ordered-element-of-set? x (cdr set)))))
; 2.61
(define (ordered-adjoin-set x set)
  ; find the first element > x
  (cond ((null? (car set)) (list x))
        ((= x (car set)) set)
        ((< x (car set)) (cons x set))
        (else (cons (car set) (ordered-adjoin-set x (cdr set))))))

(display (ordered-adjoin-set 3 '(1 2 4 5)))

; 2.62
(define (ordered-union-set set1 set2)
  (cond ((null? set1) set2)
        ((null? set2) set1)
        ((= (car set1) (car set2)) (cons (car set1) (ordered-union-set (cdr set1) (cdr set2))))
        ((< (car set1) (car set2)) (cons (car set1) (ordered-union-set (cdr set1) set2)))
        (else (cons (car set2) (ordered-union-set set1 (cdr set2))))))

(newline)
(display (ordered-union-set '(1 2 5 7 8) '(2 4 5 7 9)))

; implement set as binary tree

; 2.63
;a, They are the same, both produce the 2.16 list
;b, append is O(n), while cons is O(1), first is O(nlgn), second is O(n)

; 2.64
;a, first get the size of the left tree, use partial-tree to recursive construct the left tree,
; then use the result of the left tree to get the elements of the right tree, to construct the right tree,
; after that construct the current tree

; ((1 3) 5 (7 9 11)),

;b O(n), since every element being access once

(define list->tree newline)
(define tree->list-2 newline)
(define key car)
(define entry car)

; 2.65
; tranverse back to list to intersect and union then trans
(define (tree-union-set set1 set2)
  (list->tree (ordered-union-set (tree->list-2 set1)
                                 (tree->list-2 set2))))

; for ordered list
(define (ordered-intersection-set set1 set2)
  (cond ((null? set1) '())
        ((null? set2) '())
        ((< (car set1) (car set2)) (ordered-intersection-set (cdr set1) set2))
        ((> (car set1) (car set2)) (ordered-intersection-set (set1 (cdr set2))))
        (else (cons (car set1) (ordered-intersection-set (cdr set1)
                                                         (cdr set2))))))

(define (tree-intersection-set set1 set2)
  (list->tree (ordered-intersection-set (tree->list-2 set1)
                                        (tree->list-2 set2))))

; 2.66
(define (lookup given-key tree-set)
  (cond ((null? tree-set) #f)
        ((< given-key (key (entry tree-set))) (lookup given-key (left-branch tree-set)))
        ((> given-key (key (entry tree-set))) (lookup given-key (right-branch tree-set)))
        (else (entry tree-set))))
