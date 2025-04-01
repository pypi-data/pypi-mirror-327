import os
import pty
import subprocess
import sys
import json

def run_with_live_output(command):
    """Helper function to run command with live output using PTY"""
    master_fd, slave_fd = pty.openpty()
    
    process = subprocess.Popen(
        command,
        stdout=slave_fd,
        stderr=slave_fd,
        text=True
    )
    
    os.close(slave_fd)
    
    try:
        while True:
            output = os.read(master_fd, 1024*1024)
            if not output:
                break

            if hasattr(sys.stdout, "buffer"):
                sys.stdout.buffer.write(output)
            else:
                sys.stdout.write(output)
            sys.stdout.flush()
    except OSError:
        pass  # The PTY may close when the process ends
    
    process.wait()
    return process.returncode

def start_training(
    model_path,
    model_id,
    model_revision,
    dataset_path,
    recipe_path,
    recipe_id,
    recipe_revision,
    run_path,
    client_params,
    adapter_name,
):
    """
    Start training with proper output handling using PTY.
    """
    run_file_path = os.path.join(os.path.dirname(__file__), "run.py")
    
    command = [
        "deepspeed",
        run_file_path,
        "--model_path", model_path,
        "--dataset_path", dataset_path,
        "--recipe_path", recipe_path,
        "--run_path", run_path,
        "--client_params", json.dumps(client_params),
        "--adapter_name", adapter_name,
        "--recipe_id", recipe_id,
        "--recipe_revision", recipe_revision,
        "--model_id", model_id,
        "--model_revision", model_revision,
    ]

    return run_with_live_output(command)