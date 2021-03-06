(define (build-list n proc)
  (define (iter i result)
    (if (= 0 i)
      result
      (iter (- i 1) (cons (proc (- i 1)) result)))
    )
  (iter n empty)
  )
(define (foldl proc init l)
  (if (null? l)
    init
    (foldl proc (proc (car l) init) (cdr l)))
  )
(define (map proc l)
  (if (null? l)
    empty
    (cons (proc (car l)) (map proc (cdr l))))
  )
(define (filter pred l)
  (cond
    ((null? l) empty)
    ((pred (car l)) (cons (car l) (filter pred (cdr l))))
    (else (filter pred (cdr l))))
  )
(define (curry n f . boundArgs)
  (lambda args 
    (let ((all-args (append boundArgs args)))
      (if (>= (length all-args) n)
        (apply f all-args)
        (apply curry n f all-args))))
  )
(define (for-each proc l)
  (if (empty? l)
    'ok
    (begin (proc (car l))
           (for-each proc (cdr l))))
  )
