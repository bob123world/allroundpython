import os

from PyPDF2 import PdfFileReader, PdfFileWriter

def main():
    file1 = ""
    split1 = [[0,1,2,3], [4]]
    split(file1, "contract", split1)

    file2 = "contract4.pdf"
    file3 = "contract3.pdf"
    files = [file2, file3]
    merge_pdfs(files, "")

def merge_pdfs(paths: list, output: str):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

def split(path: str, name_of_split: str, divider: list):
    pdf = PdfFileReader(path)
    for div in divider:
        pdf_writer = PdfFileWriter()
        for i, page in enumerate(range(pdf.getNumPages())):
            if i in div:
                pdf_writer.addPage(pdf.getPage(page))

        output = f'{name_of_split}{str(div[-1])}.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

if __name__ == '__main__':
    main()