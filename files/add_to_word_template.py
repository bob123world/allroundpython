from docxtpl import DocxTemplate

context = {}
context["company"] = "PAELLA NV"
employees = []
employee = {}
employee["firstname"] = "BoB"
employee["lastname"] = "Buffet" 
employee["age"] = 26
employees.append(employee)
employee = {}
employee["firstname"] = "B"
employee["lastname"] = "IT Obliterator" 
employee["age"] = 25
employees.append(employee) 
context["row_contents"] = employees

doc = DocxTemplate("C:/Users/MDEBOE.EUROPE/Documents/GIT/allroundpython/files/test_word.docx")
doc.render(context)
doc.save("generated_doc.docx")
