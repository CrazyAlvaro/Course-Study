#lang r6rs
; 4.3 Variation on a Scheme - Nondeterministic Computing

; Parsing natural language
(define nouns '(noun student professor cat class))
(define verbs '(verb studies lectures eats sleeps))
(define articles '(article the a))

; (sentence (noun-phrase (article the) (noun cat))
;           (verb eats))

(define parse-sentence
  (list 'sentence
        (parse-noun-phrase)
        (parse-word verbs)))

(define parse-noun-phrase
  (list 'noun-phrase
        (parse-word articles)
        (parse-word nouns)))

; global variable: *unparsed* is the input that has not yet been parsed
(define (parse-word word-list)
  (require (not (null? *unparsed*)))
  (require (memq (car *unparsed*) (cdr word-list)))
  (let ((found-word (car *unparsed*)))
    (set! *unparsed* (cdr *unparsed*))
    (list (car word-list) found-word)))

(define *unparsed* '())

(define (parse input)
  (set! *unparsed* input)
  (let ((sent (parse-sentence)))
    (require (null? *unparsed*))
    sent))
