import yaml
import os
from pathlib import Path
from typing import List, Dict, Generator

def list_files(path: Path) -> Generator[Path, None, None]:
    """
    Yields a list of files under the provided path.
    If it's a file, yields it. If it's a directory, walks it.
    """
    if path.is_file():
        yield path
    elif path.is_dir():
        for root, _, files in os.walk(path):
            for file in files:
                yield Path(root) / file
    else:
        # Might be a glob or invalid path, for now we only support existing files/dirs
        pass

def load_config(config_path: str) -> List[Dict]:
    """
    Loads groups from a YAML configuration file.
    Example format:
    groups:
      - name: group_name
        paths:
          - path/to/folder
          - path/to/file
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    groups = []
    for group_cfg in config.get('groups', []):
        name = group_cfg.get('name')
        paths = group_cfg.get('paths', [])
        
        all_files = []
        for p in paths:
            all_files.extend(list(list_files(Path(p))))
        
        groups.append({
            'name': name,
            'files': all_files
        })
    return groups
