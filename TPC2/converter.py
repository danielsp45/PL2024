import re
from bs4 import BeautifulSoup as bs
from typing import List
import sys

TITLE_RE = r"^#{1,6}\s(.+)$"
BOLD_RE = r"(\*\*|__)(.*?)\1"
ITALIC_RE = r"(\*|_)(.*?)\1"
LINK_RE = r"(?<!!)\[(.*?)\]\((.*?)\)"
IMAGE_RE = r"!\[(.*?)\]\((.*?)\)"
LIST_RE = r"^\s*[-*]\s(.+)$"
ORD_LIST_RE = r"^\s*\d+\.\s(.+)$"


def markdown_to_html(markdown_file: str, html_file: str):
    # open and read the markdown file content
    with open(markdown_file, "r") as file:
        markdown = file.read()

    # read the markdown file line by line
    lines = markdown.split("\n")
    html = ""
    i = 0
    while i < len(lines):
        if (match := re.match(TITLE_RE, lines[i])):
            content = convert_title(match.group(1))
            html += content + "\n"

        elif (match := re.match(LIST_RE, lines[i])):
            # check if there's more lines in the list
            list_items = []
            list_items.append(match.group(1))

            i += 1
            while i < len(lines) and (match := re.match(LIST_RE, lines[i])):
                list_items.append(match.group(1))
                i += 1
            html += convert_list(list_items)

        elif (match := re.match(ORD_LIST_RE, lines[i])):
            # check if there's more lines in the list
            list_items = []
            list_items.append(match.group(1))

            i += 1
            while i < len(lines) and (match := re.match(ORD_LIST_RE, lines[i])):
                list_items.append(match.group(1))
                i += 1
            html += convert_ord_list(list_items)

        else:
            # in this case it's a paragraph
            if lines[i] != "":
                line = lines[i]
                line = function_pipeline(
                        line,
                        convert_bold,
                        convert_italic,
                        convert_image,
                        convert_link
                        )
                html += f"<p>{line}</p>\n"
        i += 1

    # write the html content to the file
    with open(html_file, "w") as file:
        html_content = bs(html, "html.parser").prettify()
        file.write(html_content)


# line level conversion
# the functions in the line conversion only receive the content of the line

def convert_title(title_content: str) -> str:
    title_content = function_pipeline(
            title_content,
            convert_bold,
            convert_italic,
            convert_image,
            convert_link
            )
    return f"<h1>{title_content}</h1>\n"

def convert_list(list_items: List[str]) -> str:
    list_html = "<ul>\n"
    for item in list_items:
        item = function_pipeline(
                item,
                convert_bold,
                convert_italic,
                convert_image,
                convert_link
                )

        list_html += f"<li>{item}</li>\n"
    list_html += "</ul>\n"
    return list_html

def convert_ord_list(list_items: List[str]) -> str:
    list_html = "<ol>\n"
    for item in list_items:
        item = function_pipeline(
                item,
                convert_bold,
                convert_italic,
                convert_image,
                convert_link
                )
        list_html += f"<li>{item}</li>\n"
    list_html += "</ol>\n"
    return list_html

# inline level conversion
# the functions in the inline conversion receive a raw line content and return the converted content

def convert_bold(content: str) -> str:
    bold_matches = re.finditer(BOLD_RE, content)
    converted_content = content

    # Iterate over each match and convert it to HTML
    for match in bold_matches:
        bold_text = match.group(2)

        bold_text = function_pipeline(
                bold_text, 
                convert_bold, 
                convert_italic, 
                convert_image, 
                convert_link
                )

        html_bold = f'<b>{bold_text}</b>'
        converted_content = converted_content.replace(match.group(0), html_bold)

    return converted_content
    

def convert_italic(content: str) -> str:
    italic_matches = re.finditer(ITALIC_RE, content)
    converted_content = content

    # Iterate over each match and convert it to HTML
    for match in italic_matches:
        italic_text = match.group(2)

        italic_text = function_pipeline(
                italic_text, 
                convert_bold, 
                convert_italic, 
                convert_image, 
                convert_link
                )

        html_italic = f'<i>{italic_text}</i>'
        converted_content = converted_content.replace(match.group(0), html_italic)

    return converted_content

def convert_link(content: str) -> str:
    link_matches = re.finditer(LINK_RE, content)
    converted_content = content

    # Iterate over each match and convert it to HTML
    for match in link_matches:
        link_text = match.group(1)
        link_url = match.group(2)

        link_text = function_pipeline(
                link_text, 
                convert_bold, 
                convert_italic, 
                convert_image, 
                convert_link
                )

        html_link = f'<a href="{link_url}">{link_text}</a>'
        converted_content = converted_content.replace(match.group(0), html_link)

    return converted_content

def convert_image(content: str) -> str:
    image_matches = re.finditer(IMAGE_RE, content)
    converted_content = content

    # Iterate over each match and convert it to HTML
    for match in image_matches:
        image_text = match.group(1)
        image_url = match.group(2)

        image_text = function_pipeline(
                image_text, 
                convert_bold, 
                convert_italic, 
                convert_image, 
                convert_link
                )

        html_link = f'<img href="{image_url}">{image_text}</img>'
        converted_content = converted_content.replace(match.group(0), html_link)

    return converted_content


# helpers
def function_pipeline(input, *funcs):
    for func in funcs:
        input = func(input)
    return input 


if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python converter.py <input.md> <output.html>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        # Call the markdown_to_html function with the provided input and output files
        markdown_to_html(input_file, output_file)
        print(f"Conversion successful. HTML output saved to {output_file}")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during conversion: {str(e)}")
        sys.exit(1)
