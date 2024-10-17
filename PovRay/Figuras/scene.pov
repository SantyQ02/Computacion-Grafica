cone { 
    <2, 1, 1>, 0.5, 
    <4, 2, 1.5>, 0.9
    pigment {color rgb <1, 1, 0>} 
}

box {
    <0.2, 0.2, 0.2>,
    <-0.2, -0.2, -0.2>
    pigment {color rgb <1, 1, 1>}
}

camera {
    location <3, 3, -5>
    look_at <3, 2, 0>
    up <0, 1, 0>
}

light_source {
    <0, 5, 0>
    color rgb <1, 1, 1>
}

