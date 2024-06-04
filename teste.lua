
function distance(p1, p2)
    return ((p1.x - p2.x)^2 + (p1.y - p2.y)^2 + (p1.z - p2.z)^2)^0.5
end
    
function sphereSDF(p)
    local center = vec3(0.0, 0.0, 0.0)
    local radius = 1.0
    return distance(p, center) - radius
end

function SignedDistance(p)
    return sphereSDF(p)
end

function Color(p)
    return vec3(1.0, 0.0, 0.0)
end

print(SignedDistance(point))
print(Color(point))

