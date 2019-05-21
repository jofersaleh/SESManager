import subprocess as sp
import sys

print(sys.argv[1])
pipe = sp.Popen(["python", "./sample/simulation_instance.py", sys.argv[1]], stdin=sp.PIPE, stdout=sp.PIPE)

#log = []
f = open("sim_result.log")
for l in pipe.stdout:
#   log.append(l.decode('ascii').strip())
    f.write(l)
f.close()




#for line in pipe.stdout.read():
#    print(line)