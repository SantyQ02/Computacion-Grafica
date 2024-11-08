import pyparsing as pp
import json
import sys


def make_parser():
    include_line = pp.Suppress(pp.LineStart() + "#" + pp.rest_of_line)

    comma = pp.Suppress(",")
    open_brace = pp.Suppress("{")
    close_brace = pp.Suppress("}")

    sign = pp.Optional(pp.oneOf("+ -"))

    uinteger = pp.Word("123456789", pp.nums) ^ "0"
    sinteger = pp.Combine(sign + uinteger)
    expon = pp.one_of("e E") + sinteger

    ufloat = pp.Combine(uinteger + pp.Optional("." + uinteger) + pp.Optional(expon))
    sfloat = pp.Combine(sinteger + pp.Optional("." + uinteger) + pp.Optional(expon))

    uinteger.set_parse_action(lambda t: int(t[0]))
    sinteger.set_parse_action(lambda t: int(t[0]))
    ufloat.set_parse_action(lambda t: float(t[0]))
    sfloat.set_parse_action(lambda t: float(t[0]))

    vector3 = pp.Group(
        pp.Suppress("<")
        + sfloat("x")
        + comma
        + sfloat("y")
        + comma
        + sfloat("z")
        + pp.Suppress(">")
    )

    color_vector3 = pp.Group(
        pp.Suppress("<")
        + sfloat("r")
        + comma
        + sfloat("g")
        + comma
        + sfloat("b")
        + pp.Suppress(">")
    )

    rgb_vector3 = pp.Keyword("rgb") + color_vector3("color")

    light = pp.Group(
        pp.Keyword("light_source")
        + open_brace
        + vector3("position")
        + comma
        + pp.Keyword("color")
        + rgb_vector3
        + close_brace
    ).setResultsName("light_sources", listAllMatches=True)

    camera = pp.Group(
        pp.Keyword("camera")
        + open_brace
        + pp.Keyword("location")
        + vector3("location")
        + pp.Keyword("look_at")
        + vector3("look_at")
        + pp.Keyword("up")
        + vector3("up")
        + close_brace
    ).setResultsName("cameras", listAllMatches=True)

    pigment = (
        pp.Keyword("pigment")
        + open_brace
        + pp.Keyword("color")
        + rgb_vector3
        + close_brace
    )

    modifiers_list = [pigment]

    object_modifiers = pp.ZeroOrMore(pp.Group(pp.Or(modifiers_list))).setResultsName(
        "object_modifiers", listAllMatches=True
    )

    ovus_parser = (
        pp.Keyword("ovus")("type")
        + open_brace
        + ufloat("bottom_radius")
        + comma
        + ufloat("top_radius")
        + object_modifiers
        + close_brace
    )

    cone_parser = (
        pp.Keyword("ovus")("type")
        + open_brace
        + vector3("bottom_center")
        + comma
        + ufloat("bottom_radius")
        + comma
        + vector3("top_center")
        + comma
        + ufloat("top_radius")
        + object_modifiers
        + close_brace
    )

    object_list = [ovus_parser, cone_parser]

    objects = pp.ZeroOrMore(pp.Group(pp.Or(object_list))).setResultsName(
        "objects", listAllMatches=True
    )

    element = light | camera | objects

    parser = pp.ZeroOrMore(include_line | element)

    parser = pp.Dict(parser)

    return parser


def parse(filename):
    parser = make_parser()

    with open(filename, "r", encoding="utf-8") as f:
        file_contents = f.read()

    try:
        res = parser.parse_string(file_contents, parse_all=True)
    except pp.ParseException as pe:
        print("Parsing failed:", pe)
        sys.exit(1)

    result_dict = res.as_dict()

    result = {
        "light_sources": result_dict.get("light_sources", []),
        "cameras": result_dict.get("cameras", []),
        "objects": result_dict.get("objects", []),
    }

    return result


def main(args):
    if len(args) < 2:
        print("Uso: python parser.py <archivo_entrada.pov>")
        return 1

    result = parse(args[1])

    print(json.dumps(result, indent=4))

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
