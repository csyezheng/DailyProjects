#lang racket

(provide (all-defined-out))
;------------------------------
(define (make-ordered-queue less?)
  (define (make)
    empty
    )
  (define (empty? queue)
    (null? queue)
    )
  (define (top queue)
    (car queue)
    )
  (define (pop queue)
    (cdr queue)
    )
  (define (insert queue item)
    (if (or (null? queue) (less? item (car queue)))
      (cons item queue)
      (cons (car queue) (insert (cdr queue) item)))
    )

  (define queue (make))

  (lambda (m . args)
    (cond 
      ((eq? m 'empty?) (empty? queue))
      ((eq? m 'top) (top queue))
      ((eq? m 'pop!) (set! queue (pop queue)))
      ((eq? m 'insert!) (set! queue (insert queue (car args)))))
    )
  )

;------------------------------
(define (make-agenda)
  (mcons 0 (make-ordered-queue (lambda (a b) (< (car a) (car b)))))
  )
(define (agenda-current-time agenda)
  (mcar agenda)
  )
(define (agenda-time-queue agenda)
  (mcdr agenda)
  )
(define (agenda-set-current-time! agenda time)
  (set-mcar! agenda time)
  )
(define (agenda-empty? agenda)
  ((agenda-time-queue agenda) 'empty?)
  )
(define (agenda-pop-action! agenda)
  (let ((item ((agenda-time-queue agenda) 'top)))
    ((agenda-time-queue agenda) 'pop!)
    (agenda-set-current-time! agenda (car item))
    (cdr item))
  )
(define (agenda-add-action! agenda delay action)
  ((agenda-time-queue agenda) 'insert! (cons (+ delay (agenda-current-time agenda)) action))
  )

;------------------------------
(define the-agenda (make-agenda))
(define (after-delay delay action)
  (agenda-add-action! the-agenda delay action)
  )
(define (propagate)
  (if (agenda-empty? the-agenda)
    (agenda-current-time the-agenda)
    (let ((action (agenda-pop-action! the-agenda)))
      (action)
      (propagate)))
  )

;------------------------------
(define (make-wire)
  (mcons false empty)
  )
(define (get-signal wire)
  (mcar wire)
  )
(define (set-signal! wire signal)
  (if (eq? signal (get-signal wire))
    'ok
    (begin (set-mcar! wire signal)
           (for-each (lambda (f) (f)) (mcdr wire))))
  )
(define (add-signal-action! wire action)
  (set-mcdr! wire (cons action (mcdr wire)))
  (action)
  )

;------------------------------
(define not-gate-delay 2)
(define and-gate-delay 3)
(define or-gate-delay 5)

(define (not-gate in out)
  (define (action)
    (define new-signal (not (get-signal in)))
    (after-delay not-gate-delay 
                 (lambda () (set-signal! out new-signal)))
    )
  (add-signal-action! in action)
  )
(define (and-gate in1 in2 out)
  (define (action)
    (define new-signal (and (get-signal in1) (get-signal in2)))
    (after-delay and-gate-delay 
                 (lambda () (set-signal! out new-signal)))
    )
  (add-signal-action! in1 action)
  (add-signal-action! in2 action)
  )
(define (or-gate in1 in2 out)
  (define (action)
    (define new-signal (or (get-signal in1) (get-signal in2)))
    (after-delay or-gate-delay 
                 (lambda () (set-signal! out new-signal)))
    )
  (add-signal-action! in1 action)
  (add-signal-action! in2 action)
  )

;------------------------------
(define (half-adder a b s c)
  (define d (make-wire))
  (define e (make-wire))
  (and-gate a b c)
  (or-gate a b d)
  (not-gate c e)
  (and-gate d e s)
  )
(define (full-adder a b cin sum cout)
  (define s (make-wire))
  (define c1 (make-wire))
  (define c2 (make-wire))
  (half-adder b cin s c1)
  (half-adder a s sum c2)
  (or-gate c1 c2 cout)
  )

;------------------------------
(define (probe name wire)
  (add-signal-action! 
    wire
    (lambda ()
      (newline)
      (display name)
      (display " ")
      (display (agenda-current-time the-agenda))
      (display " New-value = ")
      (display (if (get-signal wire) 1 0))))
  )

;------------------------------
;
(define input-1 (make-wire))
(define input-2 (make-wire))
(define sum (make-wire))
(define carry (make-wire))
(probe 'sum sum)
(probe 'carry carry)

(half-adder input-1 input-2 sum carry)

(set-signal! input-1 true)
(printf "\n@done: ~a\n" (propagate))

(set-signal! input-2 true)
(printf "\n@done: ~a\n" (propagate))
