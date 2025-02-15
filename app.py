from flask import Flask, request, render_template, jsonify
import subprocess
import os
import tempfile
from pathlib import Path
import logging
import signal
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

MAX_EXECUTION_TIME = 5
MAX_OUTPUT_SIZE = 50000
COMPILE_TIMEOUT = 10

class CompilationError(Exception):
    pass

class ExecutionError(Exception):
    pass

def sanitize_output(output: str, max_length: int = MAX_OUTPUT_SIZE) -> str:
    """Sanitize and truncate output if necessary"""
    if len(output) > max_length:
        return output[:max_length] + "\n... (Output truncated due to length)"
    return output

def compile_and_run(code: str, temp_dir: str) -> str:
    """Compile and run C code with proper error handling"""
    c_file = os.path.join(temp_dir, "code.c")
    output_file = os.path.join(temp_dir, "program")
    
    try:
        with open(c_file, 'w') as f:
            f.write(code)
    except IOError as e:
        raise CompilationError(f"Failed to write code to file: {str(e)}")

    try:
        compile_result = subprocess.run(
            ["gcc", c_file, "-o", output_file, "-Wall", "-Wextra"],
            capture_output=True,
            text=True,
            timeout=COMPILE_TIMEOUT
        )
        
        if compile_result.returncode != 0:
            raise CompilationError(compile_result.stderr)
    except subprocess.TimeoutExpired:
        raise CompilationError("Compilation timed out")
    except subprocess.SubprocessError as e:
        raise CompilationError(f"Compilation failed: {str(e)}")

    try:
        result = subprocess.run(
            [output_file],
            capture_output=True,
            text=True,
            timeout=MAX_EXECUTION_TIME
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\nErrors:\n{result.stderr}"
        
        return sanitize_output(output)
    except subprocess.TimeoutExpired:
        raise ExecutionError("Program execution timed out (possible infinite loop)")
    except subprocess.SubprocessError as e:
        raise ExecutionError(f"Program execution failed: {str(e)}")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/run/", methods=['POST'])
def run_code():
    code = request.form.get('programByUser', '').strip()
    if not code:
        return render_template("home.html", code_result="No code provided")

    temp_dir = tempfile.mkdtemp()
    try:
        output = compile_and_run(code, temp_dir)
        return render_template("home.html", 
                             code=code,
                             code_result=output)
    except CompilationError as e:
        logger.error(f"Compilation error: {str(e)}")
        return render_template("home.html",
                             code=code,
                             code_result=f"Compilation Error:\n{str(e)}")
    except ExecutionError as e:
        logger.error(f"Execution error: {str(e)}")
        return render_template("home.html",
                             code=code,
                             code_result=f"Execution Error:\n{str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return render_template("home.html",
                             code=code,
                             code_result="An unexpected error occurred. Please try again.")
    finally:


        try:
            if os.path.exists(temp_dir):
                for file in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, file))
                os.rmdir(temp_dir)
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)