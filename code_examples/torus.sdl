#in vec3 point, out vec3 color, out float distance, opt width 100, opt height 100, opt steps 5

function Length2D(v)
    return (v.x * v.x + v.y * v.y)^0.5
end

function torusSDF(p, R, r)
    local q = vec2(Length2D(vec2(p.x, p.y)) - R, p.z)
    return Length2D(q) - r
end

function SignedDistance(p)
    print("a")
    print(p)
    return torusSDF(p,1.0,0.5)

end

function Color(p)

    local normalized_x = (p.x + 50.0) / 100.0  
    local normalized_y = (p.y + 50.0) / 100.0 
    local r = normalized_x
    local g = 0.0
    local b = 0.0
    return vec3(r, g, b)
end

local distance = SignedDistance(point)
local color = Color(point)
