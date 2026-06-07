#!/usr/bin/env -S python3


import sys
from typing import Callable, Optional

import base85ed

if __name__ == "__main__":
    op: Optional[Callable[[bytes], bytes]] = None

    match sys.argv[1:]:
        case ["-d"]:
            op = base85ed.decode
        case ["-e"]:
            op = base85ed.encode
        case _:
            print("Provide d or e command", file=sys.stderr)
            sys.exit(1)

    input_bytes: bytes = b""
    while (chunk := sys.stdin.buffer.read()) != b"":
        input_bytes += chunk

    output_bytes: bytes = op(input_bytes)

    sys.stdout.buffer.write(output_bytes)
    sys.stdout.flush()