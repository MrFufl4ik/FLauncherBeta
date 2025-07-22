async def convert_string_to_int(s: str) -> int:
    result: int = 0
    for ch in s: result += ord(ch)
    return result