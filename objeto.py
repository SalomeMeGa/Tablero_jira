import requests
import json
import pandas as pd
from config import Config


def objeto():
    jira = (Config.username, Config.api_token)
    headers = {
        "Accept": "application/json"
    }
    pagina = 1
    count = 1
    df = pd.DataFrame()
    i = 1

    while count > 0:
        url = f'{Config.Url_parte_1}{pagina}{Config.Url_parte_2}'

        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=jira
        )

        r = json.loads(response.content)

        count = len(r['objectEntries'])

        for k in r['objectEntries']:

            if k['objectType']['id'] == '13':

                # print(i)

                CRDD = None
                NSerie = None
                Respaldo = None
                Stack = None
                Localidad = None
                Status = None
                Ip = None
                Poliza = None
                Contrato = None
                HostName = None
                Caracteristicas = None
                SO = None
                Firmware = None

                for l in k['attributes']:

                    if l['objectTypeAttributeId'] == '107':
                        CRDD = l['objectId']
                    if l['objectTypeAttributeId'] == '108':
                        NSerie = l['objectAttributeValues'][0]['displayValue']
                    if l['objectTypeAttributeId'] == '134':
                        Respaldo = l['objectAttributeValues'][0]['displayValue']
                    if l['objectTypeAttributeId'] == '135':
                        Stack = l['objectAttributeValues'][0]['referencedObject']['label']
                    if l['objectTypeAttributeId'] == '136':
                        Localidad = l['objectAttributeValues'][0]['referencedObject']['label']
                    if l['objectTypeAttributeId'] == '137':
                        Status = l['objectAttributeValues'][0]['status']['name']
                    if l['objectTypeAttributeId'] == '138':
                        Ip = l['objectAttributeValues'][0]['displayValue']
                    if l['objectTypeAttributeId'] == '142':
                        Poliza = l['objectAttributeValues'][0]['referencedObject']['label']
                    if l['objectTypeAttributeId'] == '143':
                        Contrato = l['objectAttributeValues'][0]['displayValue']
                    if l['objectTypeAttributeId'] == '146':
                        HostName = l['objectAttributeValues'][0]['displayValue']
                    if l['objectTypeAttributeId'] == '147':
                        Caracteristicas = l['objectAttributeValues'][0]['displayValue']
                    if l['objectTypeAttributeId'] == '150':
                        SO = l['objectAttributeValues'][0]['displayValue']
                    if l['objectTypeAttributeId'] == '151':
                        Firmware = l['objectAttributeValues'][0]['displayValue']

                registro = {
                    'CRDD': CRDD,
                    'No de serie': NSerie,
                    'Respaldo': Respaldo,
                    'Stack': Stack,
                    'Localidad': Localidad,
                    'Estatus': Status,
                    'Ip': Ip,
                    'Poliza': Poliza,
                    'Contrato': Contrato,
                    'Hostname': HostName,
                    'Caracteristicas': Caracteristicas,
                    'Sistema': SO,
                    'Firmware': Firmware
                }

                df_temp = pd.DataFrame([registro])
                df = pd.concat([df, df_temp])
                i += 1

        pagina += 1
    df = df.reset_index()  # It is a method to reset the index of a data frame.
    df.pop('index')  # remove the index
    return df