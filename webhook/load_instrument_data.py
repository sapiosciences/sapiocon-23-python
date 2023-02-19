from typing import List, Dict, Optional

from sapiopylib.rest.WebhookService import AbstractWebhookHandler
from sapiopylib.rest.pojo.DataRecord import DataRecord
from sapiopylib.rest.pojo.eln import ExperimentEntry
from sapiopylib.rest.pojo.webhook.WebhookContext import SapioWebhookContext
from sapiopylib.rest.pojo.webhook.WebhookResult import SapioWebhookResult
from sapiopylib.rest.utils.ProtocolUtils import ELNStepFactory
from sapiopylib.rest.utils.Protocols import ElnExperimentProtocol, ElnEntryStep
import csv


# This is a method that will mimic a method that retrieves information from an "instrument"
def get_csv_from_instrument(samples: List[DataRecord]):
    with open('webhook/qubit_example.csv', 'r') as file:
        # Create a copy of the input samples list as we will pop samples until no more remain
        samples = samples.copy()
        # The instrument data that will be generated in the following loop and returned
        inst_rows = []
        for row in csv.DictReader(file):
            # Create a fake instrument row for each sample given
            if not samples:
                break
            sample = samples.pop()
            # Replace the identifying Sample information in the row with data from our sample
            row["Sample ID"] = sample.fields["SampleId"]
            row["Sample Name"] = sample.fields["OtherSampleId"]
            inst_rows.append(row)

        return inst_rows


# Here is an example on how to use the protocol/step interfaces to easily create new steps in ELN.
class LoadInstrumentDataHandler(AbstractWebhookHandler):
    def run(self, context: SapioWebhookContext) -> SapioWebhookResult:

        my_entry: ExperimentEntry = context.experiment_entry

        print("Loading instrument data for {}, entry {} ".format(context.eln_experiment.notebook_experiment_name, my_entry.entry_name))

        # Retrieve the protocol representation of the experiment to use the sapiopylib protocol utils
        active_protocol: Optional[ElnExperimentProtocol] = context.active_protocol

        qc_datums: List[DataRecord] = list()

        # Create records for the instrument data to add to the experiment
        for instrument_row in get_csv_from_instrument(context.active_step.get_records()):
            # Translate the instrument data rows into a Dictionary of fields for the QC Datum
            fields: Dict = {
                "DatumType": "Qubit",
                "InstrumentName": "Qubert 3000",
                "SampleId": str(instrument_row["Sample ID"]),
                "OtherSampleId": str(instrument_row["Sample Name"]),
                "Concentration": float(instrument_row["Qubit Tube Conc."]),
                "ConcentrationUnits": str(instrument_row["Qubit tube conc. units"])
            }
            # Create a new QC Datum DataRecord with an empty RecordId value so that the server creates a new one
            qc_datum: DataRecord = DataRecord('QCDatum', None, fields)

            # Add the draft record to the list of records to be added to the table
            qc_datums.append(qc_datum)

        # Add a table underneath the Samples with the loaded in instrument data
        table_step: ElnEntryStep = ELNStepFactory.create_table_step(active_protocol, 'Sample Details', "QCDatum", qc_datums)

        # Chart the instrument data with a bar chart
        ELNStepFactory.create_bar_chart_step(active_protocol, table_step, "Qubit Data", "SampleId", "Concentration")

        return SapioWebhookResult(True)

