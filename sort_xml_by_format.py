import os
import shutil
from lxml import etree

# --- Configuration ---
SOURCE_XML_DIR = "data/downloaded_xml_files"  # Directory containing the XML files to sort
NEW_FORMAT_DIR = "data/new_format"
OLD_FORMAT_DIR = "data/old_format"
UNKNOWN_FORMAT_DIR = "data/unknown_format" # Optional: for files that don't match
# --- End Configuration ---

def sort_xml_files_by_format():
    """
    Sorts XML files from a source directory into 'new_format' or 'old_format'
    directories based on their root element.
    """
    os.makedirs(NEW_FORMAT_DIR, exist_ok=True)
    os.makedirs(OLD_FORMAT_DIR, exist_ok=True)
    os.makedirs(UNKNOWN_FORMAT_DIR, exist_ok=True) # Create if you want to move unknown files

    print(f"Source XML directory: {os.path.abspath(SOURCE_XML_DIR)}")
    print(f"New format XMLs will be moved to: {os.path.abspath(NEW_FORMAT_DIR)}")
    print(f"Old format XMLs will be moved to: {os.path.abspath(OLD_FORMAT_DIR)}")
    print(f"Unknown format XMLs will be moved to: {os.path.abspath(UNKNOWN_FORMAT_DIR)}")
    print("-" * 30)

    files_processed = 0
    files_moved_new = 0
    files_moved_old = 0
    files_unknown = 0
    files_error = 0

    if not os.path.isdir(SOURCE_XML_DIR):
        print(f"Error: Source directory '{SOURCE_XML_DIR}' not found.")
        return

    for filename in os.listdir(SOURCE_XML_DIR):
        if filename.lower().endswith('.xml'):
            files_processed += 1
            source_filepath = os.path.join(SOURCE_XML_DIR, filename)
            target_dir = None
            moved = False

            try:
                # Parse the XML file
                # We use `recover=True` to try and parse even if there are minor errors,
                # but for format detection, the root element is key.
                parser = etree.XMLParser(recover=True)
                tree = etree.parse(source_filepath, parser=parser)
                root = tree.getroot()

                # Remove namespace prefix if present for easier tag comparison
                # e.g. {WebTeam}Report -> Report
                root_tag_name = etree.QName(root.tag).localname
                root_namespace = etree.QName(root.tag).namespace if root.tag.startswith('{') else None


                if root_tag_name == "Report":
                    # For new format, we can also check the namespace if it's consistently "WebTeam"
                    # The example shows xmlns="WebTeam", so the namespace URI would be "WebTeam"
                    # However, some parsers might not expose it this way directly without more complex namespace handling.
                    # Checking the root tag "Report" is often sufficient if "ha_planned_roadworks" is distinct.
                    # If you need to be stricter and check the default namespace:
                    # if root_tag_name == "Report" and root.nsmap.get(None) == "WebTeam":
                    target_dir = NEW_FORMAT_DIR
                    files_moved_new += 1
                elif root_tag_name == "ha_planned_roadworks":
                    target_dir = OLD_FORMAT_DIR
                    files_moved_old += 1
                else:
                    target_dir = UNKNOWN_FORMAT_DIR # Move to unknown if neither
                    files_unknown += 1
                    print(f"File '{filename}' has an unrecognized root element: '{root.tag}'. Moving to unknown.")

            except etree.XMLSyntaxError as e:
                target_dir = UNKNOWN_FORMAT_DIR # Or handle errors differently
                files_error += 1
                print(f"Error parsing XML file '{filename}': {e}. Moving to unknown.")
            except Exception as e:
                target_dir = UNKNOWN_FORMAT_DIR # Or handle errors differently
                files_error += 1
                print(f"An unexpected error occurred with file '{filename}': {e}. Moving to unknown.")

            if target_dir:
                destination_filepath = os.path.join(target_dir, filename)
                try:
                    # Ensure the destination directory exists (it should, from the start)
                    # os.makedirs(target_dir, exist_ok=True) # Redundant if created at start
                    shutil.move(source_filepath, destination_filepath)
                    if target_dir != UNKNOWN_FORMAT_DIR : # Don't print success for unknowns already printed
                        print(f"Moved '{filename}' to '{target_dir}'")
                    moved = True
                except Exception as e_move:
                    print(f"Error moving file '{filename}' to '{destination_filepath}': {e_move}")
                    if target_dir == NEW_FORMAT_DIR: files_moved_new -=1
                    elif target_dir == OLD_FORMAT_DIR: files_moved_old -=1
                    elif target_dir == UNKNOWN_FORMAT_DIR and files_unknown > 0 : files_unknown -=1 # if it was counted as unknown but failed to move
                    files_error +=1 # Count as an error if move fails

    print("-" * 30)
    print("Sorting Summary:")
    print(f"Total XML files found in source: {files_processed}")
    print(f"Moved to New Format ({NEW_FORMAT_DIR}): {files_moved_new}")
    print(f"Moved to Old Format ({OLD_FORMAT_DIR}): {files_moved_old}")
    print(f"Moved to Unknown Format ({UNKNOWN_FORMAT_DIR}): {files_unknown + files_error}") # Includes parsing errors moved to unknown
    # print(f"Files with parsing/processing errors (moved to unknown or not moved): {files_error}")


if __name__ == "__main__":
    # Before running, ensure:
    # 1. `lxml` is installed: pip install lxml
    # 2. The SOURCE_XML_DIR contains your XML files.
    # 3. The target directories (NEW_FORMAT_DIR, OLD_FORMAT_DIR, UNKNOWN_FORMAT_DIR)
    #    are writable or will be created.

    if not os.path.exists(SOURCE_XML_DIR) or not os.listdir(SOURCE_XML_DIR):
        print(f"Source directory '{SOURCE_XML_DIR}' is empty or does not exist.")
        print("Please populate it with XML files before running the sorter.")
    else:
        sort_xml_files_by_format()
    print("\nScript finished.")