#include "colors.inc"

light_source {
    <4, 5, -6>, color rgb <1, 1, 1>
}

camera {
    location <0, 100, 0>
    look_at <0, 0, 0>
    up <1, 0, 0>
    angle 45
}

sphere {
    <0,0,0>, 1
    pigment{
        color rgb <1,0,0>
    }
}

sphere {
    <0,-100,0>, 99
    pigment{
        color rgb <1,1,0>
    }
}