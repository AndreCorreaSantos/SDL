#in vec3 point, out vec3 color, out float distance, opt width 200, opt height 200, opt steps 5

function max(a, b)
    local result
    if a > b then
        result = a
    else
        result = b
    end
    return result
end

function min(a, b)
    local result
    if a < b then
        result = a
    else
        result = b
    end
    return result
end

function abs(v)
    local result = v
    if result < 0.0 then
        result = -v
    else
        result = v
    end
    return result
end

function distance(p1, p2)
    return ((p1.x - p2.x)^2 + (p1.y - p2.y)^2 + (p1.z - p2.z)^2)^0.5
end


function cubeSDF(p, size)
    local halfSize = size / 2.0
    local dX = max(abs(p.x) - halfSize, 0.0)
    local dY = max(abs(p.y) - halfSize, 0.0)
    local dZ = max(abs(p.z) - halfSize, 0.0)
    local maxD = vec3(dX, dY, dZ)
    local minD = min(maxD.x, min(maxD.y, maxD.z))
    return minD + distance(maxD, vec3(0.0, 0.0, 0.0))
end

function SignedDistance(p)
    return cubeSDF(p, 1.0)
end

function Color(p)
    return vec3(0.0, 0.0, 1.0) 
end

local distance = SignedDistance(point)
local color = Color(point)
