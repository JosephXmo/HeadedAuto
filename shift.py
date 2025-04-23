def compute_offset(target, observation_point, x_rev=False, y_rev=False):
    tx, ty = target
    ox, oy = observation_point

    x_shift = tx - ox if not x_rev else ox - tx
    y_shift = ty - oy if not y_rev else oy - ty

    return x_shift, y_shift
