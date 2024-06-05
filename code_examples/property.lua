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

function cubeSDF(p, size)
    local dX = p.x
    local dY = p.y
    local uau = p.z
    local maxD = vec3(dX, dY, 0.0)
    return maxD.z
end

function SignedDistance(p)
    return cubeSDF(p, 1.0)
end

function Color(p)
    return vec3(0.0, 0.0, 1.0) 
end

local v = -1.0
print(abs(v))


local distance = SignedDistance(point)
local color = Color(point)
