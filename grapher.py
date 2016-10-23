#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import *
from os import linesep

import click


def _get_longest(strs):
    l = ""
    for st in strs:
        if len(st) > len(l):
            l = st
    return l


def _get_int_len(a):
    return len('%s' % a)

class Point(object):
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_tuple(tuple):
        return Point(*tuple)


def _calculate_coefficient(p1, p2):
    return (p1.y - p2.y) / (p1.x - p2.x)


def _calculate_entry_point(k, p):
    return p.y - k * p.x


def _get_function(p1, p2):
    def func(x):
        k = _calculate_coefficient(p1, p2)
        e = _calculate_entry_point(k, p1)

        return (x * k + e)
    return func


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def _draw_line(length, inp="|", out="|", builders=" "):
    return [inp] + [builders] * (length - (len(inp) + len(out))) + [out] + [linesep]


def _draw_graph_line(line):
    return ''.join(line)


def _draw_point(line, position, el="•"):
    if position > len(line):
        return line
    else:
        line[position] = el
        return line


def draw_graph(height, width, points, connected=False):
    graph = ""

    if connected:
        funcs = map(lambda ps: _get_function(*ps), pairwise(points))
    else:
        ran = range(1, height + 1)
        longst = _get_longest(map(lambda x: '%s' % x, ran))

        for y in ran:
            inp = ' ' * (len(longst) - _get_int_len(y)) + ('%s| ' % y)
            line = _draw_line(width, inp=inp, out="")
            for point in points:
                if point.y == y:
                    line = _draw_point(line, point.x)
                else:
                    pass
            graph = _draw_graph_line(line) + graph

    return graph


def _txt_to_points(file):
    with open(file) as f:
        content = f.read()
        return map(lambda p: Point(
            int(p.split('=')[0]), int(p.split('=')[1])), content.split())

# Click
# ----------------------------------------------------------------------------


@click.command()
@click.option('--height', '-h', default=10, envvar='HEIGHT', help='Number of characters used to display height of a graph.')
@click.option('--width', '-w', default=20, envvar='WIDTH', help='Number of characters used to display width of a graph.')
@click.option('--step', '-s', default=1, envvar='STEP', help='How wide should each space be.')
@click.argument('file', type=click.Path(exists=True))
def grapher(height, width, step, file):
    '''Draws a graph from a given points in a file.'''

    points = _txt_to_points(file)
    graph = draw_graph(height=height, width=width,
                       points=points, connected=False)

    click.echo(graph)


if __name__ == '__main__':
    grapher()
