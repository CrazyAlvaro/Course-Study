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
(display "3.3.3 Representing Tables")
(newline)
(display "Exercise 3.24")
(define (make-table same-key?)
  (let ((local-table (list '*table*)))
    (define (assoc key records)
      (cond ((null? records) #f)
            ; used the passed in procedure here
            ((same-key? key (caar records)) (car records))
            (else (assoc key (cdr records)))))
    (define (lookup key)
      (let ((record (assoc key (cdr local-table))))
        (if record
            (cdr record)
            #f)))
    (define (insert! key value)
      (let ((record (assoc key (cdr local-table))))
        (if record
            (set-cdr! record value)
            (set-cdr! local-table
                      (cons (cons key value)
                            (cdr local-table))))))

    (define (dispatch m)
      (cond ((eq? m 'lookup) lookup)
            ((eq? m 'insert) insert!)
            (else (error "Unkown operation: TABLE" m))))
    dispatch))

(newline)
(display "Exercise 3.25")
; actual we can just use list as key
(define (nkeys-make-table)
  (list '*table*))

(define (nkeys-assoc key records)
 (cond ((null? records) #f)
       ((not (pair? records)) #f) ; expect records to be a pair
       ((equal? key (caar records)) (car records))
       (else (nkeys-assoc key (cdr records)))))

(define (nkeys-lookup keys table)
  (if (null? keys)
      (cdr table) ; found value
      (let ((records (nkeys-assoc (car keys) (cdr table))))
        (if records
            (nkeys-lookup (cdr keys) records)
            #f))))

(define (nkeys-insert! keys value table)
  (define (create-subtable keys value)
    (let ((keys-len (length keys)))
      (cond ((= 0 keys-len) value)
            ((= 1 keys-len)
             (cons (car keys)
                   (create-subtable (cdr keys) value)))
            (else
              (list (car keys)
                    (create-subtable (cdr keys) value))))))

  (if (null? keys)
      (set-cdr! table value)
      (let ((subtable (nkeys-assoc (car keys) (cdr table))))
        (if (pair? subtable)
            (nkeys-insert! (cdr keys) value subtable)
            (set-cdr! table
                      (cons (list (car keys)
                                  (create-subtable (cdr keys) value))
                            (cdr table)))))))

(define (nkeys-print table)
  (define (print-space n)
    (if (= n 0)
        #f
        (begin (display " ")
               (print-space (- n 1)))))

  (define (print-help table level)
    (cond ((pair? table)
           (if (pair? (car table))
               (begin (print-help (car table) level)
                      (print-help (cdr table) level))
               (begin (newline)
                      (print-space level)
                      (display (car table))
                      (display ": ")
                      (print-help (cdr table) (+ level 1)))))
          ((not (null? table))
           (begin (newline)
                  (print-space level)
                  (display table)))
          (else (display ""))))

  (print-help table 0))


; Test
(define t3 (nkeys-make-table))
;(nkeys-print t3)
(nkeys-insert! '(key-a) 'value-a t3)
;(nkeys-print t3)
(nkeys-insert! '(a c) 'ac t3)
;(nkeys-print t3)
(nkeys-insert! '(a c) 'value-ac t3)
;(newline)
;(display (nkeys-lookup '(a c) t3))
(nkeys-insert! '(a b c) 'value-abc t3)
(newline)
(display (nkeys-lookup '(a b c) t3))
(nkeys-insert! '(a b c d e f g) 'value-abcdefg t3)
;(nkeys-insert! '(a b c d) 'value-abcd t3)
;(nkeys-print t3)
(newline)
;(display t3)
(display (nkeys-lookup '(a b c d e f g) t3))
;(newline)
;(display t3)
;(nkeys-print t3)
;(nkeys-insert! '(a d c) 'adc t3)

; lookip
(newline)
(display (nkeys-lookup '(a c) t3))
(newline)
(display (nkeys-lookup '(a g) t3))

(display "Exercise 3.26")
; we could construct a node with key, either value or (left-branch, right-branch),
; value less than ccurent value goes to left, otherwise goes to right.

(display "Exercise 2.27")
; looks like a cache mechanism

; it's because the table has all previous number stored
; No it won't work, since we need fib to call memo-fib to have the table the same as the one created before
