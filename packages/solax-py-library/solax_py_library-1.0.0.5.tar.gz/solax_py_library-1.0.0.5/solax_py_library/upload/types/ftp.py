import os
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


class FTPFileType(str, Enum):
    CSV = "CSV"

    def get_file_suffix(self):
        return {
            FTPFileType.CSV: ".csv",
        }.get(self)


class FTPData(BaseModel):
    file_type: FTPFileType
    file_name: str
    data: Any

    def build_full_path(self, remote_path) -> str:
        return os.path.join(remote_path, self.file_name)


class FTPServiceConfig(BaseModel):
    host: str
    user: Optional[str]
    password: Optional[str]
    remote_path: str


class FTPParsedData(BaseModel):
    file_name: str
    file_path: str
