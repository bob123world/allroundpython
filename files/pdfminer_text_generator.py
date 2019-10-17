import io
import os
import json
import xml.etree.ElementTree as xml
from xml.dom import minidom
 
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
 
def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            laparams = LAParams()
            converter = TextConverter(resource_manager, fake_file_handle, laparams=laparams)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
 
            text = fake_file_handle.getvalue()
            yield text
 
            # close open handles
            converter.close()
            fake_file_handle.close()
 
def extract_text(pdf_path):
    for page in extract_text_by_page(pdf_path):
        print(page)
        print()

def export_as_txt(pdf_path, txt_path):
    file = open(txt_path, "w")
    for page in extract_text_by_page(pdf_path):
        file.write(page)

    file.close()

def export_as_json(pdf_path, json_path):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    data = {'Filename': filename}
    data['Pages'] = []
 
    counter = 1
    for page in extract_text_by_page(pdf_path):
        page.replace(",","\n")
        page = {'Page_{}'.format(counter): page}
        data['Pages'].append(page)
        counter += 1
 
    with open(json_path, 'w') as fh:
        json.dump(data, fh)

def export_as_xml(pdf_path, xml_path):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    root = xml.Element('{filename}'.format(filename=filename))
    pages = xml.Element('Pages')
    root.append(pages)
 
    counter = 1
    for page in extract_text_by_page(pdf_path):
        text = xml.SubElement(pages, 'Page_{}'.format(counter))
        text.text = page
        counter += 1
 
    tree = xml.ElementTree(root)
    xml_string = xml.tostring(root, 'utf-8')
    parsed_string = minidom.parseString(xml_string)
    pretty_string = parsed_string.toprettyxml(indent='  ')
 
    with open(xml_path, 'w') as fh:
        fh.write(pretty_string)
    #tree.write(xml_path)
 
if __name__ == '__main__':
    config = {}
    config["pdf_path"] = "C:/Users/MDEBOE.EUROPE/Documents/GIT/allroundpython/files/SeptMC.pdf"
    config["txt_path"] = "C:/Users/MDEBOE.EUROPE/Documents/GIT/allroundpython/files/example1.txt"
    config["json_path"] = "C:/Users/MDEBOE.EUROPE/Documents/GIT/allroundpython/files/example1.json"
    config["xml_path"] = "C:/Users/MDEBOE.EUROPE/Documents/GIT/allroundpython/files/example1.xml"
    #print(extract_text(config["pdf_path"]))
    #export_as_txt(config["pdf_path"], config["txt_path"])
    export_as_json(config["pdf_path"], config["json_path"])
    #export_as_xml(config["pdf_path"], config["xml_path"])