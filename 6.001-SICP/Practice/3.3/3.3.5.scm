#lang r5rs

;; error function
(define (error reason . args)
  (newline)
  (display "Error: ")
  (display reason)
  (for-each (lambda (arg)
              (display " ")
              (write arg))
            args)
  (newline))

(display "3.3.5 Propagation of Constraints")
; constrant system
(define (inform-about-value constraint)
  (constraint 'I-have-a-value))

(define (inform-about-no-value constraint)
  (constraint 'I-lost-my-value))

(define (make-connector)
  (let ((value #f) (informant #f) (constraints '()))
    (define (set-my-value newval setter)
      (cond ((not (has-value? me))
             (set! value newval)
             (set! informant setter)
             (for-each-except setter
                              inform-about-value
                              constraints))
            ; NOTE: cannot set value if I already have value
            ((not (= value newval))
             (error "Contradiction" (list value newval)))
            (else 'ignored)))
    (define (forget-my-value retractor)
      (if (eq? retractor informant) ; NOTE: only command from same informant
          (begin (set! informant #f)
                 (for-each-except retractor
                                  inform-about-no-value
                                  constraints))
          'ignored))
    (define (connect new-constraint)
      (if (not (memq new-constraint constraints))
          (set! constraints
                (cons new-constraint constraints)))
      (if (has-value? me)
          (inform-about-value new-constraint))
      'done)
    (define (me request)
      (cond ((eq? request 'has-value?)
             (if informant #t #f))
            ((eq? request 'value) value)
            ((eq? request 'set-value!) set-my-value)
            ((eq? request 'forget) forget-my-value)
            ((eq? request 'connect) connect)
            (else (error "Unknown operation -- CONNECTOR"
                         request))))
    me))

(define (for-each-except exception procedure list)
  (define (loop items)
    (cond ((null? items) 'done)
          ((eq? (car items) exception) (loop (cdr items)))
          (else (procedure (car items))
                (loop (cdr items)))))
  (loop list))

(define (has-value? connector)
  (connector 'has-value?))

(define (get-value connector)
  (connector 'value))

(define (set-value! connector new-value informant)
  ((connector 'set-value!) new-value informant))

(define (forget-value! connector retractor)
  ((connector 'forget) retractor))

; NOTE NOTE NOTE
(define (connect connector new-constraint)
  ((connector 'connect) new-constraint))

; adder
(define (adder a1 a2 sum)
  (define (process-new-value)
    (cond ((and (has-value? a1) (has-value? a2))
           (set-value! sum
                       (+ (get-value a1) (get-value a2))
                       me))
          ((and (has-value? a1) (has-value? sum))
           (set-value! a2
                       (- (get-value sum) (get-value a1))
                       me))
          ((and (has-value? a2) (has-value? sum))
           (set-value! a1
                       (- (get-value sum) (get-value a2))
                       me))))

  (define (process-forget-value)
    (forget-value! sum me)
    (forget-value! a1 me)
    (forget-value! a2 me)
    (process-new-value))

  (define (me request)
    (cond ((equal? request 'I-have-a-value)
           (process-new-value))
          ((equal? request 'I-lost-my-value)
           (process-forget-value))
          (else
            (error "Unknown request -- ADDER" request))))

  (connect a1 me)
  (connect a2 me)
  (connect sum me)
  me)

; multiplier
(define (multiplier m1 m2 product)
  (define (process-new-value)
    (cond ((or (and (has-value? m1) (= (get-value m1) 0))
               (and (has-value? m2) (= (get-value m2) 0)))
           (set-value! product 0 me))
          ((and (has-value? m1) (has-value? m2))
           (set-value! product
                       (* (get-value m1) (get-value m2))
                       me))
          ((and (has-value? m1) (has-value? product))
           (set-value! m2
                       (/ (get-value product) (get-value m1))
                       me))
          ((and (has-value? m2) (has-value? product))
           (set-value! m1
                       (/ (get-value product) (get-value m2))
                       me))))

  (define (process-forget-value)
    (forget-value! product me)
    (forget-value! m1 me)
    (forget-value! m2 me)
    (process-new-value))

  (define (me request)
    (cond ((equal? request 'I-have-a-value)
           (process-new-value))
          ((equal? request 'I-lost-my-value)
           (process-forget-value))
          (else
            (error "Unknown request -- ADDER" request))))

  (connect m1 me)
  (connect m2 me)
  (connect product me)
  me)

(define (constant value connector)
  (define (me request)
    (error "Unknown request -- CONSTANT" request))
  (connect connector me)
  (set-value! connector value me)
  me)

(define (probe name connector)
  (define (print-probe value)
    (newline)
    (display "Probe: ")
    (display name)
    (display " = ")
    (display value))
  (define (process-new-value)
    (print-probe (get-value connector)))
  (define (process-forget-value)
    (print-probe "?"))
  (define (me request)
    (cond ((eq? request 'I-have-a-value)
           (process-new-value))
          ((eq? request 'I-lost-my-value)
           (process-forget-value))
          (else
            (error "Unknown request -- PROBE" request))))
  (connect connector me)
  me)

; Book's example
(define (celsius-fahrenheit-converter c f)
  (let ((u (make-connector))
        (v (make-connector))
        (w (make-connector))
        (x (make-connector))
        (y (make-connector)))
    (multiplier c w u)
    (multiplier v x u)
    (adder v y f)
    (constant 9 w)
    (constant 5 x)
    (constant 32 y)
    (probe "Intermediate value u" u)
    (probe "Constant value x" x)
    (newline)
    'ok))

(define C (make-connector))
(define F (make-connector))

(newline)
(display (celsius-fahrenheit-converter C F))

; probe is like a middleware
(probe "Celsius temp" C)
(probe "Fahrenheit temp" F)

(set-value! C 25 'user)
(set-value! F 212 'user)
(forget-value! C 'user)
(set-value! F 212 'user)

(newline)
(newline)
(display "Exercise 3.33")
(define (average-converter a b c)
  (let ((sum (make-connector))
        (two (make-connector)))
    (adder a b sum)
    (multiplier two c sum)
    (constant 2 two)
    'ok))

(define A (make-connector))
(define B (make-connector))
(define Average (make-connector))

(newline)
(display (average-converter A B Average))
(probe "A" A)
(probe "B" B)
(probe "Average" Average)

; calculate sum
(set-value! A 23 'CrazyAlvaro)
(set-value! B 12 'CrazyAlvaro)

; expect a Contradiction
(set-value! Average 12 'CrazyAlvaro)

; clear value
(forget-value! A 'CrazyAlvaro)

(set-value! A 24 'CrazyAlvaro)

(newline)
(newline)
(display "Exercise 3.34")
(define (squarer-flaw a b)
  (multiplier a a b)
  (newline)
  'ok)

(define xa (make-connector))
(define xb (make-connector))

(display (squarer-flaw xa xb))
(probe "xa" xa)
(probe "square" xb)
(set-value! xa 3 'CrazyAlvaro)
(forget-value! xa 'CrazyAlvaro)

(set-value! xb 2 'CrazyAlvaro)

; The flaw is that within multiplier, it both use xa, while if xa = ?, only product
; has value, it won't trigger the square

(newline)
(newline)
(display "Exercise 3.35")
(define (squarer a b)
  (define (process-new-value)
    (if (has-value? b)
        (if (< (get-value b) 0)
            (error "square less than 0 -- SQUARER" (get-value b))
            (set-value! a (sqrt (get-value b)) me))
        (if (has-value? a)
            (set-value! b (expt (get-value a) 2) me))))
  (define (process-forget-value)
    (forget-value! a me)
    (forget-value! b me)
    (process-new-value))
  (define (me request)
    (cond ((equal? request 'I-have-a-value)
           (process-new-value))
          ((equal? request 'I-lost-my-value)
           (process-forget-value))
          (else
            (error "Unknown request -- SQUARER" request))))
  (connect a me)
  (connect b me)
  me)

(define (squarer-converter a b)
  (squarer a b)
  (newline)
  'ok)

(define sq-a (make-connector))
(define sq-b (make-connector))
(display (squarer-converter sq-a sq-b))
(probe "sq-a" sq-a)
(probe "sq-b" sq-b)
(set-value! sq-a 3 'CrazyAlvaro)
(forget-value! sq-a 'CrazyAlvaro)
(set-value! sq-b 8 'CrazyAlvaro)

(newline)
(newline)
(display "Exercise 3.36")

(newline)
(newline)
(display "Exercise 3.37")
(define (c+ x y)
  (let ((z (make-connector)))
    (adder x y z)
    z))

(define (c- x y)
  (let ((z (make-connector)))
    (adder z y x)
    z))

(define (c* a b)
  (let ((product (make-connector)))
    (multiplier a b product)
    product))

(define (c/ a b)
  (let ((z (make-connector)))
    (multiplier b z a)
    z))
(define (cv val)
  (let ((z (make-connector)))
    (constant val z)
    z))

(define (new-celsius-fahrenheit-converter x)
  (c+ (c* (c/ (cv 9) (cv 5))
          x)
      (cv 32)))

(define new-C (make-connector))
(define new-F (new-celsius-fahrenheit-converter new-C))

(probe "new-C:" new-C)
(probe "new-F:" new-F)
(set-value! new-C 29 'CrazyAlvaro)
