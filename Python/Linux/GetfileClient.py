import socket
import sys

s = socket.socket()
s.connect(('192.168.204.155', 1234))

while s:
	print "Enter the operation you want to do [get | end]: "
	oper=sys.stdin.readline()
	oper=oper.replace("\n","")
	if oper == "get":
		print "Enter the file name you want to get: "
		file_name=sys.stdin.readline()
        	file_name=file_name.replace("\n","")
    		cmd = 'get\n%s\n' % (file_name)
    		s.sendall(cmd)
    		r = s.recv(2)
    		size = int(s.recv(16))
    		recvd = ''
		output_file=open(file_name, "wb")
    		while size > len(recvd):
        		data = s.recv(1024)
			output_file.write(data)
        		if not data: 
            			break
        		recvd += data
    		s.sendall('ok')
		print "file: " + file_name + " created."
	elif oper == "end":
		s.sendall('end\n')
		break
