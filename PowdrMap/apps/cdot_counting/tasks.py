#!/usr/bin/env python
from celery import task

#each task must start with @app.task
#the ignore_result is if we don't want the state to be stored
@task(ignore_result=True) 
def print_hello():
    print 'hello there'


@task()
def gen_prime(x):
    multiples = []
    results = []
    for i in xrange(2, x + 1):
        if i not in multiples:
            results.append(i)
            for j in xrange(i*i, x+1, i):
                multiples.append(j)
    return results

