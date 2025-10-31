"""
Some smaller models it will sometimes have a working code solution, but it
will still fail to actually save it. This will grab the last output code block
and save that as the final code.
"""
import os
import sys
from fire import Fire # type: ignore

def main(macnet_output_folder: str | None = None, save_to_file: str | None = None):
    """
    Grab the last output code block from each agent's log file and save it as the final code.
    Args:
        macnet_output_folder (str | None): The folder containing agent log files. If None, defaults to 'MacNetLog'/latest folder
        save_to_file (str | None): If provided, saves the final code blocks to this single file.
    """
    folder_of_this_file = os.path.dirname(os.path.abspath(__file__))
    log_root = os.path.join(folder_of_this_file, "MacNetLog")
    if macnet_output_folder is None:
        all_runs = [os.path.join(log_root, d) for d in os.listdir(log_root) if os.path.isdir(os.path.join(log_root, d))]
        latest_run = max(all_runs, key=os.path.getmtime)
        macnet_output_folder = latest_run
    
    # print(f"Using output folder: {output_folder}")
    # Find all .log files in the output_folder
    log_files = [f for f in os.listdir(macnet_output_folder) if f.endswith('.log')]
    if len(log_files) == 0:
        print("No .log files found in the specified output folder.", file=sys.stderr)
        sys.exit(1)
    log_file = log_files[0]

    log_path = os.path.join(macnet_output_folder, log_file)
    with open(log_path, 'r') as f:
        content = f.read()

    blocks = content.split('---')

    for block in reversed(blocks):
        if '```python' not in block:
            continue
        start = block.find('```python') + len('```python')
        end = block.rfind('```')
        if start >= end:
            continue
        code = block[start:end].strip()
        print(code)
        if save_to_file:
            with open(save_to_file, 'a') as f:
                f.write(code + '\n\n')
        break

if __name__ == "__main__":
    Fire(main)