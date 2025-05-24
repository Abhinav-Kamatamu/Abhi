import os
import shutil

def get_max_number(folder):
    """
    Finds the maximum number from .png filenames (e.g., '123.png') in the given folder.
    """
    max_num = 0
    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' does not exist!")
        return -1  # Indicates an error or non-existent folder

    print(f"\nChecking .png files in: {os.path.abspath(folder)}")
    for filename in os.listdir(folder):
        if filename.lower().endswith('.png'): # Check for .png files, case-insensitive
            name_part = filename[:-4] # Remove '.png'
            if name_part.isdigit():
                num = int(name_part)
                print(f"Found numbered PNG file: {filename} (value: {num})")
                if num > max_num:
                    max_num = num
    print(f"Max number found in '{folder}': {max_num}")
    return max_num

def process_source_folder(source_folder, target_folder, start_num):
    """
    Processes .png files from the source_folder, renames them sequentially
    starting from start_num + 1, and moves them to the target_folder.
    Returns the new maximum number after processing.
    """
    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' does not exist!")
        return start_num # Return original start_num if source folder is missing

    print(f"\nProcessing source folder: {os.path.abspath(source_folder)} into {os.path.abspath(target_folder)}")
    files_to_process = []
    for filename in os.listdir(source_folder):
        if filename.lower().endswith('.png'): # Check for .png files, case-insensitive
            name_part = filename[:-4] # Remove '.png'
            if name_part.isdigit():
                num = int(name_part)
                files_to_process.append(num) # Store original number for sorting
                print(f"Found numbered PNG file: {filename}")

    if not files_to_process:
        print(f"No valid numbered .png files found to process in '{source_folder}'")
        return start_num

    files_to_process.sort() # Sort by the original number to maintain order
    current_max_in_target = start_num
    print(f"Starting renaming/moving from number: {current_max_in_target + 1}")

    for original_num in files_to_process:
        src_filename = f"{original_num}.png"
        src_path = os.path.join(source_folder, src_filename)

        # Check if the specific source file still exists (it might have been moved if names clashed, though unlikely with sort)
        if not os.path.exists(src_path):
            print(f"Warning: Source file {src_path} not found, possibly already moved or deleted. Skipping.")
            continue

        new_num_for_target = current_max_in_target + 1
        dest_filename = f"{new_num_for_target}.png"
        dest_path = os.path.join(target_folder, dest_filename)

        print(f"Processing: {src_path} -> {dest_path}")

        try:
            shutil.move(src_path, dest_path)
            current_max_in_target = new_num_for_target # Update only on successful move
            print("Success!")
        except Exception as e:
            print(f"Error moving file '{src_filename}': {str(e)}")

    return current_max_in_target

def main():
    base_target_folder = '1'  # All files will be consolidated here

    print("Script starting...")
    print(f"Current working directory: {os.getcwd()}")

    # Ensure the base target folder exists. If not, create it.
    if not os.path.exists(base_target_folder):
        print(f"Base target folder '{base_target_folder}' does not exist. Creating it.")
        try:
            os.makedirs(base_target_folder)
            print(f"Folder '{base_target_folder}' created successfully.")
        except OSError as e:
            print(f"Error creating base target folder '{base_target_folder}': {e}. Exiting.")
            return

    # Get the initial maximum number in the base target folder
    current_overall_max_num = get_max_number(base_target_folder)
    # get_max_number returns -1 if folder1 itself doesn't exist, but we create it now.
    # If it's empty, it returns 0.

    source_folder_index = 2  # Start looking for source folders from '2'
    while True:
        current_source_folder_name = str(source_folder_index)
        print(f"\n--- Checking for source folder: '{current_source_folder_name}' ---")

        if not os.path.exists(current_source_folder_name):
            print(f"Source folder '{current_source_folder_name}' not found. All available source folders processed.")
            break # Stop if the next numbered folder doesn't exist

        updated_max_after_processing = process_source_folder(
            current_source_folder_name,
            base_target_folder,
            current_overall_max_num
        )

        if updated_max_after_processing == current_overall_max_num:
            print(f"No new files were processed from folder '{current_source_folder_name}'.")
        else:
            print(f"Files from '{current_source_folder_name}' processed. New max number: {updated_max_after_processing}")

        current_overall_max_num = updated_max_after_processing
        source_folder_index += 1 # Move to the next potential source folder number

    print(f"\nOperation complete. All .png files consolidated into '{base_target_folder}'.")
    print(f"Final number sequence in '{base_target_folder}' ends at: {current_overall_max_num}")

if __name__ == "__main__":
    main()
