from typing import Dict

from sapiopylib.rest.DataMgmtService import DataMgmtServer
from sapiopylib.rest.WebhookService import AbstractWebhookHandler
from sapiopylib.rest.pojo.DataRecord import DataRecord
from sapiopylib.rest.pojo.webhook.WebhookContext import SapioWebhookContext
from sapiopylib.rest.pojo.webhook.WebhookDirective import FormDirective, CustomReportDirective
from sapiopylib.rest.pojo.webhook.WebhookResult import SapioWebhookResult
from sapiopylib.rest.utils.recordmodel.PyRecordModel import PyRecordModel
from sapiopylib.rest.utils.recordmodel.RecordModelManager import RecordModelManager, RecordModelInstanceManager, \
    RecordModelRelationshipManager
from sapiopylib.rest.utils.recordmodel.RelationshipPath import RelationshipPath


class RecordModelExampleHandler(AbstractWebhookHandler):
    def run(self, context: SapioWebhookContext) -> SapioWebhookResult:
        root_record: DataRecord = context.data_record_manager.query_system_for_record("Directory", 1)

        rec_man: RecordModelManager = RecordModelManager(context.user)
        inst_man: RecordModelInstanceManager = rec_man.instance_manager
        relationship_man: RecordModelRelationshipManager = rec_man.relationship_manager

        root_record_model: PyRecordModel = inst_man.add_existing_record(root_record)

        # In order to navigate the hierarchy with RecordModel you must load those parents/children first
        relationship_man.load_children([root_record_model], "Project")

        # Bring in any studies that are related to the projects through requests
        relationship_man.load_path([root_record_model], RelationshipPath().child("Project").child("Request").parent("Study"))

        # In our example we will do some simple counting of the data we have
        created_by_ranking: Dict[str, int] = {}
        total_study_links: int = 0

        # Iterate through the now locally stored records
        for project in root_record_model.get_children_of_type("Project"):
            for request in project.get_children_of_type("Request"):
                created_by: str = request.fields["CreatedBy"]
                # Increment the ranking in our scoring sheet
                if created_by in created_by_ranking:
                    created_by_ranking[created_by] += 1
                else:
                    created_by_ranking[created_by] = 1
                total_study_links += len(request.get_parents_of_type("Study"))

        # Add now RecordModel, this isn't created in sapio until rec_man.store_and_commit() is called
        sapio_con: PyRecordModel = inst_man.add_new_record("C_SapioConTest")

        # Set a field on the new record to be set with it
        sapio_con.fields["Description"] = f"Found {total_study_links} studies linked to projects in the directory. " \
                                                 f"\n Request Ranking: {created_by_ranking}"

        sapio_con.fields["Name"] = "Python!"

        # Push all the changes to sapio in one call
        rec_man.store_and_commit()

        custom_report_man = DataMgmtServer.get_custom_report_manager(context.user)

        # Retrieve a report to show all the sapio con test records
        all_tests_report = custom_report_man.run_system_report_by_name("All Sapio Con Tests")

        return SapioWebhookResult(True, directive=CustomReportDirective(all_tests_report))
