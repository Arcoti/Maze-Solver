import array
import struct
from dataclasses import dataclass
from typing import BinaryIO

MAGICNUMBER: bytes = b'MAZE'

@dataclass(frozen=True)
class FileHeader:
    formatVersion: int
    width: int
    height: int

    @classmethod
    def read(cls, file: BinaryIO) -> "FileHeader":              # Quotation Marks: Treat as string and then as class when the class is fully parsed
        assert (
            file.read(len(MAGICNUMBER)) == MAGICNUMBER          # Checks if the first few bytes of file (which is the header) matches the Magic Number
        ), "Unknown File Type"

        formatVersion, = struct.unpack("B", file.read(1))       # Read one byte and eat the comma
        width, height = struct.unpack("<2I", file.read(2 * 4))  # Read eigth bytes and eat the coma in between

        return cls(formatVersion, width, height)

    def write(self, file: BinaryIO) -> None:
        file.write(MAGICNUMBER)
        file.write(struct.pack("B", self.formatVersion))        # Unsigned char (0 - 255)
        file.write(struct.pack("<2I", self.width, self.height)) # Little Endian, 2 Unsigned Integers

@dataclass(frozen=True)
class FileBody:
    squareValues: array.array                                           # Module's array class

    @classmethod
    def read(cls, header: FileHeader, file: BinaryIO) -> "FileBody":
        return cls(
            array.array("B", file.read(header.width * header.height))   # Read width * height number of bytes
        )

    def write(self, file: BinaryIO) -> None:
        file.write(self.squareValues.tobytes())                         # Converts array to byte sequece to be written in to BinaryIO file, binary in python may differ