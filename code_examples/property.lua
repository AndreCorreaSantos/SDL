#in vec3 point, out vec3 color, out float distance, opt width 200, opt height 200, opt steps 5



function abs(v)
    local u = 0.0
    if v < 0.0 then
        u = -v
    else
        u = v
    end

    return u
end

function min(a, b)
    if a < b then
        return a
    else
        return b
    end
end

function max(a, b)
    if a > b then
        return a
    else
        return b
    end
end

function cubeSDF(p, size)
    local halfSize = size / 2.0
    local dX = max(abs(p.x) - halfSize, 0.0)
    local dY = max(abs(p.x) - halfSize, 0.0)
    local dZ = max(abs(p.x) - halfSize, 0.0)

    local minD = min(1.0, min(1.0,1.0))
    return 1.0
end


local t = vec3(0.0, 0.0, 0.0)
local size = 1.0

local u = cubeSDF(t, size)




function SignedDistance(p)
    return 1.0
end

function Color(p)
    return vec3(0.0, 0.0, 1.0) 
end
local distance = SignedDistance(point)
local color = Color(point)