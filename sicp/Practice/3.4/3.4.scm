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

(display "3.4 Concurrency: Time Is of the Essence")
(newline)
(display "3.4.1 The Nature of Time in Concurrent Systems")
(newline)
(display "Exercise 3.38")
; a
; Peter: x, Paul y, Mary z
; zxy = zyx = 40
; xzy = 35
; yzx = 50
; xyz = yxz = 45

; b
; (xyz) 50
; (xzy) 80
; (yzx) 110
; (xy)z 40
; (yx)z 55
; z(xy) 30
; z(yx) 60
; (xz)y 30
; (zx)y 90
; y(xz) 40
; y(zx) 90
; (yz)x 60
; (zy)x 90
; x(yz) 55
; x(zy) 90

(newline)
(display "3.4.2 Mechanisms for Controlling Concurrency")

(newline)
(display "Exercise 3.39")
; I think all remains, since we haven't make x atomic

(newline)
(display "Exercise 3.40")
; 10**2 10**3 10**4 10**5 10**6

; 10**6

(newline)
(display "Exercise 3.41")
; er, I think it's not necessary, since read is not changing the value

(newline)
(display "Exercise 3.42")
; it's safe, we have a mutex for both procedure

(newline)
(display "Exercise 3.43")

(newline)
(display "Exercise 3.44")
; we need to serialize this as well, since transfer could occur at the same account

(newline)
(display "Exercise 3.45")
; The exchange procedure and the deposit or withdraw procedure are all protected,
; while exchange use both withdraw and deposit, the program will be locked

(newline)
(display "Exercise 3.46")

(newline)
(display "Exercise 3.47")
; a, in terms of mutexes
; b, in terms of atomic test-and-set! operations

; Don't see quite different of the two
; here my initial implementation
(define (make-semaphore-initial size)
  (define (test-and-set! semaphor-list)
    (if (null? semaphor-list)
        #t
        (if (car semaphor-list)
            (test-and-set! (cdr semaphor-list))
            (begin (set-car! semaphor-list #t)
                   #f))))

  (define (clear! semaphor-list)
    (if (null? semaphor-list)
        'clear
        (if (car semaphor-list)
            (set-car! semaphor-list #f)
            (clear! (cdr semaphor-list)))))

  (define (construct-list size)
    (cond ((< size 0)
           (error "semaphor-list must > 0" size))
          ((= size 0) '())
          (else
            (cons #f (construct-list (- size 1))))))

  (let ((semaphor-list (construct-list size)))
    (define (the-semaphore m)
      (cond ((eq? m 'acquire)
             (if (test-and-set! semaphor-list)
                 (the-semaphore 'acquire)))
            ((eq? m 'release) (clear! semaphor-list))))
    the-semaphore))

; checkout community solution
(define (make-semaphore max-size)
  (let ((lock (make-mutex))
        (size 0))
    (define (the-semaphore m)
      (cond ((eq? m 'acquire)
             (lock 'acquire)
             (if (> size max-size)
                 (begin (lock 'release) (the-semaphore m))
                 (begin (set! size (+ 1 size)) (lock 'release))))
            ((eq? m 'release)
             (lock 'acquire)
             (set! size (- size 1))
             (lock 'release))
            (else
              (error "Unknown command --THE-SEMAPHORE" m))))
    the-semaphore))

(newline)
(display "Exercise 3.48")
(define (serialized-exchange acc1 acc2)
  (let ((ser1 (acc1 'serialize))
        (ser2 (acc2 'serialize))
        (ser-exchange (if (< (acc1 'id) (acc2 'id))
                       (ser1 (ser2 exchange))
                       (ser2 (ser1 exchange)))))
    (ser-exchange acc1 acc2)))

(newline)
(display "Exercise 3.49")
; if no order information know before two get each resource, but
; not willing to give up
