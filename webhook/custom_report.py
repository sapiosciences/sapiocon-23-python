from sapiopylib.rest.WebhookService import AbstractWebhookHandler
from sapiopylib.rest.pojo.CustomReport import CustomReport, RawReportTerm, CompositeReportTerm, RawTermOperation, \
    CompositeTermOperation, CustomReportCriteria, ReportColumn
from sapiopylib.rest.pojo.datatype.FieldDefinition import FieldType
from sapiopylib.rest.pojo.webhook.WebhookContext import SapioWebhookContext
from sapiopylib.rest.pojo.webhook.WebhookDirective import CustomReportDirective
from sapiopylib.rest.pojo.webhook.WebhookResult import SapioWebhookResult


# Here is an example on how to use the protocol/step interfaces to easily create new steps in ELN.
class CustomReportExampleHandler(AbstractWebhookHandler):
    def run(self, context: SapioWebhookContext) -> SapioWebhookResult:
        # Our terms. We can use programmatic logic to control what should be included in this report based on the context.
        # In this example we are filtering based on the user
        if context.user.username == "bmayer":
            term1 = RawReportTerm('Project', 'ProjectId', RawTermOperation.EQUAL_TO_OPERATOR, 'Clinical Demo')
        else:
            term1 = RawReportTerm('Project', 'ProjectId', RawTermOperation.EQUAL_TO_OPERATOR, 'DEMOPROJ')

        # Only show the most recent 90 samples
        term2 = RawReportTerm('Sample', 'DateCreated', RawTermOperation.EQUAL_TO_OPERATOR, '@last90days')
        root_term = CompositeReportTerm(term1, CompositeTermOperation.AND_OPERATOR, term2)

        # The columns we want to include in shown report
        column_list = [ReportColumn('Project', 'ProjectName', FieldType.STRING),
                       ReportColumn('Sample', 'SampleId', FieldType.STRING)]
        request = CustomReportCriteria(column_list, root_term, page_size=1, page_number=0)

        # Create a temporary report that the client will run
        report: CustomReport = CustomReport(criteria=request, has_next_page=False, result_table=None)

        # Direct the client to our report
        return SapioWebhookResult(passed=True, directive=CustomReportDirective(report))
