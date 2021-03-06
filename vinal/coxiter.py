#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from subprocess import call
from pathlib import Path

def weight(M, i, j):
    cos2 = (M[i][j]*M[i][j])/(M[i][i]*M[j][j])
    try:
        return {
            0: 2,
            1: 3,
            2: 4,
            3: 6,
            4: 0,
        }[int(4*cos2)]
    except KeyError:
        if cos2 > 1:
            return 1
        else:
            print('coxiter.py ERROR: cosine cannot be ', cos2)
            return -1

def gram_matrix2graph(M, d):
    n = len(M)
    strings = [f'{n} {d-1}\n',]
    for i in range(n):
        for j in range(i):
            if M[i][j] != 0:
                strings.append(f'{j+1} {i+1} {weight(M,i,j)}\n')
    strings.append('\n')
    #print(strings)
    return strings
    

def run(M, d, graph_file = 'graph.txt', answer_file = 'answer.txt', 
                coxiter_dir = Path(__file__).parent.parent.joinpath('CoxIter/build/') ):
    with open(coxiter_dir.joinpath(graph_file), 'w') as graph:
        graph.writelines(gram_matrix2graph(M, d))
    call('bash -c "{0}/coxiter -fv < {0}/{1} > {0}/{2}"'.format(coxiter_dir, graph_file, answer_file), shell=True)
    with open(coxiter_dir.joinpath(answer_file), 'r') as out:
        response = out.readlines()
    question = 'Finite covolume'
    answer = [('yes' in s) for s in response if question in s]
    if len(answer) == 0:
        print(f'"{question}" not found, check answer.txt, you may want to rebuild CoxIter')
        raise Exception('coxiter.py', 'did not find answer')
    return answer[0]