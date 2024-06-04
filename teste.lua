

function distance(point1, point2)
    return ((point1.x - point2.x)^2 + (point1.y - point2.y)^2 + (point1.z - point2.z)^2)^0.5
end
    
function sphereSDF(point)
    local center = vec3(0, 0, 0)
    local radius = 1.0
    return distance(point, center) - radius
end

function SignedDistance(point)
    return sphereSDF(point)
end

function Color(point)
    return vec3(1, 0, 0)
end


