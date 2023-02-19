from typing import List, Dict, Optional, Any

from sapiopylib.rest.WebhookService import AbstractWebhookHandler
from sapiopylib.rest.pojo.DataRecord import DataRecord
from sapiopylib.rest.pojo.eln import ExperimentEntry
from sapiopylib.rest.pojo.webhook.WebhookContext import SapioWebhookContext
from sapiopylib.rest.pojo.webhook.WebhookResult import SapioWebhookResult
from sapiopylib.rest.utils.ProtocolUtils import ELNStepFactory
from sapiopylib.rest.utils.Protocols import ElnExperimentProtocol, ElnEntryStep
import csv


# This is a method that will mimic a method calls an external service with context
def get_mock_data(home_world: str):
    with open('webhook/characters.csv', 'r') as file:
        ret_row = []
        for row in csv.DictReader(file):
            if row["homeworld"] != home_world:
                continue
            ret_row.append(row)

        return ret_row


# Here is an example on how to use the protocol/step interfaces to easily create new steps in ELN.
class GetAvailableTechnicians(AbstractWebhookHandler):
    def run(self, context: SapioWebhookContext) -> SapioWebhookResult:
        home_world = None

        # Retrieve the home world from the data record given in the context
        if "C_HomeWorld" in context.data_record.fields:
            home_world = context.data_record.fields["C_HomeWorld"]

        # If there is no associated home world then default to Tatooine
        if not home_world:
            home_world = "Tatooine"
        else:
            home_world = str(home_world)

        # Ask our mock service for a list of available technicians in the world
        persons: List[Dict[str, Any]] = get_mock_data(home_world)

        returned_list: List[str] = []
        # Create a list of technician names
        for person in persons:
            returned_list.append(person["name"])

        print("Found {} technicians in {}".format(len(returned_list), home_world))

        return SapioWebhookResult(passed=True, list_values=returned_list)

