import os
from pathlib import Path
from fastmcp import FastMCP
import asyncio

mcp = FastMCP("system_administration_mcp")

# FastMCP uses asyncio -> good to use async methods
@mcp.tool()
async def get_file_content(file_path: str) -> str:
    """
    Reads the entire content of the file specified by file_path.
    
    Args:
        file_path (str): The path to the file to read.
    
    Returns:
        str: The content of the file, or an error message if the file cannot be read. 
    """

    try:
        if not os.path.isfile(file_path):
            return f"Error: Path '{file_path}' is not a valid file."
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file '{file_path}': {e}"
    
@mcp.tool()
async def list_directory(dir_path: str) -> list[str]:
    """
    Lists the names of all files and directories in the given directory path.
    
    Args:
        dir_path (str): The path to the directory to list.
        
    Returns:
        list[str]: A list of file and directory names (not full paths), 
                    or a list containing an error message.
    """
    try:
        path = Path(dir_path)

        if not path.is_dir()    :
            return [f"Error: Path '{dir_path}' is not a valid directory."]
            
        return [item.name for item in path.iterdir()]
    except Exception as e:
        return [f"Error listing directory '{dir_path}': {e}"]
    

if __name__ == "__main__":
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=os.getenv("MCP_PORT", 8080),
        )
    )