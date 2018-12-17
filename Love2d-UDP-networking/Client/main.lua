local socket = require "socket"
local address, port = "localhost", 12345
udp = socket.udp()
udp:setpeername(address, port)
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
	redX, redY = love.mouse.getPosition()
	udp:send(tostring(redX)..'-'..tostring(redY))
	data = udp:receive()
	if data then
		local p = split(data, '-')
		greenX, greenY = p[1], p[2]
	end
end

function split(s, delimiter)
	result = {}
	for match in (s..delimiter):gmatch("(.-)"..delimiter) do
		table.insert(result, match)
	end
	return result
end
