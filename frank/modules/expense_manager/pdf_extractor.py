import io
import os
import json
from datetime import datetime, date

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams

def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
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

def mastercard_bill_to_expense_note_json(pdf_path):
    output = {}
    output["name"] = "expense_note"
    today = date.today()
    output["date"] = today.strftime("%d/%m/%Y")
    expenses = []
    date_array = []
    data_array = []
    money_array = []

    for count, page in enumerate(extract_text_by_page(pdf_path)):
        page = page.replace("\n\n","\n")
        segments = page.split("\n")
        if count == 0:
            start = False
            section = 1
            for segment in segments:
                if section is 1:
                    if "Vorig saldo op" in segment:
                         start = True
                    elif start:
                        if "Kaartnummer" not in segment:
                            date_array.append(segment)
                        else:
                            start = False
                            section = 2
                elif section is 2:
                    if segment in "MICHAEL DEBOEURE":
                        start = True
                    elif start:
                        if "bedrag in EUR" not in segment:
                            data_array.append(segment)
                        else:
                            section = 3
                elif section is 3:
                    if start:
                        if "Kaart blokkeren:" not in segment:
                            money_array.append(segment)
                        else:
                            start = False
        else:
            start = False
            section = 1
            for segment in segments:
                if section is 1:
                    if "verrekening" in segment:
                         start = True
                    elif start:
                        if "-" in list(segment)[2]:
                            date_array.append(segment)
                        else:
                            section = 2
                            data_array.append(segment)
                elif section is 2:
                    if start:
                        if "Totaal bedrag van" not in segment:
                            data_array.append(segment)
                        else:
                            start = False
                            section = 3
                elif section is 3:
                    if "bedrag in EUR" in segment:
                         start = True
                    elif start:
                        if "Kaart blokkeren:" not in segment:
                            money_array.append(segment)
                        else:
                            start = False

    # Delete the first two element of the money array because they are for previous month
    money_array = money_array[2:]
    # The last element is the total amount to be paid
    total = money_array[-1]
    # Delete every secondth element out of the date list
    date_array = date_array[0::2]

    termination_list = ["BE", "BEL", "GBR"]
    exclusion_list = ["KONTICH", "BURCHT"]
    name_list = []
    start = True
    name = ""
    for data in data_array():
        if start:
            name = data
            if check_for_end(name, termination_list):
                pass


    money = None

def check_for_end(data, termination_list):
    for term in termination_list:
        l = len(term)
        if data[:-l] in term:
            return True
    return False
            

if __name__ == '__main__':
    config = {}
    config["pdf_path"] = "C:/Users/MDEBOE.EUROPE/Documents/GIT/allroundpython/files/SeptMC.pdf"
    config["json_path"] = "C:/Users/MDEBOE.EUROPE/Documents/GIT/allroundpython/files/example1.json"
    mastercard_bill_to_expense_note_json(config["pdf_path"])