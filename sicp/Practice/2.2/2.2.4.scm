#lang r5rs

(newline)
(display "Exercise 2.44")

; make compiler happy
(define (beside left right) (newline))
(define (below down up) (newline))
(define (edge1-frame f) (newline))
(define (edge2-frame f) (newline))
(define (error message)
  (display message))

(define (up-split painter n)
  (if (= n 0)
    painter
    (let ((smaller (up-split painter (- n 1))))
      (below painter (beside smaller smaller)))))


(newline)
(display "Exercise 2.45")

(define (right-split painter n)
  (if (= n 0)
    painter
    (let ((smaller (right-split painter (- n 1))))
      (beside painter (below smaller smaller)))))

(define (split inter-layout inner-layout)
  (define (split-func painter n)
    (if (= n 0)
      painter
      (let ((smaller (split-func painter (- n 1))))
        (inter-layout painter (inner-layout smaller smaller)))))
  split-func)

(newline)
(display "Exercise 2.46")

(define (make-vect xcor ycor)
  (cons xcor ycor))

(define (xcor-vect v)
  (car v))

(define (ycor-vect v)
  (cdr v))

(define (add-vect v1 v2)
  (make-vect
    (+ (xcor-vect v1) (xcor-vect v2))
    (+ (ycor-vect v1) (ycor-vect v2))))

(define (sub-vect v1 v2)
  (make-vect
    (- (xcor-vect v1) (xcor-vect v2))
    (- (ycor-vect v1) (ycor-vect v2))))

(define (scale-vect v scalar)
  (make-vect
    (* (xcor-vect v) scalar)
    (* (ycor-vect v) scalar)))

(define (eq-vect? v1 v2)
  (and (= (xcor-vect v1) (xcor-vect v2))
       (= (ycor-vect v1) (ycor-vect v2))))

; frame-coord-map method
(define (frame-coord-map frame)
  (lambda (v)
    (add-vect
      (origin-frame frame)
      (add-vect (scale-vect (xcor-vect v)
                            (edge1-frame frame))
                (scale-vect (ycor-vect v)
                            (edge2-frame frame))))))
;; Testing:
(define (ensure b err-msg)
  (if (not b) (error err-msg)))

(define (ensure-all list-of-tests-and-messages)
  (cond ((null? list-of-tests-and-messages) #t)
        (else
          (ensure (car list-of-tests-and-messages)
                  (cadr list-of-tests-and-messages))
          (ensure-all (cddr list-of-tests-and-messages)))))

;; Tests:
(define v2-3 (make-vect 2 3))
(define v5-8 (make-vect 5 8))

;; Simple TDD to ensure everything works.  Yes, pretty keen of me.
(ensure-all
  (list (= (xcor-vect (make-vect 3 4)) 3) "x"
        (= (ycor-vect (make-vect 3 4)) 4) "y"
        (eq-vect? (make-vect 7 11) (add-vect v5-8 v2-3)) "add"
        (eq-vect? (make-vect 3 5) (sub-vect v5-8 v2-3)) "sub"
        (eq-vect? (make-vect 10 16) (scale-vect v5-8 2)) "scale"
        ))

(newline)
(display "Exercise 2.47")
(define (make-frame-list origin edge1 edge2)
  (list origin edge1 edge2))

(define (origin-frame frame)
  (life-ref frame 0))

(define (edge1-frame frame)
  (life-ref frame 1))

(define (edge2-frame frame)
  (life-ref frame 2))

(define (make-frame-cons origin edge1 edge2)
  (cons origin (const edge1 edge2)))

(define (origin-frame-cons frame)
  (car frame))

(define (edge1-frame-cons frame)
  (cadr frame))

(define (edge2-frame-cons frame)
  (cddr frame))


(newline)
(display "Exercise 2.48")

(define make-segment cons)

(define start-segment car)

(define end-segment cdr)

(newline)
(display "Exercise 2.49")

(define (segments->painter segment-list)
  (lambda (frame)
    (for-each
      (lambda (segment)
        (draw-line
          ((frame-coord-map frame) (start-segment segment))
          ((frame-coord-map frame) (end-segment segment))))
      segment-list)))

; selector from frame
(define (frame-bl frame)
  (origin-frame frame))

(define (frame-br frame)
  (add-vect (origin-frame frame) (edge1-frame frame)))

(define (frame-tl frame)
  (add-vect (origin-frame frame) (edge2-frame frame)))

(define (frame-tr frame)
  (add-vect (origin-frame frame)
            (add-vect (edge1-frame frame)
                      (edge2-frame frame))))

(define (middle-two-vectors v1 v2)
  (make-vect (/ (+ (xcor-vect v1) (xcor-vect v2)) 2)
             (/ (+ (ycor-vect v1) (ycor-vect v2)) 2)))

; a
(define (draw-outline frame)
  (let ((bl (frame-bl frame))
        (br (frame-br frame))
        (tl (frame-tl frame))
        (tr (frame-tr frame)))
    (segments->painter
      (make-segment bl br)
      (make-segment bl tl)
      (make-segment tl tr)
      (make-segment br tr))))

; b
(define (draw-X frame)
  (let ((bl (frame-bl frame))
        (br (frame-br frame))
        (tl (frame-tl frame))
        (tr (frame-tr frame)))
    (segments->painter
      (make-segment bl tr)
      (make-segment tl br))))
; c
(define (draw-diamond frame)
  (let ((bl (frame-bl frame))
        (br (frame-br frame))
        (tl (frame-tl frame))
        (tr (frame-tr frame)))
    (let ((a (middle-two-vectors bl br))
          (b (middle-two-vectors bl tl))
          (c (middle-two-vectors tl tr))
          (d (middle-two-vectors tr br)))
      (segments->painter
        (make-segment a b)
        (make-segment b c)
        (make-segment c d)
        (make-segment d a)))))

(newline)
(display "Exercise 2.50")

(define (transform-painter painter origin corner1 corner2)
  (lambda (frame)
    (let ((m (frame-coord-map frame)))
      (let ((new-origin (m origin)))
        (painter
          (make-frame new-origin
                      (sub-vect (m corner1) new-origin)
                      (sub-vect (m corner2) new-origin)))))))

(define (flip-vert painter)
  (transform-painter painter
                     (make-vect 0.0 1.0)
                     (make-vect 1.0 1.0)
                     (make-vect 0.0 0.0)))

(define (shrink-to-upper-right painter)
  (transform-painter painter
                     (make-vect 0.5 0.5)
                     (make-vect 1.0 0.5)
                     (make-vect 0.5 1.0)))

(define (rotate90 painter)
  (transform-painter painter
                     (make-vect 1.0 0.0)
                     (make-vect 1.0 1.0)
                     (make-vect 0.0 0.0)))

(define (beside painter1 painter2)
  (let ((split-point (make-vect 0.5 0.0)))
    (let ((paint-left
            (transform-painter painter1
                               (make-vect 0.0 0.0)
                               split-point
                               (make-vect 0.0 1.0)))
          (paint-right
            (transform-painter painter2
                               split-point
                               (make-vect 1.0 0.0)
                               (make-vect 0.5 1.0))))
      (lambda (frame)
        (paint-left frame)
        (paint-right frame)))))

(define (flip-horiz painter)
  (transform-painter painter
                     (make-vect 1.0 0.0)
                     (make-vect 0.0 0.0)
                     (make-vect 1.0 1.0)))

(define (rotate180 painter)
  (transform-painter painter
                     (make-vect 1.0 1.0)
                     (make-vect 0.0 1.0)
                     (make-vect 1.0 0.0)))

(define (rotate270 painter)
  (transform-painter painter
                     (make-vect 0.0 1.0)
                     (make-vect 0.0 0.0)
                     (make-vect 1.0 1.0)))

(newline)
(display "Exercise 2.51")

(define (below painter1 painter2)
  (let ((split-point (make-vect 0.0 0.5)))
    (let ((paint-down
            (transform-painter painter1
                               (make-vect 0.0 0.0)
                               (make-vect 0.0 1.0)
                               split-point))
          (paint-up
            (transform-painter painter2
                               split-point
                               (make-vect 0.5 1.0)
                               (make-vect 0.0 1.0))))
      (lambda (frame)
        (paint-down frame)
        (paint-up frame)))))


(define (below-2 painter1 painter2)
  (rotate90 (beside (rotate270 painter1) (rotate270 painter2))))

(newline)
(display "Exercise 2.52")

; a
; b
(define (corner-split painter n)
  (if (= n 0)
    painter
    (let ((up (up-split painter (- n 1)))
          (right (right-split painter (- n 1))))
      (let ((top-left (beside up up))
            (buttom-right (below right right))
            (corner (corner-split painter (- n 1))))
        (beside (below painter top-left)
                (below bottom-right corner))))))

(define (corner-split painter n)
  (if (= n 0)
    painter
    (beside (below painter (up-split painter n))
            (below (right-split painter n) (corner-split painter (- n 1))))))

; c
(define (square-limit painter n)
  (let ((four-parts (square-of-four flip-vert rotate180
                                  identity flip-horiz)))
    (four-parts (corner-split painter n))))
