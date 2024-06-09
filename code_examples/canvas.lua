#in vec3 point, out vec3 color, out float distance, opt width 100, opt height 100, opt steps 5

function abs(p)
    local result
    if p < 0.0 then
        result = -p
    else
        result = p
    end
    return result
end

function Color(p)
    local normalized_x = (sin(10.0*p.x) +1.0)/2.0
    local normalized_y = (cos(10.0*p.y)+1.0)/2.0
    local r = normalized_x
    local g = normalized_y
    local b = 0.0 
    return vec3(r, g, b)
end

function sdf(p)
    local distance = 1.0
    if p.z > 0.0 then
        distance = 0.0
    end
    return distance
end

local distance = sdf(point)
local color = Color(point)
