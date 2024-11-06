import pyparsing as pp
import json
import sys


def make_parser():
    # Definir comentarios que serán ignorados
    include_line = pp.Suppress(pp.LineStart() + "#" + pp.rest_of_line)

    # Definir el análisis de números
    sign = pp.Optional(pp.oneOf("+ -"))

    uinteger = pp.Word("123456789", pp.nums) ^ "0"
    sinteger = pp.Combine(sign + uinteger)
    expon = pp.one_of("e E") + sinteger

    ufloat = pp.Combine(uinteger + pp.Optional("." + uinteger) + pp.Optional(expon))
    sfloat = pp.Combine(sinteger + pp.Optional("." + uinteger) + pp.Optional(expon))

    # Establecer acciones de análisis para convertir cadenas a tipos apropiados
    uinteger.set_parse_action(lambda t: int(t[0]))
    sinteger.set_parse_action(lambda t: int(t[0]))
    ufloat.set_parse_action(lambda t: float(t[0]))
    sfloat.set_parse_action(lambda t: float(t[0]))

    # Definir un vector 3D
    vector3 = pp.Group(
        pp.Suppress("<")
        + sfloat("x")
        + pp.Suppress(",")
        + sfloat("y")
        + pp.Suppress(",")
        + sfloat("z")
        + pp.Suppress(">")
    )

    color_vector3 = pp.Group(
        pp.Suppress("<")
        + sfloat("r")
        + pp.Suppress(",")
        + sfloat("g")
        + pp.Suppress(",")
        + sfloat("b")
        + pp.Suppress(">")
    )

    # Definir vector RGB
    rgb_vector3 = pp.Keyword("rgb") + color_vector3("color")

    # Definir light_source
    light = pp.Group(
        pp.Keyword("light_source")
        + pp.Suppress("{")
        + vector3("position")
        + pp.Suppress(",")
        + pp.Keyword("color")
        + rgb_vector3
        + pp.Suppress("}")
    ).setResultsName("light_sources", listAllMatches=True)

    # Definir camera
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
    ).setResultsName("cameras", listAllMatches=True)

    # Definir pigment (opcional)
    pigment = pp.Optional(
        pp.Keyword("pigment")
        + pp.Suppress("{")
        + pp.Keyword("color")
        + rgb_vector3
        + pp.Suppress("}")
    )

    # Definir modificadores de objeto
    object_modifiers = pigment

    # Definir objeto (e.g., ovus)
    obj = pp.Group(
        pp.MatchFirst(pp.Keyword(x) for x in ["ovus"])("type")
        + pp.Suppress("{")
        + ufloat("bottom_radius")
        + pp.Suppress(",")
        + ufloat("top_radius")
        + pp.Optional(object_modifiers)
        + pp.Suppress("}")
    ).setResultsName("objects", listAllMatches=True)

    # Definir elemento que puede ser un light, camera o object
    element = light | camera | obj

    # Definir el parser general que permite cualquier orden de elementos y comentarios
    parser = pp.ZeroOrMore(include_line | element)

    # Convertir los resultados a un diccionario
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
    make_parser().create_diagram("povview_parser_diagram.html")
