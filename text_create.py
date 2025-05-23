import xml.etree.ElementTree as ET
from typing import List, Dict
import json
from pathlib import Path

def parse_marc_values(xml_file_path: str = "sample_of_records.xml") -> Dict[str, str]:
    """
    Parse MARC XML records and create a dictionary with 001 as key and concatenated values as value
    Args: 
        xml_file_path: Path to the MARC XML file
    Returns:
        Dictionary with 001 tag values as keys and concatenated field values as values
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        records_dict = {}
        
        for record in root.findall('record'):
            record_values = []
            record_id = None
            
            # Get the 001 control number
            control_field = record.find("controlfield[@tag='001']")
            if control_field is not None and control_field.text:
                record_id = control_field.text.strip()
            
            # Get datafield values for 2xx and 6xx ranges
            for datafield in record.findall('datafield'):
                tag = datafield.get('tag', '')
                
                if tag.startswith('2') or tag.startswith('6'):
                    for subfield in datafield.findall('subfield'):
                        if subfield.text and subfield.text.strip():
                            record_values.append(subfield.text.strip())
            
            if record_id and record_values:
                records_dict[record_id] = ' '.join(record_values)
            
        return records_dict
        
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return {}
    except FileNotFoundError:
        print(f"File not found: {xml_file_path}")
        return {}

def save_values_to_file(records: Dict[str, str], 
                       output_file: str = "data/marc_values.txt"):
    """
    Save the parsed values to text and JSON files
    """
    Path("data").mkdir(exist_ok=True)
    
    # Save text version
    with open(output_file, 'w', encoding='utf-8') as f:
        for record_id, content in records.items():
            f.write(f"Record ID: {record_id}\n{'=' * 50}\n\n")
            f.write(f"{content}\n\n")
    
    # Save JSON version - object with 001 as keys
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