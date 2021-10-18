from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import logging

ERRORS = 'errors'
ERROR = 'error'


def run_action(project_id, rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    zone = entity.get('zone')
    instance = entity.get('name')
    logging.info(f'{__file__} - project_id : {project_id} - zone : {zone} instance : {instance}')

    output_msg = ''

    try:
        logging.info(f'{__file__} - stopping virtual machine: {instance}')
        request = service.instances().stop(project=project_id, zone=zone, instance=instance)
        response = request.execute()
        if ERROR in response:  # on failure
            msg = f'Failed stopping virtual machine - {instance}: {response[ERROR]}'
            logging.error(f'{__file__} - {msg}')
            output_msg += msg
        else:  # on success
            msg = f'Virtual machine - {instance} was stopped'
            logging.info(f'{__file__} - {msg}')
            output_msg += msg
    except Exception as e:
        msg = f'Unexpected error occurred - {e}'
        logging.error(f'{__file__} - {msg}')
        output_msg += msg
    return output_msg
