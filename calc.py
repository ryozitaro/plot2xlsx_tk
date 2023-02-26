def delta(out_t, in_t, ini_t, formula=False) -> str | float | int:
    if formula:
        return f"={out_t}-{in_t}-{ini_t}"
    else:
        return out_t - in_t - ini_t


def v(spe_height, delta_t, formula=False) -> str | float | int:
    if formula:
        return f"=({spe_height}/100)/{delta_t}"
    else:
        return (spe_height / 100) / delta_t


def poisson(p_v, s_v, formula=False) -> str | float | int:
    if formula:
        return f"=(POWER(({p_v}/{s_v}), 2)-2)/(2*(POWER(({p_v}/{s_v}), 2) - 1))"
    else:
        try:
            p = (((p_v / s_v) ** 2) - 2) / (2 * (((p_v / s_v) ** 2) - 1))
        except ZeroDivisionError:
            p = "#DIV/0!"
        return p
