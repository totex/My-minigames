local socket = require('socket')
udp = socket.udp()
udp:setsockname('*', 12345)
udp:settimeout(0)

local greenX, greenY = '100', '100'
local redX, redY = '400', '100'

function love.draw()
	love.graphics.setColor(0, 1, 0)
	love.graphics.rectangle("fill", greenX, greenY, 50, 50)

	love.graphics.setColor(1, 0, 0)
	love.graphics.rectangle("fill", redX, redY, 50, 50)
end

function love.update()
	greenX, greenY = love.mouse.getPosition()
	data, msg_or_ip, port_or_nil = udp:receivefrom()
	print(data)
	if data then
		local p = split(data, '-')
		redX, redY = p[1], p[2]
		udp:sendto(tostring(greenX)..'-'..tostring(greenY), msg_or_ip, port_or_nil)
	end
end

function split(s, delimiter)
	result = {}
	for match in (s..delimiter):gmatch("(.-)"..delimiter) do
		table.insert(result, match)
	end
	return result
end
