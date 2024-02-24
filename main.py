import cmd
import os
import json


class FileManagerCLI(cmd.Cmd):
    prompt = 'FileMngr>> '
    intro = 'Welcome to FileManagerCLI. Type "help" for available commands.'

    def __init__(self):
        super().__init__()
        self.current_directory = os.getcwd()

    def add_data(self, args):
        filename, function, key, value = args
        file_path = os.path.join(self.current_directory, filename)
        try:
            with open(file_path, 'r') as existing_file:
                file_content = existing_file.read()  # Read file content before closing
                # print(file_content)
        except FileNotFoundError:
            # print(f"File '{filename}' not found or empty.")
            file_content = None  # Set file_content to None if file doesn't exist

        try:
            data = json.loads(file_content) if file_content is not None else {}
        except json.JSONDecodeError:
            data = {}

        data[key] = value

        with open(file_path, 'w') as f:
            json.dump(data, f)

        print(f"Key '{key}' with value '{value}' has been dumped to {filename}.")

    def remove_data(self, args):
        filename, function, key = args
        file_path = os.path.join(self.current_directory, filename)
        try:
            with open(file_path, 'r') as existing_file:
                file_content = existing_file.read()  # Read file content before closing
                # print(file_content)
        except FileNotFoundError as e:
            print(f"File '{filename}' not found.")
            file_content = None  # Set file_content to None if file doesn't exist
            return
        try:
            data = json.loads(file_content) if file_content is not None else {}
        except json.JSONDecodeError:
            data = {}


        if key in data:
            value = data[key]
            del data[key]
        else:
            print(f"Key '{key}' not found in JSON data.")
            return

        if not data:
            self.delete_file(filename)
            print(f"Key '{key}' with value '{value}' has been removed from {filename}.")
        else:
            with open(file_path, 'w') as f:
                json.dump(data, f)
                print(f"Key '{key}' with value '{value}' has been removed from {filename}.")

    def read_data(self, filename):
        file_path = os.path.join(self.current_directory, filename)
        try:
            with open(file_path, 'r') as existing_file:
                file_content = existing_file.read()  # Read file content before closing
                print(file_content)
        except FileNotFoundError as e:
            print(f"File '{filename}' not found.")
            return

    def read_data_from_key(self, filename, key):
        file_path = os.path.join(self.current_directory, filename)
        try:
            with open(file_path, 'r') as existing_file:
                file_content = existing_file.read()  # Read file content before closing
                # print(file_content)
        except FileNotFoundError as e:
            print(f"File '{filename}' not found.")
            return
        try:
            data = json.loads(file_content) if file_content is not None else {}
        except json.JSONDecodeError:
            data = {}
        if key in data:
            print(data[key])
        else:
            print(f"key is not present in '{filename}'")

    def delete_file(self, filename):
        file_path = os.path.join(self.current_directory, filename)
        try:
            os.remove(file_path)
            # print(f"File '{filename}' deleted successfully.")
        except FileNotFoundError:
            return

    def do_json_dump(self, args):
        args = args.split()
        if len(args) == 2:
            filename, function = args
            if function == "read":
                self.read_data(filename)
            else:
                print("Invalid command, Try json_dump 'filename' 'read'")

        elif len(args) == 3:
            filename, function, key = args
            if function == "remove":
                self.remove_data(args)
            elif function == "read":
                self.read_data_from_key(filename, key)
            else:
                print("Invalid command")
                return
        elif len(args) == 4:
            filename, function, key, value = args
            if function == "add":
                self.add_data(args)
            else:
                print("Invalid command. Use json_dump 'filename' 'add' 'key' 'value'")
        else:
            print("Invalid command format.")
            return

    def do_quit(self, line):
        """Exit the CLI."""
        return True


    def postcmd(self, stop, line):
        # print()  # Add an empty line for better readability
        return stop


if __name__ == '__main__':
    FileManagerCLI().cmdloop()