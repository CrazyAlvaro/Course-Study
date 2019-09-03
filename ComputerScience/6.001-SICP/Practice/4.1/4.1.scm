(display "4.1 The Metacircular Evaluator")
;        <-
; Eval        Apply
;        ->

(newline)
(display "4.1.1 The Core of the Evaluator")


(newline)
(display "Eval")
(define (eval exp env)
        ; Primitive expressions
  (cond ((self-evaluating? exp) exp)
        ((variable? exp) (lookup-variable-value exp env))
        ; Special forms
        ((quoted? exp) (text-of-quotation exp))
        ((assignment? exp) (eval-assignment exp env))
        ((definition? exp) (eval-definition exp env))
        ((if? exp) (eval-if exp env))
        ((lambda? exp)
         (make-procedure (lambda-parameters exp)
                         (lambda-body exp)
                         env))
        ((begin? exp)
         (eval-sequence (begin-actions exp) env))
        ((cond? exp) (eval (cond->if exp) env))
        ; Combinations
        ((application? exp)
         (begin
           (display exp)
           (apply (eval (operator exp) env)
                  (list-of-values (operands exp) env))))
        (else
          (error "Unkown expression type -- EVAL" exp))))

(newline)
(display "Apply")
(define (apply procedure arguments)
  (cond ((primitive-procedure? procedure)
         (begin
           (newline)
           (display "Apply")
           (newline)
           (display procedure)
           (newline)
           (display arguments)
           (newline)
           (apply-primitive-procedure procedure arguments)))
        ((compound-procedure? procedure)
         (eval-sequence
           (procedure-body procedure)
           (extend-environment
             (procedure-parameters procedure)
             arguments
             (procedure-environment procedure))))
        (else
          (error
            "Unknown procedure type -- APPLY" procedure))))

(newline)
(display "Procedure arguments")
(define (list-of-values exps env)
  (if (no-operands? exps)
      '()
      (begin
        (newline)
        (display "list-of-values")
        (display (first-operand exps))
        (cons (eval (first-operand exps) env)
              (list-of-values (rest-operands exps) env)))))

(newline)
(display "Conditionals")
(define (eval-if exp env)
  (if (true? (eval (if-predicate exp) env))
      (eval (if-consequent exp) env)
      (eval (if-alternative exp) env)))

(newline)
(display "Sequences")
(define (eval-sequence exps env)
  (cond ((last-exp? exps) (eval (first-exp exps) env))
        (else (eval (first-exp exps) env)
              (eval-sequence (rest-exps exps) env))))

(newline)
(display "Assignments and definitions")
(define (eval-assignment exp env)
  (set-variable-value! (assignment-variable exp)
                       (eval (assignment-value exp) env)
                       env)
  'ok)

(define (eval-definition exp env)
  (define-variable! (definition-variable exp)
                    (eval (definition-value exp) env)
                    env)
  'ok)

(newline)
(display "Exercise 4.1")
(define (list-of-values-left-to-right exps env)
  (if (no-operands? exps)
      '()
      (let ((first-value (eval (first-operand exps) env)))
        (cons first-value (list-of-values-left-to-right (rest-operands exps) env)))))

(define (list-of-values-right-to-left exps env)
  (list-of-values-left-to-right (reverse exps) env))

(newline)
(display "4.1.2 Representing Expressions")

(define (self-evaluating? exp)
  (cond ((number? exp) #t)
        ((string? exp) #t)
        (else #f)))

(define (variable? exp) (symbol? exp))

; (quote <text-of-quotation>)
(define (quoted? exp)
  (begin
    (newline)
    (display "quoted? ")
    (display (tagged-list? exp 'quote))
    (tagged-list? exp 'quote)))
(define (text-of-quotation exp)
  (begin
    (newline)
    (display "text-of-quotation ")
    (display (cadr exp))
    (cadr exp)))

(define (tagged-list? exp tag)
  (if (pair? exp)
      (eq? (car exp) tag)
      #f))

; (set! <var> <value>)
(define (assignment? exp) (tagged-list? exp 'set!))
(define (assignment-variable exp) (cadr exp))
(define (assignment-value exp) (caddr exp))

; Definition
; First: (define <var> <value>)
; Second: (define (<var> <parameter> ... <parameter>)
;           <body>)
; is syntactic sugar
; (define <var>
;   (lambda (<parameter> ... <parameter>)
;     <body>))

(define (definition? exp) (tagged-list? exp 'define))
(define (definition-variable exp)
  (if (symbol? (cadr exp))  ; First form
      (cadr exp)
      (caadr exp)))

(define (definition-value exp)
  (if (symbol? (cadr exp))
      (caddr exp)
      (make-lambda (cdadr exp)      ; formal parameters
                   (cddr exp))))    ; body

; Lambda expressions
(define (lambda? exp) (tagged-list? exp 'lambda))
(define (lambda-parameters exp) (cadr exp))
(define (lambda-body exp) (cddr exp))

(define (make-lambda parameters body)
  (cons 'lambda (cons parameters body)))

; Conditionals begin with if
(define (if? exp) (tagged-list? exp 'if))
(define (if-predicate exp) (cadr exp))
(define (if-consequent exp) (caddr exp))
(define (if-alternative exp)
  (if (not (null? (cdddr exp)))
      (cadddr exp)
      'false))

(define (make-if predicate consequent alternative)
  (list 'if predicate consequent alternative))

; begin
(define (begin? exp) (tagged-list? exp 'begin))
(define (begin-actions exp) (cdr exp))
(define (last-exp? seq) (null? (cdr seq)))
(define (first-exp seq) (car seq))
(define (rest-exps seq) (cdr seq))

(define (sequence->exp seq)
  (cond ((null? seq) seq)
        ((last-exp? seq) (first-exp seq))
        (else (make-begin seq))))
(define (make-begin seq) (cons 'begin seq))

; application
(define (application? exp) (pair? exp))
(define (operator exp) (car exp))
(define (operands exp) (cdr exp))
(define (no-operands? ops) (null? ops))
(define (first-operand ops) (car ops))
(define (rest-operands ops) (cdr ops))

(newline)
(display "Derived expressions")

; cond -> if
(define (cond? exp) (tagged-list? exp 'cond))
(define (cond-clauses exp) (cdr exp))
(define (cond-else-clause? clause)
  (eq? (cond-predicate clause) 'else))
(define (cond-predicate clause) (car clause))
(define (cond-actions clause) (cdr clause))
(define (cond->if exp) (expand-clauses (cond-clauses exp)))
(define (expand-clauses clauses)
  (if (null? clauses)
      'false  ; no else clause
      (let ((first (car clauses))
            (rest (cdr clauses)))
        (if (cond-else-clause? first)
          (if (null? rest)
              (sequence->exp (cond-actions first))
              (error "ELSE clause isn't last: COND->IF"
                     clauses))
          (make-if (cond-predicate first)
                   (sequence->exp (cond-actions first))
                   (expand-clauses rest))))))
; StartExercise
#|
(newline)
(display "Exercise 4.2")
; a: no, this will make almost all clauses matched by procedure since as long as it's a pair, it will matched
;    which will result incorrect condtion

; b:
(define (new-application? exp) (tagged-list? exp 'call))
(define (new-operator exp) (cadr exp))
(define (new-operands exp) (cddr exp))

(newline)
(display "Exercise 4.3")
(define eval-data-directed-table make-table)
(define get (eval-data-directed-table 'lookup-proc))
(define put (eval-data-directed-table 'insert-proc))

(put 'eval 'quote text-of-quotation)
(put 'eval 'set! eval-assignment)
(put 'eval 'define eval-definition)
(put 'eval 'if eval-if)
(put 'eval 'lambda (lambda (exp env)
                     (make-procedure (lambda-parameters exp)
                                     (lambda-body exp)
                                     env)))
(put 'eval 'begin (lambda (exp env)
                    (eval-sequence (begin-sequence exp) env)))

(put 'eval 'cond (lambda (exp env)
                   (eval (cond->if exp) env)))

(define (eval-data-directed exp env)
  (cond ((self-evaluating? exp) exp)
        ((variable? exp) (lookup-variable-value exp env))
        ((get 'eval (car exp) (apply (get 'eval (car exp)) exp env)))
        ((application? exp)
         (apply (eval (operator exp) env)
                (list-of-values (operands exp) env)))
        (else (error "Unknown expression type -- EVAL-DATA-DIRECTED" exp)))

(newline)
(display "Exercise 4.4")
(put 'eval 'and eval-and)
(define (eval-and exp env)
  (define (eval-and-exp exps)
    (cond ((null? exps) #t)
          ((eq? #f (eval (car exps) env)) #f)
          (else (eval-and-exp (cdr exps)))))
  (eval-and-exp (cdr exp)))

(put 'eval 'or eval-or)
(define (eval-or exp env)
  (define (eval-or-exp exps)
    (cond ((null? exps) #f)
          ((eq? #t (eval (car exps) env)) #t)
          (else (eval-or-exp (cdr exps)))))
  (eval-or-exp (cdr exp)))

; modify the eval
(define (and? exp) (tagged-list? exp 'and))
(define (or? exp) (tagged-list? exp 'or))

(define (eval-and-or exp env)
  (cond ((and? exp) (eval-and exp env))
        ((or? exp) (eval-or exp env))
        ;;; others
        ))

(newline)
(display "Exercise 4.5")
(define (expand-clauses-extend clauses)
  (if (null? clauses)
      'false
      (let ((first (car clauses))
            (rest (cdr clauses)))
        (if (cond-else-clause? first)
          (if (null? rest)
              (sequence->exp (cond-actions first))
              (error "ESLE clause isn't last: COND->IF" clauses))
          (if (extend-cond? clause)
              ; use a lambda procedure to avoid invoke cond-predicate twice
              ((lambda (predicate-result)
                (make-if predicate-result
                         (sequence->exp ((extend-cond-actions clause) predicate-result))
                         (expand-clauses-extend rest)))
               (cond-predicate first))
              ; normal cond
              (make-if (cond-predicate first)
                       (sequence->exp (cond-actions first))
                       (expand-clauses-extend rest)))))))


(define (extend-cond? clause)
  (eq? (cadr (cond-actions clause) '=>)))

(define (extend-cond-actions clause)
  (caddr clause))

(newline)
(display "Exercise 4.6")
(define (let? exp) (eq? (tagged-list? exp) 'let))
(define (eval-let exp env) (eval (let->combination exp) env))
(define (let-vars exp) (cadr exp))
(define (let-body exp) (caddr exp))

(define (let-vars-params exp) (map car (let-vars exp)))
(define (let-vars-values exp) (map cadr (let-vars exp)))
(define (let->combination exp)
  (list
    (make-lambda (let-vars-params exp) (let-body exp))
    (let-vars-values exp)))

(define (eval exp env)
  (cond ((let? exp) (eval-let exp env))
        ;;; other conditions
        ))

(newline)
(display "Exercise 4.7")
(let* ((x 3)
       (y (+ x 2))
       (z (+ x y 5)))
  (* x z))

(let ((x 3))
  (let ((y (+ x 2)))
    (let ((z (+ x y 5)))
      (* x z))))

(define (let*->nested-lets exp)
  (define (make-let vars body)
    (cond ((< (length vars) 0)
           (error "let* no vars -- LET*->NESTED-LETS" exp))
          ((= (length vars) 1)
           (list 'let vars (let-body exp)))
          (else
            (list 'let
                  (list (car vars))
                  (make-let (list (cdr vars)) body)))))
  (make-let (let-vars exp) (let-body exp)))

(newline)
(display "Exercise 4.8")
(define (let-named-proc exp) (cadr exp))
(define (let-named-vars exp) (caddr exp))
(define (let-named-body exp) (cadddr exp))

(define (let-named-vars-params exp) (map car (let-named-vars exp)))
(define (let-named-vars-values exp) (map cadr (let-named-vars exp)))

(define (let->combination exp)
  (cond ((= (length exp) 3) ; (let ((<var> <exp>) (<var> <exp>)) <body>)
         (list
           (make-lambda (let-vars-params exp) (let-body exp))
           (let-vars-values exp)))
        ((= (length exp) 4)
         (sequence->exp
           (list 'define
                 (cons (let-named-proc exp) (let-named-vars-params exp))
                 (let-named-body exp))
           (cons (let-named-proc exp) (let-named-vars-values exp))))
        (else
          error "Unknown expression --LET->COMBINATION" exp)))

(newline)
(display "Exercise 4.9")
; (while <predicate> <body>)
; while
(define (while? exp) (tagged-list? exp 'while))
(define (while-predicate exp) (cadr exp))
(define (while-body exp) (caddr exp))
(define (while->combination exp)
  (sequence->exp
    (list (list 'define
                'while-iter
                (make-if (while-predicate exp)
                         (sequence->exp
                           (list (while-body exp)
                                 (list 'while-iter)))
                         'true))
          (list 'while-iter))))

(newline)
(display "Exercise 4.10")
;skip
|#
; End StartExercise

(newline)
(display "4.1.3 Evaluator Data Structures")

(newline)
(display "Testing of predicates")
(define (true? x)
  (not (eq? x #f)))

(define (false? x)
  (eq? x #f))

(newline)
(display "Representing procedures")
(define (make-procedure parameters body env)
  (list 'procedure parameters body env))

(define (compound-procedure? p)
  (tagged-list? p 'procedure))

(define (procedure-parameters p) (cadr p))
(define (procedure-body p) (caddr p))
(define (procedure-environment p) (cadddr p))

(newline)
(display "Operations on Environment")

(define (enclosing-environment env) (cdr env))

(define (first-frame env) (car env))

(define the-empty-environment '())

(define (make-frame variables values)
  (cons variables values))

(define (frame-variables frame) (car frame))
(define (frame-values frame) (cdr frame))

(define (add-binding-to-frame! var val frame)
  (set-car! frame (cons var (car frame)))
  (set-cdr! frame (cons val (cdr frame))))

(define (extend-environment vars vals base-env)
  (if (= (length vars) (length vals))
      (cons (make-frame vars vals) base-env)
      (if (< (length vars) (length vals))
          (error "Too many arguments supplied" vars vals)
          (error "Too few arguments supplied" vars vals))))

(define (lookup-variable-value var env)
  (define (env-loop env)
    (define (scan vars vals)
      (cond ((null? vars)
             (env-loop (enclosing-environment env)))
            ((eq? var (car vars))
             (car vals))
            (else (scan (cdr vars) (cdr vals)))))
    (if (eq? env the-empty-environment)
        (error "Unbound variable" var)
        (let ((frame (first-frame env)))
          (scan (frame-variables frame)
                (frame-values frame)))))
  (env-loop env))

(define (set-variable-value! var val env)
  (define (env-loop env)
    (define (scan vars vals)
      (cond ((null? vars)
             (env-loop (enclosing-environment env)))
            ((eq? var (car vars))
             (set-car! vals val))
            (else (scan (cdr vars) (cdr vals)))))
    (if (eq? env the-empty-environment)
        (error "Unbound variable -- SET!" var)
        (let ((frame (first-frame env)))
          (scan (frame-variables frame)
                (frame-values frame)))))
  (env-loop env))

(define (define-variable! var val env)
  (let ((frame (first-frame env)))
    (define (scan vars vals)
      (cond ((null? vars)
             (add-binding-to-frame! var val frame))
            ((eq? var (car vars))
             (set-car! vals val))
            (else (scan (cdr vars) (cdr vals)))))
    (scan (frame-variables frame)
          (frame-values frame))))

; StartExercise
#|
(newline)
(display "Exercise 4.11")
; NOTE: use map
(define (make-frame variables values)
  (if (= (length variables) (length values))
      (map cons variables values)
      (else (error "Length mismatch MAKE-FRAME" variables values))))

(define (frame-variables frame)
  (map car frame))

(define (frame-values frame)
  (map cdr frame))

(define (add-binding-to-frame! var val frame)
  (cons (cons var val) frame))

(newline)
(display "Exercise 4.12")
(define (scan-frame var frame no-vars-callback found-callback)
  (define (scan variables values)
    (cond ((null? variables)
           (no-vars-callback))
          ((eq? var (car variables))
           (found-callback variables values))
          (else (scan (cdr variables) (cdr values)))))
  (scan (frame-variables frame) (frame-values frame)))

(define (search-env var env success-callback)
  (define no-found-callback
    ; search the next environment
    (search-env var (enclosing-environment env) success-callback))
  (if (eq? env the-empty-environment)
      (error "Unbound variable" var)
      (scan-frame var (first-frame env) no-found-callback success-callback)))

(define (lookup-variable-value var env)
  (search-env var env (lambda (vars vals) (car vals))))

(define (set-variable-value! var val env)
  (search-env var env (lambda (vars vals) (set-car! vals val))))

(define (define-variable! var val env)
  (scan-frame
    var
    (first-frame env)
    ; no-found-callback
    (lambda () (add-binding-to-frame! var val frame)
    ; found-callback
    (lambda (vars vals) (set-car! vals val)))))

(newline)
(display "Exercise 4.13")
; We only remove the binding in the first frame if exist, since
; remove binding from other frame may affect binding usage elsewhere,
; which is very hard to debug, or being notified
(define (make-unbound! var env)
  (scan-frame
    var
    (first-frame env)
    (lambda () (error "Unbound variable in current frame" var))
    (lambda (vars vals)
      (begin
        (set-car! vars (cdr vars))
        (set-car! vals (cdr vals))))))

|#
; End StartExercise

(newline)
(display "4.1.4 Running the Evaluator as a Program")
; NOTE: probably need more primitive-procedures
(define primitive-procedures
  (list (list 'car car)
        (list 'cdr cdr)
        (list 'cons cons)
        (list 'null? null?)
        (list 'display display)))

(define (primitive-procedure-names)
  (map car primitive-procedures))

(define (primitive-procedure-objects)
  (map (lambda (proc) (list 'primitive (cadr proc)))
       primitive-procedures))

(define (setup-environment)
  (let ((initial-env
         (extend-environment (primitive-procedure-names)
                             (primitive-procedure-objects)
                             the-empty-environment)))
    (define-variable! 'true #t initial-env)
    (define-variable! 'false #f initial-env)
    initial-env))

(define the-global-environment (setup-environment))

(define (primitive-procedure? proc)
  (tagged-list? proc 'primitive))

(define (primitive-implementation proc) (cadr proc))

; save original apply procedure
(define apply-in-underlying-scheme apply)

; NOTE: apply-in-underlying-scheme
(define (apply-primitive-procedure proc args)
  (begin (display proc)
         (display (primitive-implementation proc))
         (display args)
         ((primitive-implementation proc) args)))

(define input-prompt "::: M-Eval input:")
(define output-prompt "::: M-Eval value:")

(define (driver-loop)
  (prompt-for-input input-prompt)
  (let ((input (read)))
    (let ((output (eval input the-global-environment)))
      (announce-output output-prompt)
      (user-print output)))
  (driver-loop))

(define (prompt-for-input string)
  (newline) (newline) (display string) (newline))

(define (announce-output string)
  (newline) (display string) (newline))

(define (user-print object)
  (if (compound-procedure? object)
      (display (list 'compound-procedure
                     (procedure-parameters object)
                     (procedure-body object)
                     '<procedure-env>))
      (display object)))

; start driver-loop

; NOTE: car, cdr, null? not quite work as expected, as (car '(a b)) return (a b)
; (null? ()) return #f

;(driver-loop)
(newline)
(display "Exercise 4.14")
; The primitive map will be call like (map ('primitive <operator> args))
; which primitive map couldn't handle

(newline)
(display "4.1.5 Data as Programs")
; if procedure try is halts, then (try try) will run-forever, while if
; try doesn't halt, (try try) return 'halted

(newline)
(display "4.1.6 Internal Definition")

(newline)
(display "Exercise 4.16")
; a
(define (lookup-variable-value-unassign var env)
  (define (env-loop env)
    (define (scan vars vals)
      (cond ((null? vars)
             (env-loop( enclosing-enviroment env)))
            ((eq? var (car vars))
             (if (eq? (car vals) '*unassigned*)
                 (error "Unassigned variable" var)
                 (car vals)))
            (else (scan (cdr vars) (cdr vals)))))
    (if (eq? env the-empty-environment)
        (error "Unbound variable" var)
        (let ((frame (first-frame env)))
          (scan (frame-variables frame)
                (frame-values frame)))))
  (env-loop))

; b
(define (scan-out-defines body)
  ())
