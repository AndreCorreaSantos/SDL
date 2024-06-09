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
    -- Normalize coordinates to be within the range [0, 1]
    -- Assuming `p.x` and `p.y` vary from -50 to +50
    local normalized_x = sin(p.x)  -- Adjusting by adding 50 and dividing by total width
    local normalized_y = cos(p.x)  -- Adjusting by adding 50 and dividing by total height
    print(normalized_x)

    -- Clamp the values to ensure they are within [0, 1]
    local r = normalized_x
    local g = normalized_y
    local b = 0.0  -- Constant blue component



    return vec3(r, g, b)
end

function sdf(p)
    local distance = 1.0
    if p.z > 0.0 then
        distance = 0.0
    end
    return distance -- fazendo isso para garantir que a imagem não se forme atrás do plano da câmera
end

local distance = sdf(point)
local color = Color(point)
