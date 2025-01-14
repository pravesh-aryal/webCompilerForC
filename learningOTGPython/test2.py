import subprocess




subprocess = subprocess.run('ls -la', shell = True, capture_output = True, text = True)
print(subprocess.args)
print(subprocess.returncode)
print("___________________________________________________________")
print(subprocess.stdout)
print(subprocess.stdout.decode())
