import xml.etree.ElementTree as ET
from typing import List
import json
from pathlib import Path

def parse_marc_values(xml_file_path: str = "sample_of_records.xml") -> List[str]:
    """
    Parse MARC XML records and join all values into a single string per record
    
    Args:
        xml_file_path: Path to the MARC XML file
    Returns:
        List of strings containing concatenated values
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        all_records = []
        
        for record in root.findall('record'):
            record_values = []
            
            # Get datafield values for 2xx and 6xx ranges only
            for datafield in record.findall('datafield'):
                tag = datafield.get('tag', '')
                
                # Extract values from title fields (2xx) and subject fields (6xx)
                if tag.startswith('2') or tag.startswith('6'):
                    for subfield in datafield.findall('subfield'):
                        if subfield.text and subfield.text.strip():
                            record_values.append(subfield.text.strip())
            
            if record_values:
                # Join all values with a space separator
                all_records.append(' '.join(record_values))
            
        return all_records
        
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return []
    except FileNotFoundError:
        print(f"File not found: {xml_file_path}")
        return []

def save_values_to_file(records: List[str], 
                       output_file: str = "data/marc_values.txt"):
    """
    Save the parsed values to text and JSON files
    """
    Path("data").mkdir(exist_ok=True)
    
    # Save text version
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, record in enumerate(records, 1):
            f.write(f"Record {i}\n{'=' * 50}\n\n")
            f.write(f"{record}\n\n")
    
    # Save JSON version - array of strings
    json_file = output_file.replace('.txt', '.json')
    with open(json_file, 'w', encoding='utf-8') as jf:
        json.dump(records, jf, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    file_path = "./small_sample.xml"
    records = parse_marc_values(file_path)
    
    if records:
        save_values_to_file(records)
        print("\nValues have been saved to data/marc_values.txt")
        print("JSON version saved to data/marc_values.json")
    else:
        print("No records were parsed from the file.")