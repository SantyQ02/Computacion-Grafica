#include "colors.inc"

light_source {
    <4, 5, -6>, color rgb <1, 1, 1>
}

camera {
    location <0, 5, -5>
    look_at <0, 0, 0>
    up <0, 1, 0>
}

sphere {
    <0, 0, 0>, 1
    pigment {
        color rgb <1, 1, 0>
    }
}