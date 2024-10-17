import requests
import pandas as pd
from config import Config


def ticket():
    # Declaración de variables y contadores
    i = 1
    df2 = pd.DataFrame()

    # La URL de la API para la solicitud del issue está definida
    url = f'{Config.base_url}/rest/api/2/search'
    # Define el parámetro de búsqueda para obtener todos los issues
    params = {
        'jql': 'project = CFE',
        'startAt': 0,
        'maxResults': 50
    }
    # Se realizan solicitudes GET sucesivas hasta obtener todos los issues
    all_issues = []
    start_at = 0
    max_results = 50

    while True:
        params['startAt'] = start_at
        params['maxResults'] = max_results

        response = requests.get(url, auth=(Config.username, Config.api_token), params=params)

        # Verifica el estado de la respuesta
        if response.status_code == 200:
            # La solicitud fue exitosa, se obtiene la información de los issues
            data = response.json()
            issues = data['issues']
            all_issues.extend(issues)

            start_at += max_results
            if start_at >= data['total']:
                break
        else:
            print(f'Error en la solicitud: {response.status_code}')
            break

    # Procesa la información de todos los issues
    for issue in all_issues:

        if issue['fields']['issuetype']['name'] == 'Mantenimiento Preventivo':

            issue_key = issue['key']
            issue_summary = issue['fields']['summary']
            issue_maintenance = issue['fields']['customfield_10077']['value']
            issue_type = issue['fields']['issuetype']['name']
            issue_status = issue['fields']['status']['name']
            issue_type_ticket = issue['fields']['customfield_10077']['value']
            issue_date = issue['fields']['customfield_10080']
            issue_invoice = issue['fields']['customfield_10079']
            if issue_invoice:
                registro = issue_invoice[0]
            CRDD = issue['fields']['customfield_10067'][0]['objectId']

            i += 1
            # Se crea el diccionario con el nombre de la columna y la variable
            registroc = {
                'Id': issue_key,
                'Resumen': issue_summary,
                'Tipo de mantenimiento preventivo': issue_maintenance,
                'Tipo de issue': issue_type,
                'Status': issue_status,
                'Tipo Ticket': issue_type_ticket,
                'Fecha de mantenimiento': issue_date,
                'Folio': registro,
                'CRDD': CRDD
            }

            df_temp = pd.DataFrame([registroc])
            df2 = pd.concat([df2, df_temp])

    df2 = df2.reset_index()  # Es un método para restablecer el índice de un marco de datos.
    df2.pop('index')  # Remover el index
    return df2