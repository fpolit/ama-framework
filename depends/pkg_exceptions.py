#!/usr/bin/env python3
#
# Exceptions to manage error in Package class
#
# Maintainer: glozanoa <glozanoa@uni.pe>

class NotCompressFormatError(Exception):
    def __init__(self):
        self.msg = f"Not compress format!"
        super().__init__(self.msg)

class UnsupportedCompression(Exception):
    def __init__(self, supported_compression):
        self.warning = f"Unsupported compression. Use a supported compression: {supported_compression}"
        super().__init__(self.warning)
