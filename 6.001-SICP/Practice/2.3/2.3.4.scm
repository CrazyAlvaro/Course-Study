(load "./readBook.scm")
(load "./2.3.3.scm")

(newline)
(display "Exercise 2.67")
; sample tree
(define sample-tree
  (make-code-tree (make-leaf 'A 4)
                  (make-code-tree
                    (make-leaf 'B 2)
                    (make-code-tree (make-leaf 'D 1)
                                    (make-leaf 'C 1)))))

(define sample-message '(0 1 1 0 0 1 0 1 0 1 1 1 0))
(newline)
(display sample-tree)
(decode sample-message sample-tree)

(display "Exercise 2.68")
(newline)
(define (encode message tree)
  (if (null? message)
  '()
  (append (encode-symbol (car message) tree)
          (encode (cdr message) tree))))

(define (encode-symbol symbol tree)
  (cond ((leaf? tree) '())
        ((element-of-set? symbol (symbols tree))
          (let ((left-b (left-branch tree)) (right-b (right-branch tree)))
            (cond ((element-of-set? symbol (symbols left-b))
                   (cons '0 (encode-symbol symbol left-b)))
                  ((element-of-set? symbol (symbols right-b))
                   (cons '1 (encode-symbol symbol right-b))))))
        (else (error "symbol not in the tree" symbol))))

(encode '(a d a b b c a) sample-tree)

(display "Exercise 2.69")
; make-leaf-set return an ordered set

(define (generate-huffman-tree pairs)
  (successive-merge (make-leaf-set pairs)))

; my solution
(define (successive-merge ordered-nodes)
  (if (< (length ordered-nodes) 2)
      (car ordered-nodes)
      (let ((first-node (car ordered-nodes))
            (second-node (cadr ordered-nodes)))
        (successive-merge
          (adjoin-set (make-code-tree first-node second-node)
                      (cddr ordered-nodes))))))

(newline)
(generate-huffman-tree '((A 4) (B 2) (C 1) (D 1)))
(encode '(a d a b b c a)
  (generate-huffman-tree '((A 4) (B 2) (C 1) (D 1))))

(newline)
(define test-tree (generate-huffman-tree '((A 3) (B 5) (C 6) (D 6))))
(display test-tree)
(newline)
(encode '(A B C D) test-tree)

(newline)
(display "Exercise 2.70")
;(decode sample-message
(define song
  '(get a job sha na na na na na na na na get a job sha na na na na na na na na wah yip yip yip yip yip yip yip yip yip sha boom))

(define song-tree
  (generate-huffman-tree '((A 2) (BOOM 1) (GET 2) (JOB 2) (NA 16) (SHA 3) (YIP 9) (WAH 1))))

(newline)
(display song-tree)
(newline)
(display (length (encode song song-tree)))
(newline)
(display (* 3 (length song)))

(display "Exercise 2.71")
; n=5: 4, 1,
; n=10: 9, 1

(display "Exercise 2.72")
;the special case for 2.71,
; to encode the most frequent symnbol is: O(N)
; to encode the least frequent symbol is: O(N**2)
