#include "colors.inc"

light_source {
    <0, 30, 0>, color rgb <1, 1, 1>
}

camera {
    location <0, 20, 0>
    look_at <0, 0, 0>
    angle 45
}

sphere {
    <0,1,0>, 1
    pigment{
        color rgb <1,0,0>
    }
}

box {
    <-100,-100,-100>,<100,0,100> 
    pigment{
        color rgb <1,1,0>
    }
}