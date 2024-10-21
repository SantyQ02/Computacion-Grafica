import pyparsing as pp


def make_parser():
    # Define comments to be ignored
    include_line = pp.Suppress(pp.LineStart() + "#" + pp.rest_of_line)

    # Define number parsing
    sign = pp.Optional(pp.oneOf("+ -"))

    uinteger = pp.Word("123456789", pp.nums) ^ "0"
    sinteger = pp.Combine(sign + uinteger)
    expon = pp.one_of("e E") + sinteger

    ufloat = pp.Combine(uinteger + pp.Optional("." + uinteger) + pp.Optional(expon))
    sfloat = pp.Combine(sinteger + pp.Optional("." + uinteger) + pp.Optional(expon))

    # Set parse actions to convert strings to appropriate types
    uinteger.set_parse_action(lambda t: int(t[0]))
    sinteger.set_parse_action(lambda t: int(t[0]))
    ufloat.set_parse_action(lambda t: float(t[0]))
    sfloat.set_parse_action(lambda t: float(t[0]))

    # Define a 3D vector
    vector3 = pp.Group(
        pp.Suppress("<")
        + sfloat("x")
        + pp.Suppress(",")
        + sfloat("y")
        + pp.Suppress(",")
        + sfloat("z")
        + pp.Suppress(">")
    )

    # Define RGB vector
    rgb_vector3 = pp.Keyword("rgb") + vector3("color")

    # Define light_source
    light = pp.Group(
        pp.Keyword("light_source")
        + pp.Suppress("{")
        + vector3("position")
        + pp.Suppress(",")
        + pp.Keyword("color")
        + rgb_vector3
        + pp.Suppress("}")
    )

    # Define camera
    camera = pp.Group(
        pp.Keyword("camera")
        + pp.Suppress("{")
        + pp.Keyword("location")
        + vector3("location")
        + pp.Keyword("look_at")
        + vector3("look_at")
        + pp.Keyword("up")
        + vector3("up")
        + pp.Suppress("}")
    )

    # Define pigment (optional)
    pigment = pp.Optional(
        pp.Keyword("pigment")
        + pp.Suppress("{")
        + pp.Keyword("color")
        + rgb_vector3
        + pp.Suppress("}")
    )

    # Define object modifiers
    object_modifiers = pigment

    # Define object (e.g., ovus)
    obj = pp.Group(
        pp.MatchFirst(pp.Keyword(x) for x in ["ovus"])("type")
        + pp.Suppress("{")
        + ufloat("bottom_radius")
        + pp.Suppress(",")
        + ufloat("top_radius")
        + pp.Optional(object_modifiers)
        + pp.Suppress("}")
    )

    # Define multiple lights, cameras, and objects with result names
    lights = pp.OneOrMore(light).setResultsName("light_sources")
    cameras = pp.OneOrMore(camera).setResultsName("cameras")
    objects = pp.OneOrMore(obj).setResultsName("objects")

    # Define the overall parser structure
    parser = pp.ZeroOrMore(include_line) + lights + cameras + objects

    # Convert the results to a dictionary
    parser = pp.Dict(parser)

    return parser


def parse(filename):
    parser = make_parser()

    with open(filename, "r", encoding="utf-8") as f:
        file_contents = f.read()

    res = parser.parse_string(file_contents, parse_all=True)
    result_dict = res.as_dict()

    result = {
        "light_sources": result_dict.get("light_sources", []),
        "cameras": result_dict.get("cameras", []),
        "objects": result_dict.get("objects", []),
    }

    return result


def main(args):
    import sys
    import json

    result = parse(args[1])

    print(json.dumps(result, indent=4))

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
