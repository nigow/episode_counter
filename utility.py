from typing import List


def divide_by_delimiter(content: str) -> List[str]:
    # a random episode should not contain "・" prefix
    if content.find("・") == -1:
        return []

    if content[0] == "・":
        content = content[1:]
    parsed_message = content.split('\n・')

    # make sure there are no empty strings
    parsed_message = list(filter(None, parsed_message))
    return parsed_message


def emoji_to_text(content: str) -> str:
    # replace emoji with text
    print(content)
