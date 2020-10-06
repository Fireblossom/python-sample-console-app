from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
from pathlib import Path
import re
PATTERN = re.compile('.{4}')


def fill_tk(data, im):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    offset = 841.9
    can = canvas.Canvas(packet, pagesize=A4)
    # BeginTime
    if data['BeginTime'] == '2020年10月1日':
        can.drawString(180, offset - 90, "0  1    1   0   2   0   2   0")
    else:
        can.drawString(180, offset - 90, "0  1    0   4   2   0   2   1")
    # Gender
    if data['Gender'] == '女':
        can.drawString(79, offset - 138, "X")  # Frau
    else:
        can.drawString(129, offset - 138, "X")  # Herr
    # Lastname
    can.drawString(79, offset - 152, data["LastName"])
    # Firstname
    can.drawString(79, offset - 176, data["FirstName"])
    # Address
    can.drawString(79, offset - 199, data["Address"])
    # ExtraAddress
    can.drawString(79, offset - 221, data["ExtraAddress"])
    # PLZ
    can.drawString(79, offset - 244, data["PLZ"] + ", " + data["City"])
    # Birthday
    birthday = data["Birthday"].replace('-', '')
    can.drawString(79, offset - 277, "  " + "   ".join(birthday))
    # Birthplace
    can.drawString(79, offset - 385, data["Birthplace"])
    # BirthName
    can.drawString(79, offset - 407, data["BirthName"])
    # Nation
    can.drawString(79, offset - 432, "Chinesisch")
    can.drawString(92, offset - 498, "Zuzug aus China")
    # Begin
    can.drawString(465, offset - 231, data["StudyTime"])
    can.drawString(465, offset - 249, data["Term"])
    # Major
    can.drawString(322, offset - 267, data["Major"])
    # University
    can.drawString(322, offset - 291, data["University"])
    # Master
    if data['Master'] == '硕士':
        can.drawString(321, offset - 318, "X")
        can.drawString(530, offset - 333, "4")
    # Email
    can.drawString(322, offset - 516, data["Phone"])
    can.drawString(322, offset - 541, data["Email"])

    # Advisor
    can.drawString(396, offset - 743, "DECH Makler GmbH/Wenbo")
    can.drawString(396, offset - 756, "Sundgauerstr. 105d, 14169")
    can.drawString(396, offset - 769, "030 81059725")
    can.drawString(396, offset - 782, "T7604483F2")

    # Sign
    # im = Image.open('Sign.png')
    x, y = im.size
    try:
        p = Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0, x, y), im)
    except:
        pass
    can.drawInlineImage(p, 337, offset - 570, width=190, height=20)
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("tk.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    Path('info/' + data["Email"]).mkdir(parents=True, exist_ok=True)
    output_stream = open('info/' + data["Email"] + "/tk_filled.pdf", "wb")
    output.write(output_stream)
    output_stream.close()
    print("pdf generated!")


def fill_tk_sepa(data, im):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    offset = 841.9
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont('Courier', 9.3)
    # IBAN
    can.drawString(80, offset - 484, '  '.join(data['IBAN']))
    # BIC
    can.drawString(80, offset - 532, '  '.join(data['BIC']))
    # BeginTime
    if data['BeginTime'] == '2020年10月1日':
        can.drawString(130, offset - 561, '  '.join('102020'))
    # BankName
    can.drawString(245, offset - 561, '  '.join(data['BankName']))
    # holder
    if data['holder']:
        can.drawString(195, offset - 587, "X")  # Yes
    else:
        can.drawString(228, offset - 587, "X")  # No
    # Name
    can.drawString(80, offset - 617, '  '.join(data['Name']))
    # Address
    can.drawString(80, offset - 650, '  '.join(data['Address']))
    # PLZ
    can.drawString(80, offset - 683, '  '.join(data['PLZ']))
    # City
    can.drawString(180, offset - 683, '  '.join(data['City']))
    # SignCity
    can.drawString(80, offset - 733, data['SignCity'])
    # SignTime
    can.drawString(213, offset - 733, '  '.join(data['SignTime'][:10].replace('-', '')))
    # Sign
    # im = Image.open('Sign.png')
    x, y = im.size
    try:
        p = Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0, x, y), im)
    except:
        pass
    can.drawInlineImage(p, 365, offset - 731, width=190, height=20)
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("TK_SEPA.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    Path('info/' + data["Email"]).mkdir(parents=True, exist_ok=True)
    output_stream = open('info/' + data["Email"] + "/tk_SEPA_filled.pdf", "wb")
    output.write(output_stream)
    output_stream.close()
    print("pdf generated!")


def fill_dak(data):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    offset = 841.9
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont('Courier', 9.3)
    can.drawString(384, offset - 158, 'X')
    # Gender
    if data['Gender'] == '男':
        can.drawString(283, offset - 200, 'Männlich')
    else:
        can.drawString(283, offset - 200, 'Weiblich')
    # Name
    can.drawString(283, offset - 219, data['Name'])
    # Birthday
    can.drawString(283, offset - 237, data['Birthday'])
    # c/o
    can.drawString(283, offset - 256, data['c/o'])
    # Address
    can.drawString(283, offset - 272, data['Address'])
    # PLZ
    can.drawString(283, offset - 293, data['PLZ'])
    # City
    can.drawString(283, offset - 312, data['City'])
    # Phone
    can.drawString(283, offset - 331, data['Phone'])
    # Email
    can.drawString(283, offset - 349, data['Email'])
    # BirthName
    can.drawString(283, offset - 368, data['BirthName'])
    # Birthplace
    can.drawString(283, offset - 386, data['Birthplace'])
    # Nation
    can.drawString(283, offset - 404, 'Chinesisch')
    # Master
    can.drawString(283, offset - 424, data['Master'])
    # University
    can.drawString(283, offset - 442, data['University'])
    # StudyTime
    can.drawString(283, offset - 460, data['StudyTime'])
    # Major
    can.drawString(283, offset - 480, data['Major'])
    # FromTerm
    can.drawString(283, offset - 510, data['FromTerm'])
    # MoveIn
    can.drawString(283, offset - 546, data['MoveIn'])
    # PrivateName
    can.drawString(283, offset - 589, data['PrivateName'])
    # PrivateBegin
    can.drawString(283, offset - 606, data['PrivateBegin'])
    # PrivateEnd
    can.drawString(283, offset - 626, data['PrivateEnd'])
    # Others
    can.drawString(283, offset - 646, data['OldIns'])
    can.drawString(283, offset - 679, data['Marry'])
    can.drawString(283, offset - 715, data['Children'])
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("DAK.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    Path('info/' + data["Email"]).mkdir(parents=True, exist_ok=True)
    output_stream = open('info/' + data["Email"] + "/dak_filled.pdf", "wb")
    output.write(output_stream)
    output_stream.close()
    print("pdf generated!")


def fill_dak_sepa(data, im):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    offset = 841.9
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont('Courier', 9.3)
    # Name
    can.drawString(72, offset - 297, data['Name'])
    can.drawString(79, offset - 620, data['Name'])
    # Address
    address = data['Address'] + ', ' + data['PLZ'] + ', ' + data['City']
    can.drawString(72, offset - 327, address)
    can.drawString(79, offset - 648, address)
    # BeginTime
    if data['BeginTime'] == '2020年10月1日':
        can.drawString(79, offset - 592, '10.2020')
    # BIC
    can.drawString(79, offset - 710, data['BIC'])
    # BankName
    can.drawString(79, offset - 737, data['BankName'])
    # City and Time
    can.drawString(79, offset - 767, data['SignCity']+', '+data['SignTime'][:10].replace('-', '.'))
    # IBAN
    can.setFont('Courier', 11.5)
    iban = ' '.join(PATTERN.findall(data['IBAN']))[2:]
    can.drawString(98, offset - 677, iban)
    # Sign
    # im = Image.open('Sign.png')
    x, y = im.size
    try:
        p = Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0, x, y), im)
    except:
        pass
    can.drawInlineImage(p, 80, offset - 796, width=190, height=14)
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("DAK_SEPA.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    Path('info/' + data["Email"]).mkdir(parents=True, exist_ok=True)
    output_stream = open('info/' + data["Email"] + "/dak_SEPA_filled.pdf", "wb")
    output.write(output_stream)
    output_stream.close()
    print("pdf generated!")


if __name__ == '__main__':
    im = Image.open('Sign.png')
    data = {'PLZ': '12345', 'SignTime': '27-09-2020 05:31:04', 'Email': 't@t.ty', 'Address': 't',
            'FirstName': 't', 'Birthplace': 't', 'VisaDate': '', 'BeginTime': '2020年10月1日', 'Visa': 'false',
            'Birthday': '01-09-2020', 'Gender': '男', 'City': 't', 'Term': '1', 'Master': '硕士', 'StudyTime': '10.2020',
            'ChineseName': 't', 'Passport': '', 'Major': 't', 'University': 't', 'Phone': '12345', 'LastName': 't',
            'ExtraAddress': '1234', 'BirthName': '123'}
    fill_tk(data, im)
    data = {'Email': 't@t.ty', 'Name': 'Zhang, San', 'Gender': '男', 'Birthday': '01-09-2020', 'c/o': 'Li, Si',
            'Address': '1345678 456', 'PLZ': '12345', 'Master': 'Master', 'FromTerm': '1', 'City': 'Beijing',
            'University': 'tub', 'Phone': '12345', 'Major': 't', 'StudyTime': '10.2020', 'BirthName': '',
            'OldIns': 'Nein', 'Marry': 'Nein', 'Children': 'Nein', 'Birthplace': 't', 'MoveIn': '27-09-2020',
            'PrivateName': 'Dr.Walter', 'PrivateBegin': '01-01-2020', 'PrivateEnd': '01-01-2020'}
    fill_dak(data)
    data = {'Email': 't@t.ty', 'IBAN': 'DE00000000000000000000', 'BIC': 'DEUTDBSTG', 'BankName': 'DEUTSCHE BANK',
            'BeginTime': '2020年10月1日', 'holder': False, 'Name': 'a,b', 'Address': '1345678', 'PLZ': '12345',
            'City': 'Beijing', 'SignCity': 'Shanghai', 'SignTime': '27-09-2020 05:31:04'}
    fill_tk_sepa(data, im)
    data = {'Email': 't@t.ty', 'IBAN': 'DE00000000000000000000', 'BIC': 'DEUTDBSTG', 'BankName': 'DEUTSCHE BANK',
            'BeginTime': '2020年10月1日', 'Name': 'a,b', 'Address': '1345678', 'PLZ': '12345',
            'City': 'Beijing', 'SignCity': 'Shanghai', 'SignTime': '27-09-2020 05:31:04'}
    fill_dak_sepa(data, im)
