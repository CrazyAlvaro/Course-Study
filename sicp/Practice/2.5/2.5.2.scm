#lang r5rs

(display "2.5.2")
(display "Exercise 2.81")
;a It will cause an infinite loop since there will always be  t1->t2

;b The apply-generic doesn't need to try to coerce with same type

;c
(define (apply-generic op . args)
  (define (no-method type-tags)
    (error "No method for these types"
           (list op type-tags)))

  (let ((type-tags (map type-tag args)))
    (let ((proc (get op type-tags)))
      (if proc
        (apply proc (map contents args))
        (if (= (length args) 2)
          (let ((type1 (car type-tags))
                (type2 (cadr type-tags))
                (a1 (car args))
                (a2 (cadr args)))
            (if (eq? type1 type2)
                (no-method type-tags)
                (let ((t1->t2 (get-coercion type1 type2))
                     (t2->t1 (get-coercion type2 type1)))
                  (cond (t1->t2
                          (apply-generic op (t1->t2 a1) a2))
                        (t2->t1
                          (apply-generic op a1 (t2->t1 a2)))
                        (else
                          (no-method type-tags))))))
          (no-method type-tags))))))

(display "Exercise 2.82")
; apply generic to handle multiple arguments
(define (apply-generic op . args)
  (define (no-method type-tags)
    (error "No method for these types"
           (list op type-tags)))

  ; coerce list of variables to the target type if possible
  (define (coerce-list-to-type list target)
    (if (null? list)
      '()
      (let (coerce-proc (get-coercion (type-tag (car list) target)))
        (if coerce-proc
          (cons (coerce-proc (car list)) (coerce-list-to-type (cdr list) target))
          ; otherwise we don't coerce this variable
          (cons (car list) (coerce-list-to-type (cdr list) target))))))

  ; try to transform list to each type of the list
  (define (apply-coerced-procedure list)
    (if (null? list)
      (no-method (map type-tag args))
      (let ((coerced-list (coerce-list-to-type args (type-tag (car list)))))
        (let ((proc (get op (map type-tag coerced-list))))
          (if proc
            (apply proc (map contents coerced-list))
            (apply-coerced-procedure (cdr list)))))))

  (let ((type-tags (map type-tag args)))
    (let ((proc (get op type-tags)))
      (if proc
        (apply proc (map contents args))
        ; else try to coerce to each type
        (apply-coerced-procedure args)))))


(display "Exercise 2.83")
(define (install-real-package)
  (define (make-real n d)
    (/ n d))

  (define (tag x) (attach-tag 'real x))
  (put 'make 'real
    (lambda (n d) (tag (make-real n d))))
  'done)

(define (make-real n d)
  ((get 'make 'real) n d))

; In each install package add:
(define (install-scheme-number-package)
  ; raise integer to rational number
  (define (raise-scheme-number int)
    (make-rational int 1))

  (define (tag x) (attach-tag 'scheme-number x))
  (put 'raise 'scheme-number raise-integer)
  'done)

(define (install-rational-package)
  ; raise rational to real
  (define (raise-rational rat)
    (make-real (numer rat) (denom rat)))
  (put 'raise 'rational raise-rational)
  'done)

(define (install-real-package)
  ; Raise real no complex number
  (define (raise-real real)
    (make-complex-from-real-imag real 0))
  (put 'raise 'real raise-real)
  'done)

(define (raise generic-num)
  (apply-generic 'raise generic-num))

(display "Exercise 2.84")
(define (number-level generic-num)
  (cond ((= (type-tag generic-num) 'integer) 0)
        ((= (type-tag generic-num) 'rational) 1)
        ((= (type-tag generic-num) 'real) 2)
        ((= (type-tag generic-num) 'complex) 3)
        (else
          (error "Unknown number type"
            (type-tag generic-num)
            generic-num))))

(define (apply-generic op . args)
  (define (no-method type-tags)
    (error "No method for these types"
      (list op type-tags)))

  (let ((type-tags (map type-tag args)))
    (let ((proc (get op type-tags)))
      (if proc
          (apply proc (map contents args))
          (if (= (length args) 2)
            (let ((level1 (number-level (car args)))
                  (level2 (number-level (cadr args)))
                  (a1 (car args))
                  (a2 (cadr args)))
              (cond ((> level1 level2)
                     (apply-generic op a1 (raise a2)))
                    ((< level1 level2)
                     (apply-generic op (raise a1) a2))
                    (else (no-method type-tags))))
            (else (no-method type-tags)))))))

(display "Exercise 2.85")
;(define (lower? generic-num))
;(define (lower generic-num))

(define (install-rational-package)
  (put 'project 'rational
    (lambda (x) (make-scheme-number (round(/ (numer x) (denom x))))))
  'done)

; NOTE: how to drop a real number to a rational number
;(define (install-real-package)
;  (put 'project 'real
;    (make-rational ))
;  'done)

(define (install-complex-package)
  (put 'project 'complex
    (lambda (x) (make-real (real-part x))))
  'done)

(define (project generic-num)
  (apply-generic 'project generic-num))

(define (drop generic-num)
  (cond ((= (type-tag generic-num) 'integer) generic-num)
        (else
          (if (equ? (raise (project generic-num)) generic-num)
            (drop (project generic-num))
            generic-num))))

(define (apply-generic op . args)
  (define (no-method type-tags)
    (error "No method for these types"
      (list op type-tags)))

  (let ((type-tags (map type-tag args)))
    (let ((proc (get op type-tags)))
      (if proc
          (drop (apply proc (map contents args)))
          (if (= (length args) 2)
            (let ((level1 (number-level (car args)))
                  (level2 (number-level (cadr args)))
                  (a1 (car args))
                  (a2 (cadr args)))
              (cond ((> level1 level2)
                     (drop (apply-generic op a1 (raise a2))))
                    ((< level1 level2)
                     (drop (apply-generic op (raise a1) a2)))
                    (else (no-method type-tags))))
            (else (no-method type-tags)))))))

(display "Exercise 2.86")
; inside implementation of complex number, and complex-package's
; arithmetic opeartion must be replaced by generic arithmetic opeartion

; NOTE: all the generic procedures need
(define (sine x) (apply-generic 'sine x))
(define (cosine x) (apply-generic 'cosine x))
(define (atan x) (apply-generic 'atan x))
(define (square) (apply-generic 'square x))
