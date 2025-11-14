import sys
import subprocess
import os

def test_transcript_fetch(video_id: str):
    """
    A simple, isolated script to fetch a YouTube transcript using the CLI
    and save the raw output to a file for inspection.
    """
    output_filename = "transcript_output.txt"
    print(f"Attempting to fetch transcript for video ID: {video_id}")
    print(f"Raw output will be saved to: {output_filename}")

    try:
        # Construct the absolute path to the venv's python executable
        # This ensures we use the correct interpreter with the installed packages
        script_dir = os.path.dirname(os.path.abspath(__file__))
        python_executable = os.path.join(script_dir, 'venv', 'Scripts', 'python.exe')
        
        # Command to get the transcript, we ask for json format
        command = [
            python_executable,
            "-m",
            "youtube_transcript_api",
            "--languages",
            "vi",
            "en",
            "--format",
            "json",
            "--",
            video_id
        ]

        # Execute the command and capture its output
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding='utf-8'
            # We remove 'check=True' to capture output even if the command fails
        )

        # Write all results to a file for easy inspection
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("--- COMMAND EXECUTED ---\n")
            f.write(" ".join(command) + "\n\n")
            f.write("--- EXIT CODE ---\n")
            f.write(str(result.returncode) + "\n\n")
            f.write("--- STDOUT (Standard Output) ---\n")
            f.write(result.stdout if result.stdout.strip() else "[STDOUT was empty]")
            f.write("\n\n--- STDERR (Standard Error) ---\n")
            f.write(result.stderr if result.stderr.strip() else "[STDERR was empty]")

        print(f"\nDone. Please open and inspect the file '{output_filename}'.")
        print("It contains the exit code, standard output, and standard error from the command.")

    except Exception as e:
        print(f"An unexpected error occurred while trying to run the subprocess: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_transcript_api.py <YOUTUBE_VIDEO_ID>")
        print("Example: python backend/test_transcript_api.py mScpHTIi-kM")
        sys.exit(1)
    
    # The video ID is the first argument after the script name
    video_id_to_test = sys.argv[1]
    test_transcript_fetch(video_id_to_test)
