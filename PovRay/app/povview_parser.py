import pyparsing as pp


def make_parser():
    include_line = pp.Suppress(pp.LineStart() + "#" + pp.rest_of_line)

    sign = pp.Optional(pp.one_of("+ -"))

    uinteger = pp.Word("123456789", pp.nums) ^ "0"
    uinteger.set_parse_action(lambda t: int(t[0], 10))
    sinteger = pp.Combine(sign + uinteger)
    sinteger.set_parse_action(lambda t: int(t[0], 10))
    ufloat = uinteger + pp.Optional("." + uinteger)
    ufloat.set_parse_action(lambda t: float(t[0]))
    sfloat = pp.Combine(sign + ufloat)
    sfloat.set_parse_action(lambda t: float(t[0]))

    vector3 = pp.Group(
        pp.Suppress("<")
        + sfloat
        + pp.Suppress(",")
        + sfloat
        + pp.Suppress(",")
        + sfloat
        + pp.Suppress(">")
    )
    rgb_vector3 = pp.Keyword("rgb") + vector3

    light = pp.Group(
        pp.Keyword("light_source")
        + "{"
        + vector3
        + ","
        + pp.Keyword("color")
        + rgb_vector3
        + "}"
    )

    camera = (
        pp.Keyword("camera")
        + "{"
        + pp.Keyword("location")
        + vector3
        + pp.Keyword("look_at")
        + vector3
        + pp.Keyword("up")
        + vector3
        + "}"
    )

    pigment = pp.Optional(
        pp.Keyword("pigment") + "{" + pp.Keyword("color") + rgb_vector3 + "}"
    )
    object_modifiers = pigment

    obj = (
        pp.MatchFirst(pp.Keyword(x) for x in ["ovus"])
        + "{"
        + ufloat
        + pp.Suppress(",")
        + ufloat
        + object_modifiers
        + "}"
    )

    lights = pp.OneOrMore(light)
    cameras = pp.OneOrMore(camera)
    objects = pp.OneOrMore(obj)

    parser = include_line + lights + cameras + objects
    return parser


def main(args):
    p = make_parser()

    with open(args[1], "r", encoding="utf-8") as f:
        s = f.read()

    res = p.parse_string(s)
    print(res)
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
