def line_intersection(ax: float, ay: float, bx: float, by: float, cx: float, cy: float, dx: float, dy: float):
    # Returns intersection point of two line segments if it exists
    # Line 1: (ax,ay) to (bx,by)
    # Line 2: (cx,cy) to (dx,dy)

    # Calculate the direction vectors
    r = (bx - ax, by - ay)
    s = (dx - cx, dy - cy)

    # Calculate the cross product of the direction vectors
    rxs = r[0] * s[1] - r[1] * s[0]

    # If rxs = 0, lines are parallel
    if abs(rxs) < 1e-10:
        return (False, False)

    # Calculate t and u parameters
    q = (cx - ax, cy - ay)
    t = (q[0] * s[1] - q[1] * s[0]) / rxs
    u = (q[0] * r[1] - q[1] * r[0]) / rxs

    # Check if intersection occurs within both segments
    if 0 <= t <= 1 and 0 <= u <= 1:
        # Calculate intersection point
        pos_x = ax + t * r[0]
        pos_y = ay + t * r[1]
        return (pos_x, pos_y)

    return (False, False)
