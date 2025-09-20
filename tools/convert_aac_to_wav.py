import subprocess
import os

def convert_aac_to_wav_ffmpeg(aac_file_path, wav_file_path):
    """
    Converts an AAC audio file to a WAV audio file using the ffmpeg command-line tool.

    then may use:
    python3 transcribe_wavefile.py --vosk_model vosk-model-de-0.21 output.wav


    Args:
        aac_file_path (str): The path to the input AAC file.
        wav_file_path (str): The desired path for the output WAV file.
    """
    if not os.path.exists(aac_file_path):
        print(f"Error: Input AAC file not found at '{aac_file_path}'")
        return

    # FFmpeg command:
    # ffmpeg -i input.aac output.wav
    command = ["ffmpeg", "-i", aac_file_path, wav_file_path]

    try:
        print(f"Attempting to convert '{aac_file_path}' to '{wav_file_path}' using ffmpeg...")
        # Run the command
        # capture_output=True captures stdout and stderr
        # text=True decodes output as text
        # check=True raises CalledProcessError if the command returns a non-zero exit code
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        print(f"Successfully converted '{aac_file_path}' to '{wav_file_path}'")
        # print("FFmpeg stdout:", result.stdout)
        # print("FFmpeg stderr:", result.stderr) # ffmpeg often prints progress/info to stderr

    except FileNotFoundError:
        print("Error: 'ffmpeg' command not found. Please ensure FFmpeg is installed "
              "and accessible in your system's PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion with ffmpeg (Exit Code {e.returncode}):")
        print("Command:", e.cmd)
        print("FFmpeg stdout:", e.stdout)
        print("FFmpeg stderr:", e.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Example usage:
    # Make sure to replace 'input.aac' with the actual path to your AAC file
    # and 'output.wav' with your desired output path.

    # --- For demonstration purposes: create a dummy AAC file ---
    # In a real scenario, you would replace this with your actual AAC file.
    dummy_input_aac = "example_input.aac"
    if not os.path.exists(dummy_input_aac):
        print(f"Creating a dummy file '{dummy_input_aac}' for demonstration. "
              "Please replace this with your actual AAC file for real conversion.")
        # This creates a very small, technically invalid AAC file,
        # but it allows the script to run without a missing file error.
        # For a real test, you NEED a valid AAC file.
        with open(dummy_input_aac, "wb") as f:
            f.write(b'\x00\x00\x00\x00') # Placeholder for a real AAC header/data
            f.write(b'\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') # More dummy data

    input_aac_file = dummy_input_aac   # Replace with your actual AAC file path
    output_wav_file = "output.wav"      # Replace with your desired WAV file path

    convert_aac_to_wav_ffmpeg(input_aac_file, output_wav_file)

    # --- Clean up dummy file (if it was created) ---
    if input_aac_file == dummy_input_aac and os.path.exists(dummy_input_aac):
        # os.remove(dummy_input_aac) # Uncomment to remove the dummy file after running
        pass # Keeping dummy file for easier re-testing if needed

    print("\nRemember to replace 'example_input.aac' with the path to your actual AAC file.")
