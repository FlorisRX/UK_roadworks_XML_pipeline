Okay, let's refactor the data extraction and loading process to handle both XML formats in a maintainable way. The strategy will be:

1.  **Define a Unified Schema:** Create a single list of target column names that represents the combined data structure we want in the database.
2.  **Create Format-Specific Mappers:** Implement separate functions (`map_new_to_unified`, `map_old_to_unified`) that take a record element (from either format) and return a dictionary conforming to the unified schema. These functions will handle the specific logic (attributes vs. child elements, name differences, nested structures) for each format.
3.  **Generic Directory Processor:** Create a function (`process_directory`) that iterates through XML files in a given directory, applies the correct record XPath, and uses the appropriate mapping function to extract standardized data.
4.  **Unified Database Loader:** Create a function (`load_data_to_duckdb`) that takes the list of standardized dictionaries and loads them into DuckDB.
5.  **Orchestration:** Combine the results from processing both directories and load them.

Here's the proposed implementation:

**1. Define Unified Schema (Update Configuration Cell)**

Review the attributes/elements found for both formats and define the target schema.

````python
# --- Configuration ---
NEW_DATA_DIRECTORY = 'data/new_format'     # data from 2018 onwards
OLD_DATA_DIRECTORY = 'data/old_format' # data from 2017 and earlier

DUCKDB_FILE = 'roadworks_data.duckdb'  # Name for your DuckDB database file
TABLE_NAME = 'planned_roadworks_unified' # Use a new table name for the combined data

# Define the namespace map (only needed for new format)
NSMAP = {'d': 'WebTeam'}

# XPath to find the repeating record element
NEW_ROADWORK_RECORD_XPATH = './/d:HE_PLANNED_WORKS'
OLD_ROADWORK_RECORD_XPATH = './/ha_planned_works' # XPath for the old format record

# --- Define Unified Target Columns ---
# Represents the desired final structure in the database
UNIFIED_TARGET_COLUMNS = [
    'source_filename',      # Provenance
    'event_number',         # Unified ID (from NEW_EVENT_NUMBER or reference_number)
    'start_date',           # Unified (from SDATE or start_date)
    'end_date',             # Unified (from EDATE or end_date)
    'expected_delay',       # Unified (from EXPDEL or expected_delay)
    'description',          # Unified
    'closure_type',         # Unified
    'status',               # Unified
    'published_date',       # Unified
    'centre_easting',       # Unified (nested in new, direct in old)
    'centre_northing',      # Unified (nested in new, direct in old)
    'road_numbers',         # Unified (nested in new, 'road' in old - may need joining logic if old has multiple)
    'location',             # Old format specific (or potentially map from new description?)
    'local_authority',      # Old format specific
    'traffic_management',   # Old format specific
    'old_reference_number'  # New format specific (OLD_REFERENCE_NUMBER attribute)
]

# Define XPaths for nested data relative to the NEW format HE_PLANNED_WORKS element
NEW_COORD_XPATH = './d:EASTNORTH/d:Report/d:EASTINGNORTHING/d:EASTNORTH_Collection/d:EASTNORTH'
NEW_ROAD_XPATH = './d:ROADS/d:Report/d:ROADS/d:ROAD_Collection/d:ROAD'

# How many records to inspect in detail (used in exploration functions)
NUM_RECORDS_TO_INSPECT = 3
# ---
````

**2. Create Format-Specific Mappers (New Cells)**

````python
def map_new_to_unified(record_element, source_filename):
    """
    Extracts data from a 'new' format <HE_PLANNED_WORKS> element
    and maps it to the UNIFIED_TARGET_COLUMNS schema.
    """
    data = {col: None for col in UNIFIED_TARGET_COLUMNS} # Initialize with None
    data['source_filename'] = source_filename

    # --- Map direct attributes ---
    data['event_number'] = record_element.get('NEW_EVENT_NUMBER')
    data['start_date'] = record_element.get('SDATE')
    data['end_date'] = record_element.get('EDATE')
    data['expected_delay'] = record_element.get('EXPDEL')
    data['description'] = record_element.get('DESCRIPTION')
    data['closure_type'] = record_element.get('CLOSURE_TYPE')
    data['status'] = record_element.get('STATUS')
    data['published_date'] = record_element.get('PUBLISHED_DATE')
    data['old_reference_number'] = record_element.get('OLD_REFERENCE_NUMBER') # New format specific

    # Basic check - skip if no event number
    if data.get('event_number') is None:
        # print(f"Warning: New format record missing NEW_EVENT_NUMBER in {source_filename}. Skipping.")
        return None

    # --- Extract nested coordinates ---
    coord_elements = record_element.xpath(NEW_COORD_XPATH, namespaces=NSMAP)
    if coord_elements:
        coord_element = coord_elements[0]
        data['centre_easting'] = coord_element.get('CENTRE_EASTING')
        data['centre_northing'] = coord_element.get('CENTRE_NORTHING')

    # --- Extract nested roads ---
    road_elements = record_element.xpath(NEW_ROAD_XPATH, namespaces=NSMAP)
    if road_elements:
        road_numbers_list = [road.get('ROAD_NUMBER') for road in road_elements if road.get('ROAD_NUMBER')]
        # Join multiple roads with a separator (e.g., '; ')
        data['road_numbers'] = '; '.join(road_numbers_list) if road_numbers_list else None

    return data

def map_old_to_unified(record_element, source_filename):
    """
    Extracts data from an 'old' format <ha_planned_works> element
    and maps it to the UNIFIED_TARGET_COLUMNS schema.
    """
    data = {col: None for col in UNIFIED_TARGET_COLUMNS} # Initialize with None
    data['source_filename'] = source_filename

    # Helper to get text content safely
    def get_text(tag_name):
        element = record_element.find(tag_name)
        return element.text.strip() if element is not None and element.text else None

    # --- Map child elements ---
    data['event_number'] = get_text('reference_number')
    data['start_date'] = get_text('start_date')
    data['end_date'] = get_text('end_date')
    data['expected_delay'] = get_text('expected_delay')
    data['description'] = get_text('description')
    data['closure_type'] = get_text('closure_type')
    data['status'] = get_text('status')
    data['published_date'] = get_text('published_date')
    data['centre_easting'] = get_text('centre_easting')
    data['centre_northing'] = get_text('centre_northing')
    data['road_numbers'] = get_text('road') # Assuming single 'road' tag in old format
    data['location'] = get_text('location') # Old format specific
    data['local_authority'] = get_text('local_authority') # Old format specific
    data['traffic_management'] = get_text('traffic_management') # Old format specific

    # Basic check - skip if no event number
    if data.get('event_number') is None:
        # print(f"Warning: Old format record missing reference_number in {source_filename}. Skipping.")
        return None

    return data
````

**3. Generic Directory Processor (New Cell)**

````python
def process_directory(directory_path, record_xpath, extraction_func, nsmap=None):
    """
    Processes all XML files in a directory using a specific XPath and extraction function.

    Args:
        directory_path (str): Path to the directory containing XML files.
        record_xpath (str): XPath expression to find record elements.
        extraction_func (callable): Function to call for each record element found.
                                    It should accept (record_element, source_filename)
                                    and return a dictionary or None.
        nsmap (dict, optional): Namespace map for XPath evaluation. Defaults to None.

    Returns:
        list: A list of dictionaries, where each dictionary represents a processed record.
    """
    all_records_data_dicts = []
    xml_files = glob.glob(os.path.join(directory_path, '*.xml'))
    parser = etree.XMLParser(recover=True, ns_clean=True) # Use robust parser

    if not xml_files:
        print(f"Warning: No XML files found in directory: {directory_path}")
        return []

    print(f"\n--- Processing Directory: {directory_path} ---")
    print(f"Found {len(xml_files)} XML files.")

    total_processed_records = 0
    total_skipped_records = 0
    files_with_errors = 0

    for file_path in xml_files:
        filename = os.path.basename(file_path)
        # print(f"Processing file: {filename}...") # Optional verbose output
        try:
            tree = etree.parse(file_path, parser)
            root = tree.getroot()
            # Find records using the provided XPath and namespace map
            records = root.xpath(record_xpath, namespaces=nsmap)

            if not records:
                # print(f"  Warning: No records found matching XPath in {filename}.")
                continue

            file_record_count = 0
            file_skipped_count = 0
            for record in records:
                try:
                    extracted_dict = extraction_func(record, filename)
                    if extracted_dict:
                        all_records_data_dicts.append(extracted_dict)
                        file_record_count += 1
                    else:
                        file_skipped_count += 1 # Count records skipped by extraction func
                except Exception as e_rec:
                    # Try to get an ID for logging, adapt based on potential extraction func errors
                    event_id = "UNKNOWN_ID"
                    try:
                        if nsmap: # Likely new format
                             event_id = record.get('NEW_EVENT_NUMBER', event_id)
                        else: # Likely old format
                             ref_num_el = record.find('reference_number')
                             if ref_num_el is not None and ref_num_el.text:
                                 event_id = ref_num_el.text.strip()
                    except: pass # Ignore errors getting ID for logging
                    print(f"  Error processing record {event_id} in {filename}: {e_rec}")
                    file_skipped_count += 1

            # if file_record_count > 0 or file_skipped_count > 0: # Only print if something happened
            #    print(f"  Extracted {file_record_count} valid records from {filename}. Skipped {file_skipped_count}.")

            total_processed_records += file_record_count
            total_skipped_records += file_skipped_count

        except etree.XMLSyntaxError as e_xml:
            print(f"  Error parsing XML file {filename}: {e_xml}. Skipping file.")
            files_with_errors += 1
        except Exception as e_file:
            print(f"  An unexpected error occurred processing file {filename}: {e_file}. Skipping file.")
            files_with_errors += 1

    print(f"--- Directory Scan Complete: {directory_path} ---")
    print(f"Successfully extracted {total_processed_records} records.")
    if total_skipped_records > 0:
        print(f"Skipped {total_skipped_records} records (missing ID or processing error).")
    if files_with_errors > 0:
        print(f"Skipped {files_with_errors} files due to parsing/file errors.")

    return all_records_data_dicts
````

**4. Unified Database Loader (New Cell)**

````python
def load_data_to_duckdb(db_file, table_name, data_dicts, target_columns):
    """
    Loads a list of data dictionaries into a DuckDB table.

    Args:
        db_file (str): Path to the DuckDB database file.
        table_name (str): Name of the table to create or replace.
        data_dicts (list): A list of dictionaries, each representing a row.
        target_columns (list): The list of column names in the desired order.
    """
    if not data_dicts:
        print("No data provided to load into the database. Aborting.")
        return

    print(f"\n--- Loading Data into DuckDB ---")
    print(f"Target Table: {table_name}")
    print(f"Number of records to load: {len(data_dicts)}")

    # --- Convert list of dictionaries to list of tuples/lists for insertion ---
    # Ensure data is in the order specified by target_columns
    data_to_insert = []
    for record_dict in data_dicts:
        row_values = [record_dict.get(col_name) for col_name in target_columns]
        data_to_insert.append(row_values)

    # --- Load data into DuckDB directly using executemany ---
    print(f"Connecting to DuckDB database: {db_file}")
    con = None # Initialize connection variable
    try:
        con = duckdb.connect(database=db_file, read_only=False)

        print(f"Creating or replacing table: {table_name}")
        # Quote column names to handle potential spaces or special characters
        column_defs = [f'"{col}" VARCHAR' for col in target_columns]
        create_table_sql = f"CREATE OR REPLACE TABLE \"{table_name}\" ({', '.join(column_defs)})"
        con.execute(create_table_sql)

        print(f"Inserting {len(data_to_insert)} records into {table_name}...")

        # Create the SQL insert statement with placeholders
        placeholders = ', '.join(['?'] * len(target_columns))
        # Quote table name in insert statement as well
        insert_sql = f'INSERT INTO "{table_name}" VALUES ({placeholders})'

        # Execute the insert statement for all rows
        con.executemany(insert_sql, data_to_insert)

        con.commit() # Commit the transaction
        print("Data insertion complete and committed.")

        # Verify insertion (optional)
        count_result = con.execute(f'SELECT COUNT(*) FROM "{table_name}"').fetchone()
        print(f"Verification: Table '{table_name}' now contains {count_result[0]} rows.")

    except duckdb.Error as e_db: # Catch specific DuckDB errors
        print(f"Database error: {e_db}")
        if con:
            try:
                print("Attempting to rollback transaction.")
                con.rollback()
            except duckdb.Error as e_tx: # Catch potential errors during rollback
                print(f"Rollback failed: {e_tx}")
    except Exception as e:
         print(f"An unexpected error occurred during DB operation: {e}")
         if con:
             try:
                con.rollback()
             except duckdb.Error as e_tx:
                print(f"Rollback failed: {e_tx}")
    finally:
        if con:
            con.close()
            print("Database connection closed.")
````

**5. Orchestration (New Cell to run the process)**

````python
# --- Main Data Processing and Loading ---

# 1. Process the 'new' format directory
new_format_data = process_directory(
    directory_path=NEW_DATA_DIRECTORY,
    record_xpath=NEW_ROADWORK_RECORD_XPATH,
    extraction_func=map_new_to_unified,
    nsmap=NSMAP
)

# 2. Process the 'old' format directory
old_format_data = process_directory(
    directory_path=OLD_DATA_DIRECTORY,
    record_xpath=OLD_ROADWORK_RECORD_XPATH,
    extraction_func=map_old_to_unified,
    nsmap=None # No namespace expected for old format
)

# 3. Combine the data from both formats
all_data = new_format_data + old_format_data

# 4. Load the combined data into DuckDB
load_data_to_duckdb(
    db_file=DUCKDB_FILE,
    table_name=TABLE_NAME, # Using the unified table name from config
    data_dicts=all_data,
    target_columns=UNIFIED_TARGET_COLUMNS
)

print("\n--- Data Pipeline Complete ---")
````

**Explanation and Benefits:**

*   **Maintainability:** Each format's extraction logic is isolated in its own `map_..._to_unified` function. If a format changes or a new one is added, you only need to modify or add a specific mapping function and update the orchestration cell.
*   **Reusability:** `process_directory` and `load_data_to_duckdb` are generic and can be reused.
*   **Clarity:** The orchestration cell clearly shows the steps: process new, process old, combine, load.
*   **Unified Schema:** Working towards a single, well-defined `UNIFIED_TARGET_COLUMNS` makes downstream analysis easier.
*   **Robustness:** Using `recover=True` in the parser and adding `try...except` blocks around record processing makes the pipeline more resilient to errors in individual files or records.
*   **Efficiency:** `executemany` is used for efficient bulk insertion into DuckDB.

Remember to remove or comment out the old `extract_record_data_as_dict` and `process_xml_files` functions to avoid confusion. You should now run the new configuration cell and the subsequent new cells to execute the unified pipeline.