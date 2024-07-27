import subprocess
from genson import SchemaBuilder
import json


def main():
    subprocess.run(["sh", "-c", f"mkdir ./dist"])
    inputFile = {
        "./jsonSchemas/exampleConfig.json",
    }
    outputFile = {
        "./dist/configschema.json",
    }

    for i in inputFile & outputFile:
        JsonSchema(i, outputFile)


def JsonSchema(inputFile, outputFile):
    builder = SchemaBuilder()
    json_file_path = inputFile

    try:
        # Read the JSON file and parse it into a Python dictionary
        with open(json_file_path, "r") as file:
            data = json.load(file)
        builder.add_object(data)
        builder.to_schema()
        schema = builder.to_json(indent=2)
        subprocess.run(["sh", "-c", f"mkdir ./dist"])
        subprocess.run(["sh", "-c", f"echo '{schema}' > ./dist/{outputFile}"])
        print("Schema generated successfully!")
    except FileNotFoundError:
        print(f"The file {json_file_path} was not found.")
    except json.JSONDecodeError:
        print(f"There was an error decoding the JSON from {json_file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred while processing {json_file_path}: {e}")


__main__ = main()
