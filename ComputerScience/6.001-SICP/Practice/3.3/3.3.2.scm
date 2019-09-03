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

(display "3.3.2 Representing Queues")
; Book's representation use two pointers
(define (front-ptr queue) (car queue))

(define (rear-ptr queue) (cdr queue))

(define (set-front-ptr! queue item) (set-car! queue item))

(define (set-rear-ptr! queue item) (set-cdr! queue item))

(define (make-queue) (cons '() '()))

(define (empty-queue? q) (null? (front-ptr q)))

(define (front-queue q)
  (if (empty-queue? q)
      (error "Front called with an empty queue" q)
      (car (front-ptr q))))

(define (insert-queue! q item)
  (let ((new-pair (cons item '())))
    (cond ((empty-queue? q)
           (set-front-ptr! q new-pair)
           (set-rear-ptr! q new-pair)
           q)
          (else
            (set-cdr! (rear-ptr q) new-pair)
            (set-rear-ptr! q new-pair)
            q))))

(define (delete-queue! q)
  (cond ((empty-queue? q)
         (error "DELETE! called with an empty queue" q))
        (else
          (set-front-ptr! q (cdr (front-ptr q)))
          q)))

(newline)
(display "Exercise 3.21")
(define q1 (make-queue))
(newline)
(display (insert-queue! q1 'a))
(newline)
(display (insert-queue! q1 'b))
(newline)
(display (delete-queue! q1))
(newline)
(display (delete-queue! q1))

; standard print print front-ptr and rear-ptr, and when delete-queue
; only reset front-ptr, rear-ptr still points to the item, that's why b
; is still there
(define (print-queue queue)
  (display (front-ptr queue)))

(newline)
(print-queue (insert-queue! q1 'a))
(newline)
(print-queue (insert-queue! q1 'b))
(newline)
(print-queue (delete-queue! q1))
(newline)
(print-queue (delete-queue! q1))

(newline)
(display "Exercise 3.22")
(define (make-in-queue)
  (let ((front-ptr '())
        (rear-ptr '()))
    (define (insert item)
      (let ((new-pair (cons item '())))
        (if (empty?)
            ((set! front-ptr new-pair)
             (set! rear-ptr new-pair))
            ((set-cdr! rear-ptr new-pair)
             (set! rear-ptr new-pair)))))

    (define (delete)
      (if (empty?)
          (error "DELETE called with an empty queue")
          ((let ((tmp-pair front-ptr))
            (set! front-ptr (cdr front-ptr))
            tmp-pair))))

    (define (empty?) (null? front-ptr))

    (define (dispatch m)
      (cond ((eq? m 'insert) insert)
            ((eq? m 'delete) delete)
            ((eq? m 'empty?) empty?)
            ((eq? m 'front) front-ptr)
            (else
              (error "DISPATCH unknow procedure name" m))))
    dispatch))

(define q2 (make-in-queue))

(newline)
(display "Exercise 3.23")
; use the same structure and book's implementation of queue, which use two pointers
; but for each item (value (left-ptr right-ptr)) use a double linked list
(define (make-deque) (cons '() '()))
(define (empty-deque? dq) (null? (front-ptr dq)))
(define (front-deque dq)
  (if (empty-deque? dq)
      (error "Front called with an empty deque" dq)
      (front-ptr dq)))
(define (rear-deque dq)
  (if (empty-deque? dq)
      (error "Rear called with an empty deque" dq)
      (rear-ptr dq)))

; selector of pointers
(define (deque-prev-pair item) (car (cdr item)))
(define (deque-next-pair item) (cdr (cdr item)))

; set pointers for each item
(define (set-deque-item-next-ptr! pair item)
  (set-cdr! (cdr pair) item))
(define (set-deque-item-prev-ptr! pair item)
  (set-car! (cdr pair) item))

(define (front-insert-deque! dq item)
  (let ((new-pair (cons item (cons '() '()))))
    (cond ((empty-deque? dq)
           (set-front-ptr! dq new-pair)
           (set-rear-ptr! dq new-pair)
           dq)
          (else
            (set-deque-item-next-ptr! new-pair (front-ptr dq))
            (set-deque-item-prev-ptr! (front-ptr dq) new-pair)
            (set-front-ptr! dq new-pair)
            dq))))

(define (front-delete-deque! dq)
  (cond ((empty-deque? dq)
         (error "front-delete-deque! called with an empty deque" dq))
        (else
          (set-front-ptr! dq (deque-next-pair (front-ptr dq)))
          (if (not (empty-deque? dq))
              (set-deque-item-prev-ptr! (front-ptr dq) '()) ; clear front's prev ptr
              (set-rear-ptr! dq '()))
          dq)))

(define (rear-insert-deque! dq item)
  (let ((new-pair (cons item (cons '() '()))))
    (cond ((empty-deque? dq)
           (set-front-ptr! dq new-pair)
           (set-rear-ptr! dq new-pair)
           dq)
          (else
            (set-deque-item-next-ptr! (rear-ptr dq) new-pair)
            (set-deque-item-prev-ptr! new-pair (rear-ptr dq))
            (set-rear-ptr! dq new-pair)
            dq))))

(define (rear-delete-deque! dq)
  (cond ((empty-deque? dq)
         (error "rear-delete-deque! called with an empty deque" dq))
        (else
          (set-rear-ptr! dq (deque-prev-pair (rear-ptr dq)))
          (if (not (empty-deque? dq))
              (set-deque-item-next-ptr! (rear-ptr dq) '()) ; clear rear's next ptr
              (set-front-ptr! dq '()))
          dq)))

(define (print-deque dq)
  (define (print-deque-help dq-item)
    (if (pair? dq-item)
        (begin
          (display (car dq-item))
          (print-deque-help (deque-next-pair dq-item)))))
  (if (not (empty-deque? dq))
      (print-deque-help (front-deque dq))
      (display "")))

(define dq1 (make-deque))
(print-deque dq1)
(newline)
(display dq1)
(newline)
(print-deque (front-insert-deque! dq1 'a))
(newline)
(print-deque (front-insert-deque! dq1 'b))
(newline)
(print-deque (front-insert-deque! dq1 'c))
(newline)
(print-deque (rear-insert-deque! dq1 '1))
(newline)
(print-deque (rear-insert-deque! dq1 '2))
(newline)
(print-deque (rear-delete-deque! dq1))
(newline)
(print-deque (rear-delete-deque! dq1))
(newline)
(print-deque (front-delete-deque! dq1))
(newline)
(print-deque (front-delete-deque! dq1))
(newline)
(print-deque (front-delete-deque! dq1))
