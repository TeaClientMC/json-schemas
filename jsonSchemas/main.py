import glob
import os
import subprocess
from genson import SchemaBuilder
import json
import hashlib


# A function to run commands eaiser by using a function
def proccess_command(command, check_call=False):
    shell = ["sh", "-c", command]
    try:
        if check_call is True:
            subprocess.check_call(shell)
        else:
            subprocess.run(shell)
    except Exception as e:
        print(
            "An unexpected error occurred while running the command: {} error: {}".format(
                command, e
            )
        )


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


# Main function to generate JSON schemas and SHA256 hashes and output them to the ./dist directory
def main():
    try:
        proccess_command(f"rm -rf {ROOT_DIR}/dist", check_call=True)
        proccess_command(f"rm -rf {ROOT_DIR}/shas", check_call=True)
        proccess_command(f"mkdir -p {ROOT_DIR}/dist")
        proccess_command(f"mkdir -p {ROOT_DIR}/dist/shas")
        input_dir = f"{ROOT_DIR}/examples"

        # Get all JSON files from the examples directory
        input_files = glob.glob(f"{input_dir}/*.json")

        # Generate output filenames by replacing '.json' with 'Schema.json'
        output_files = [
            f"{os.path.splitext(os.path.basename(file))[0]}Schema"
            for file in input_files
        ]

        for input_file, output_file in zip(input_files, output_files):
            genSchemaFromJsonFile(input_file, output_file + ".json")
            ShaHashGenerator(
                f"{ROOT_DIR}/dist/{output_file}.json",
                f"{ROOT_DIR}/dist/shas/{output_file}.json.sha256",
            )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Generates a SHA256 hash for a given file
def ShaHashGenerator(input_file, output_file):
    with open(input_file, "rb") as f:
        sha256_hash = hashlib.sha256(f.read()).hexdigest()

    with open(output_file, "w") as f:
        f.write(sha256_hash)


# Generates a JSON schema from a given JSON file
def genSchemaFromJsonFile(inputFile, outputFile):
    builder = SchemaBuilder()
    json_file_path = inputFile

    try:
        # Read the JSON file and parse it into a Python dictionary
        with open(json_file_path, "r") as file:
            data = json.load(file)
        builder.add_object(data)
        builder.to_schema()
        schema = builder.to_json(indent=2)
        subprocess.run(["sh", "-c", f"echo '{schema}' > {ROOT_DIR}/dist/{outputFile}"])
        print("Schema generated successfully!")
    except FileNotFoundError:
        print(f"The file {json_file_path} was not found.")
    except json.JSONDecodeError:
        print(f"There was an error decoding the JSON from {json_file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred while processing {json_file_path}: {e}")


if __name__ == "__main__":
    main()
