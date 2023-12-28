import PyPDF2
import os
import requests

month_to_number = {
    'JAN': '01',
    'FEV': '02',
    'MAR': '03',
    'ABR': '04',
    'MAI': '05',
    'JUN': '06',
    'JUL': '07',
    'AGO': '08',
    'SET': '09',
    'OUT': '10',
    'NOV': '11',
    'DEZ': '12'
}

def extract_info_from_pdf(pdf_file_path):
    pdf_file = open(pdf_file_path, 'rb')
    read_pdf = PyPDF2.PdfReader(pdf_file)
    page = read_pdf.pages[0]
    page_content = page.extract_text()
    parsed = ''.join(page_content)
    lines = parsed.split('\n')
    return lines

def extract_info(lines):
    infos_conta_luz = {}
    for i in range(len(lines)):
        if 'Nº DO CLIENTE' in lines[i]:
            numero_cliente = lines[i+1].split()[0]
            infos_conta_luz['num_client'] = numero_cliente
        elif 'Referente a' in lines[i]:
            referente_a = lines[i+1].split()[0].split("/")
            month = month_to_number[referente_a[0].upper()]
            year = referente_a[1]
            infos_conta_luz['account_month'] = int(month)
            infos_conta_luz['account_year'] = int(year)
        elif 'Energia Elétrica kWh' in lines[i]:
            quantidade_energia_eletrica = lines[i].split()[3]
            quantidade_energia_eletrica = quantidade_energia_eletrica.replace(',', '.')
            valor_energia_eletrica = lines[i].split()[5]
            valor_energia_eletrica = valor_energia_eletrica.replace(',', '.')
            infos_conta_luz['amount_electricity'] = float(quantidade_energia_eletrica)
            infos_conta_luz['value_electricity'] = float(valor_energia_eletrica)
        elif 'Energia SCEE s/ ICMS kWh' in lines[i]:
            quantidade_energia_scee = lines[i].split()[5]
            quantidade_energia_scee = quantidade_energia_scee.replace(',', '.')
            valor_energia_scee = lines[i].split()[7]
            valor_energia_scee = valor_energia_scee.replace(',', '.')
            infos_conta_luz['amount_sceee'] = float(quantidade_energia_scee)
            infos_conta_luz['value_sceee'] = float(valor_energia_scee)
        elif 'Energia compensada GD I kWh' in lines[i]:
            quantidade_energia_compensada = lines[i].split()[5]
            quantidade_energia_compensada = quantidade_energia_compensada.replace(',', '.')
            valor_energia_compensada = lines[i].split()[7]
            valor_energia_compensada = valor_energia_compensada.replace(',', '.')
            infos_conta_luz['amount_compensated'] = float(quantidade_energia_compensada)
            infos_conta_luz['value_compensated'] = float(valor_energia_compensada)
        elif 'Contrib Ilum Publica Municipal' in lines[i]:
            valor_contribuicao_publica = lines[i].split()[4]
            valor_contribuicao_publica = valor_contribuicao_publica.replace(',', '.')
            infos_conta_luz['value_street'] = float(valor_contribuicao_publica)
    return infos_conta_luz

def process_pdfs_in_directory(directory):
    files = os.listdir(directory)

    pdf_files = [file for file in files if file.endswith('.pdf')]

    for pdf_file in pdf_files:
        lines = extract_info_from_pdf(directory + pdf_file)
        infos_conta_luz = extract_info(lines)
        infos_conta_luz['url_file'] = pdf_file

        url = "http://localhost:3000/invoices"
        response = requests.post(url, json=infos_conta_luz)

        if response.status_code == 201:
            print("POST bem-sucedido para o arquivo:", pdf_file)
        else:
            print("Falha no POST para o arquivo:", pdf_file)
        

directory = './'
process_pdfs_in_directory(directory)
