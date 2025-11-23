from pathlib import Path
from src.io.base import BaseClient
from src.config import local_storage_settings


class LocalClient(BaseClient):
    """
    Local file-based storage backend for testing.
    Stores key-value pairs as files in a local directory.
    """
    
    def __init__(self):
        """
        Initialize local storage client.
        
        Args:
            storage_dir: Directory to store files. Defaults to './local_storage'
        """
        self.storage_dir = Path(local_storage_settings.DIR)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_file_path(self, key: str) -> Path:
        """
        Get the file path for a given key.
        Sanitizes the key to ensure it's a valid filename.
        
        Args:
            key: The storage key
            
        Returns:
            Path object for the file
        """
        # Sanitize key to be filesystem-safe
        # Replace any path separators and dangerous characters
        safe_key = key.replace("/", "_").replace("\\", "_")
        safe_key = "".join(c for c in safe_key if c.isalnum() or c in "._-")
        
        # Prevent directory traversal
        if safe_key in ("", ".", ".."):
            safe_key = f"key_{hash(key)}"
        
        return self.storage_dir / safe_key
    
    def get_object(self, key: str) -> bytes:
        """
        Retrieve an object from local storage.
        
        Args:
            key: The storage key
            
        Returns:
            The stored value as bytes
            
        Raises:
            FileNotFoundError: If the key does not exist
            IOError: For other file system errors
        """
        file_path = self._get_file_path(key)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Key '{key}' not found")
        
        try:
            with open(file_path, "rb") as f:
                return f.read()
        except IOError as e:
            raise IOError(f"Failed to read key '{key}': {str(e)}")
    
    def put_object(self, key: str, value: bytes) -> None:
        """
        Store an object in local storage.
        
        Args:
            key: The storage key
            value: The value to store as bytes
            
        Raises:
            IOError: If writing fails
        """
        file_path = self._get_file_path(key)
        
        try:
            # Write atomically using a temporary file
            temp_path = file_path.with_suffix(file_path.suffix + ".tmp")
            with open(temp_path, "wb") as f:
                f.write(value)
            # Atomic rename
            temp_path.replace(file_path)
        except IOError as e:
            raise IOError(f"Failed to write key '{key}': {str(e)}")

