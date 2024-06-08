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
    local result
    if a < b then -- IF PARECE ESTAR QUEBRADO !!!!!!!!!!!!!!!!!!!!! CONSERTAR IF, AS VEZES RETORNA NONE PARA CIMA
        result = a
    else
        result = b
    end
    return result
end

function max(a, b)
    local result
    if a > b then
        result = a
    else
        result = b
    end
    return result
end

local minD = min(1.0, 1.0)

local min2 = min(1.0,minD)




function SignedDistance(p)
    return 1.0
end

function Color(p)
    return vec3(0.0, 0.0, 1.0) 
end
local distance = SignedDistance(point)
local color = Color(point)
