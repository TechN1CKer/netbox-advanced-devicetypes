import os
import yaml
import requests

# Configuration
NETBOX_URL = "http://127.0.0.1:8000/api/"  # Update this
NETBOX_TOKEN = "7f0c09b008caee62349ef9ab6ffee539a7b8fa21"  # Update this
DEVICE_TYPES_PATH = "./device-types"  # Update this to your actual folder

HEADERS = {
    "Authorization": f"Token {NETBOX_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def get_manufacturers():
    """Get list of manufacturer folders from the given path."""
    return [d for d in os.listdir(DEVICE_TYPES_PATH) if os.path.isdir(os.path.join(DEVICE_TYPES_PATH, d))]

def select_manufacturers(manufacturers):
    """Prompt user to select manufacturers or choose all."""
    print("\nAvailable Manufacturers:")
    for idx, mfr in enumerate(manufacturers, 1):
        print(f"{idx}. {mfr}")
    print("0. All Manufacturers")

    choice = input("\nEnter the number of the manufacturer(s) to add (comma-separated), or '0' for all: ")
    if choice.strip() == "0":
        return manufacturers
    else:
        selected_indices = [int(i) - 1 for i in choice.split(",") if i.isdigit() and 0 <= int(i) - 1 < len(manufacturers)]
        return [manufacturers[i] for i in selected_indices]

def upload_yaml_files(manufacturer):
    """Upload all YAML files in a manufacturer's directory to NetBox."""
    manufacturer_path = os.path.join(DEVICE_TYPES_PATH, manufacturer)
    
    for file in os.listdir(manufacturer_path):
        if file.endswith(".yaml") or file.endswith(".yml"):
            file_path = os.path.join(manufacturer_path, file)
            with open(file_path, "r") as yaml_file:
                try:
                    data = yaml.safe_load(yaml_file)
                    response = requests.post(f"{NETBOX_URL}dcim/device-types/", headers=HEADERS, json=data)
                    
                    if response.status_code in [200, 201]:
                        print(f"✅ Successfully added {data.get('model', 'Unknown Model')} from {manufacturer}")
                    else:
                        print(f"❌ Failed to add {file}: {response.text}")

                except yaml.YAMLError as e:
                    print(f"❌ YAML parsing error in {file}: {e}")

def main():
    manufacturers = get_manufacturers()
    if not manufacturers:
        print("No manufacturers found! Make sure your directory structure is correct.")
        return
    
    selected_manufacturers = select_manufacturers(manufacturers)
    
    for manufacturer in selected_manufacturers:
        print(f"\n📤 Uploading device types for: {manufacturer}")
        upload_yaml_files(manufacturer)

    print("\n🎉 Device type upload complete!")

if __name__ == "__main__":
    main()