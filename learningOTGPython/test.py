import subprocess

# Path to the C file to compile
c_file = "program.c"

# Output executable name
output_file = "program"

try:
    # Compile the C program using GCC
    subprocess.run(
        ["gcc", c_file, "-o", output_file],  # GCC compilation command
        check=True                          # Raise exception if compilation fails
    )
    print("Compilation successful!")
    
    # Run the compiled executable
    result = subprocess.run(
        ["./" + output_file],              # Command to execute the program
        stdout=subprocess.PIPE,            # Capture standard output
        stderr=subprocess.PIPE             # Capture standard error
    )

    
    # Display the program's output
    print("Program Output:")
    output_string = result.stdout.decode()
    print(output_string)          # Decode and print the output from the executable
    
    
except subprocess.CalledProcessError as e:
    print("An error occurred!")
    print("Error message:", e.stderr.decode())

