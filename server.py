import os
from pathlib import Path
from fastmcp import FastMCP
import asyncio

mcp = FastMCP("system_administration_mcp")

FILE_ROOT = Path(os.getenv("MCP_FILE_ROOT", "/")).resolve()
MOUNT_SOURCE = Path(os.getenv("MCP_MOUNT_SOURCE", "/")).resolve()

def _resolve_requested_path(path_str: str) -> Path:
    """
    Resolve an incoming path string to an actual Path inside the container.
    - If the path exists as given, use it.
    - Otherwise, join it under FILE_ROOT (stripping the leading anchor if absolute).
    - Ensure the final path is inside FILE_ROOT (unless FILE_ROOT == '/').
    """
    req = Path(path_str)
    # If exists as given, use it
    if req.exists():
        cand = req.resolve()
    else:
        p = req
        if MOUNT_SOURCE != Path("/") and str(p).startswith(str(MOUNT_SOURCE)):
            rel = p.relative_to(MOUNT_SOURCE)
        else:
            rel = p.relative_to(p.anchor) if p.is_absolute() else p
        cand = (FILE_ROOT / rel).resolve()

    # Ensure the resolved path is within FILE_ROOT, unless FILE_ROOT is root ('/')
    if FILE_ROOT != Path("/"):
        try:
            cand.relative_to(FILE_ROOT)
        except Exception:
            raise ValueError(f"Resolved path '{cand}' is outside of allowed root '{FILE_ROOT}'")

    return cand

# FastMCP uses asyncio -> good to use async methods
async def _list_directory(dir_path: str) -> list[str]:
    """
    Lists the names of all files and directories in the given directory path.
    """
    try:
        p = _resolve_requested_path(dir_path)

        if not p.is_dir():
            return [f"Error: Path '{dir_path}' resolved to '{p}' is not a valid directory."]
            
        return [item.name for item in p.iterdir()]
    except ValueError as ve:
        return [f"Error: {ve}"]
    except Exception as e:
        return [f"Error listing directory '{dir_path}': {e}"]

async def _get_file_content(file_path: str) -> str:
    """
    Reads the entire content of the file specified by file_path.
    """
    try:
        p = _resolve_requested_path(file_path)

        if not p.is_file():
            return f"Error: Path '{file_path}' resolved to '{p}' which is not a valid file."

        with open(p, 'r', encoding='utf-8') as f:
            return f.read()
    except ValueError as ve:
        return f"Error: {ve}"
    except Exception as e:
        return f"Error reading file '{file_path}': {e}"
    
async def _delete_file(file_path: str) -> str:
    """
    Deletes the specified file.
    """
    try:
        p = _resolve_requested_path(file_path)

        if not p.is_file():
            return f"Error: Path '{file_path}' resolved to '{p}' which is not a valid file."

        p.unlink()
        return f"File '{file_path}' successfully deleted."
    except ValueError as ve:
        return f"Error: {ve}"
    except Exception as e:
        return f"Error deleting file '{file_path}': {e}"

# register tools (keeps the same tool names)
get_file_content = mcp.tool()(_get_file_content)
list_directory = mcp.tool()(_list_directory)
delete_file = mcp.tool()(_delete_file)

if __name__ == "__main__":

    port_string=os.getenv("MCP_PORT", 8080)
    # os.getenv always returns a string, so we need to convert to int to avoid uvicorn errors: Uvicorn running on %s://%s:%d
    port = int(port_string)

    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=port,
        )
    )