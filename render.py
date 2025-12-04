import numpy as np

def render_segment(buf, start, end, onval=255):
    """Generates a list of (x, y) coordinates for a line using Bresenham's algorithm,
       populates a pixel buffer, with "on" pixels set to "onval"."
       """
    x1, y1 = start
    x2, y2 = end

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    points = []
    while True:
        points.append((x1, y1))
        buf[-y1,x1]=onval
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return points


def render_amoeba(buf, xs, ys, onval=255):
    for nobj in np.arange(len(xs)):
        for nseg in np.arange(len(xs[nobj])):
            for nrad in np.arange(len(xs[nobj][nseg])):
                render_segment(buf, (int(xs[nobj][nseg][nrad]),int(ys[nobj][nseg][nrad])),
                    (int(xs[nobj][nseg][nrad]),int(ys[nobj][nseg][nrad])), onval )
    return buf
