# What it does: Enables subnet 'private google access'
# Usage: subnet_set_private_google_access_on
# Example: subnet_set_private_google_access_on
# Limitations: None
# Sample GSL: Subnet should have privateIpGoogleAccess=true
# Associated Rule: D9.GCP.NET.14
# Permissions: compute.subnetworks.setPrivateIpGoogleAccess

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import logging
import bots_utils


def run_action(project_id, rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)

    subnet_name, region = get_properties_from_entity(entity)
    output_msg = ''

    logging.info(f'{__file__} - Setting private google access on subnet: {subnet_name} to on')

    try:
        set_google_private_access_on(service, project_id, subnet_name, region)
    except Exception as e:  # on failure
        msg = f'Failed to set private google access on: {e}'
        logging.error(f'{__file__} - {msg}')
        raise Exception(msg)
    msg = f'Successfully set private google access on'
    logging.info(f'{__file__} - {msg}')
    output_msg += msg

    return output_msg


def set_google_private_access_on(service, project_id, subnet_name, region):
    subnetworks_set_private_ip_google_access_request_body = {
        "privateIpGoogleAccess": True
    }
    request = service.subnetworks().setPrivateIpGoogleAccess(project=project_id, region=region, subnetwork=subnet_name,
                                                             body=subnetworks_set_private_ip_google_access_request_body)
    request.execute()


def get_properties_from_entity(entity):
    try:
        subnet_name = entity['name']
        region = entity['region']
    except KeyError as e:
        raise KeyError(f"Missing property from entity: {e}")
    return subnet_name, region
