import argparse 
import os
from bs4 import BeautifulSoup
from ebooklib import epub
import re
import subprocess

def extract_annotations(html_path):
    """Extract highlights and notes from the HTML file."""
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
    
    annotations = []
    
    # Find all highlight and note pairs
    highlights = soup.find_all('div', class_='noteHeading')
    for highlight in highlights:
        note_text = highlight.find_next_sibling('div', class_='noteText')
        if note_text:
            annotations.append({
                'text': note_text.get_text().strip(),
                'type': 'highlight' if 'Highlight' in highlight.get_text() else 'note'
            })
    
    return annotations

def apply_annotations_to_epub(epub_path, annotations, output_path):
    """Apply annotations to the epub file and save to output path."""
    # Read the epub
    book = epub.read_epub(epub_path)
    
    # Create a new section for annotations
    annotations_html = '<h1>Annotations</h1>\n'
    for ann in annotations:
        annotations_html += f'<div class="annotation {ann["type"]}">\n'
        annotations_html += f'<p>{ann["text"]}</p>\n'
        annotations_html += '</div>\n'
    
    # Create a new chapter for annotations
    annotations_chapter = epub.EpubHtml(
        title='Annotations',
        file_name='annotations.xhtml',
        content=annotations_html
    )
    
    # Add the annotations chapter to the book
    book.add_item(annotations_chapter)
    
    # Add to table of contents
    book.toc.append(annotations_chapter)
    
    # Update spine
    book.spine.append(annotations_chapter)
    
    # Write the epub
    epub.write_epub(output_path, book)
    
def convert_to_pdf(epub_path, pdf_path):
    """Convert epub to PDF using Calibre's ebook-convert."""
    try:
        subprocess.run(['ebook-convert', epub_path, pdf_path], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Error: Failed to convert epub to PDF. Make sure Calibre is installed.")
        return False
    except FileNotFoundError:
        print("Error: ebook-convert not found. Please install Calibre first.")
        return False

def main():
    parser = argparse.ArgumentParser(description='Process epub file and annotations.')
    parser.add_argument('--epub', required=True, help='Path to the epub file')
    parser.add_argument('--annotations', required=True, help='Path to the annotations HTML file')
    parser.add_argument('--pdf', action='store_true', help='Convert to PDF')
    
    args = parser.parse_args()
    
    # TODO: Add processing logic here
    print(f"Processing epub file: {args.epub}")
    print(f"Processing annotations file: {args.annotations}")
    
     # Generate output path
    output_path = os.path.join('temp', 'annotated_' + os.path.basename(args.epub))
    
    # Process annotations
    print(f"Extracting annotations from: {args.annotations}")
    annotations = extract_annotations(args.annotations)
    
    # Apply annotations to epub
    print(f"Applying annotations to epub: {args.epub}")
    apply_annotations_to_epub(args.epub, annotations, output_path)
    
    print(f"Annotated epub saved to: {output_path}")
    
        # Convert to PDF if requested
    if args.pdf:
        pdf_output_path = os.path.splitext(output_path)[0] + '.pdf'
        print(f"Converting to PDF...")
        if convert_to_pdf(output_path, pdf_output_path):
            print(f"PDF saved to: {pdf_output_path}")


if __name__ == "__main__":
    main() 