from typing import List, Dict, Optional, Any

from sapiopylib.rest.WebhookService import AbstractWebhookHandler
from sapiopylib.rest.pojo.DataRecord import DataRecord
from sapiopylib.rest.pojo.eln import ExperimentEntry
from sapiopylib.rest.pojo.webhook.WebhookContext import SapioWebhookContext
from sapiopylib.rest.pojo.webhook.WebhookResult import SapioWebhookResult
from sapiopylib.rest.utils.ProtocolUtils import ELNStepFactory
from sapiopylib.rest.utils.Protocols import ElnExperimentProtocol, ElnEntryStep
import csv


# This is a method that will mimic a method calls an external service or list
def get_mock_data():
    with open('webhook/characters.csv', 'r') as file:
        ret_row = []
        for row in csv.DictReader(file):
            ret_row.append(row)

        return ret_row


# Here is an example that will return a simple list of home worlds to choose from
class GetHomeWorldList(AbstractWebhookHandler):
    def run(self, context: SapioWebhookContext) -> SapioWebhookResult:
        # Ask our mock service for a list of available technicians
        persons: List[Dict[str, Any]] = get_mock_data()

        # Create a list of the home worlds the customer can use
        returned_list: List[str] = []
        for person in persons:
            homeworld: str = person["homeworld"]
            returned_list.append(homeworld)

        print("Found {} home worlds".format(len(returned_list)))

        return SapioWebhookResult(passed=True, list_values=returned_list)

