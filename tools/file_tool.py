import os
from crewai.tools import BaseTool

class FileWriteTool(BaseTool):
    name: str = "File Writer"
    description: str = "Write content to a file. Input format: 'filename.txt|content to write'"

    def _run(self, input_str: str) -> str:
        try:
            filename, content = input_str.split("|", 1)
            filename = filename.strip()
            os.makedirs("outputs", exist_ok=True)
            filepath = os.path.join("outputs", filename)
            with open(filepath, "w") as f:
                f.write(content)
            return f"Successfully written to {filepath}"
        except Exception as e:
            return f"FIle write failed: {str(e)}"
        
class FileReadTool(BaseTool):
    name: str = "File Reader"
    description: str = "Read content from a file. Input should be the filename."

    def _run(self, filename: str) -> str:
        try:
            filepath = os.path.join("outputs", filename.strip())
            with open(filepath, "r") as f:
                return f.read()
        except FileNotFoundError:
            return f"File '{filename}' not found."
        except Exception as e:
            return f"File read failed: {str(e)}"