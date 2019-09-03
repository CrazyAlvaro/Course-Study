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

(display "3.3.4 A Simulator for Digital Circuits")
; half-adder
(define (half-adder a b s c)
  (let ((d (make-wire)) (e (make-wire)))
    (or-gate a b d)
    (and-gate a b c)
    (inverter c e)
    (and-gate d e s)
    'ok))

; full-adder
(define (full-adder a b c-in sum c-out)
  (let ((s (make-wire))
        (c1 (make-wire))
        (c2 (make-wire)))
    (half-adder b c-in s c1)
    (half-adder a s sum c2)
    (or-gate c1 c2 c-out)
    'ok))

; Primitive function boxes
(get-signal <wire>)
(set-signal! <wire> <new value>)
(add-action! <wire> <procedure of no arguments>)

(define (inverter input output)
  (define (invert-input)
    (let ((new-value (logical-not (get-signal input))))
      (after-delay inverter-delay
                   (lambda ()
                     (set-signal! output new-value)))))
  (add-action! input invert-input)
  'ok)

(define (and-gate a1 a2 output)
  (define (and-action-procedure)
    (let ((new-value
           (logical-and (get-signal a1)
                        (get-signal a2))))
      (after-delay and-delay
                   (lambda ()
                     (set-signal! output new-value)))))
  (add-action! a1 and-action-procedure)
  (add-action! a2 and-action-procedure)
  'ok)

(display "Exercise 3.28")
(define (or-gate a1 a2 output)
  (define (or-action-procedure)
    (let ((new-value
            (logical-or (get-signal a1)
                        (get-signal a2))))
      (after-delay or-delay
                   (lambda ()
                     (set-signal! output new-value)))))
  (add-action! a1 or-action-procedure)
  (add-action! a2 or-action-procedure)
  'ok)

(define (logical-or s1 s2)
  (cond ((and (= s1 0) (= s2 0)) 0)
        (else 1)))

(display "Exercise 3.29")
(define (or-gate-compound a1 a2 output)
  (let ((s1 (make-wire))
        (s2 (make-wire))
        (c1 (make-wire)))
    (inverter a1 s1)
    (inverter a2 s2)
    (and-gate s1 s2 c1)
    (inverter c1 output)
    'ok))

; the first two inverter only count once
; or-gate-delay = inverter-delay + and-delay + inverter-delay
;               = inverter-delay * 2 + and-delay

(define "Exercise 3.30")
(define (ripple-carry-addder A B S C)
  ; three list of wires, Ak, Bk, Sk and C
  (let ((c-in (make-wire)))
    (cond ((and (= (length A) 1) (= (length B) 1))
           (begin
             (set-signal! c-in 0)
             (full-adder (car A) (car B) c-in (car S) C)))
          ((and (> (length A) 1) (> (length B) 1))
           (begin
             ; get c-in on previous ripple-carry-addder
             (ripple-carry-addder (cdr A) (cdr B) (cdr S) c-in)
             (full-adder (car A) (car B) c-in (car S) C)))
          (else
           (error "ripple-carry-addder No input signal")))))

; ripple-carry-addder-delay = n * full-adder-delay
; full-adder-delay = half-adder-s-delay + half-adder-c-delay + or-delay
; half-adder-s-delay = max(or-delay, (and-delay + inverter-delay)) + and-delay
; half-adder-c-delay = and-delay
; assume and-delay + inverter-delay > or-delay
; full-adder-delay = and-delay + inverter-delay + and-delay + or-delay
;                  = 2 * and-delay + or-delay + inverter-delay

; conclusion: ripple-carry-addder-delay = n * (2 * and-delay + or-delay + inverter-delay)

(display "Exercise 3.31")
; if didn't invoke the proc immediately, then the output won't have any value
; for half-adder, d, c, e s will not have any value,

(display "Exercise 3.32")
; For and-gate: both a1 a2 have and-action-procedure which contains after-delay
;
; the point here is that new-value is calculated before delay
; if the segments' list has LIFO, and the first wire a1 change first, then the result will be incorrect
; (a1, a2)
; (0, 1) initial
; (1, 1) a1 0 -> 1, then a1's and-action-procedure called, a1's new-value = 1, lambda procedure inserted
; (1, 0) a2 1 -> 0, then a2's and-action-procedure called, a2's new-value = 0, lambda procedure inserted
; propogate, after-delay
; a2's (lambda() (set-signal! output new-value)) called, set output = 0
; a1's (lambda() (set-signal! output new-value)) called, set output = 1
;
; so after this propogation we got output = 1, which is not correct
