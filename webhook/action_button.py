from typing import Optional, cast, Dict, Any

from sapiopylib.rest.WebhookService import AbstractWebhookHandler
from sapiopylib.rest.pojo.datatype.FieldDefinition import VeloxBooleanFieldDefinition, VeloxStringFieldDefinition
from sapiopylib.rest.pojo.webhook.ClientCallbackRequest import FormEntryDialogRequest
from sapiopylib.rest.pojo.webhook.ClientCallbackResult import FormEntryDialogResult
from sapiopylib.rest.pojo.webhook.WebhookContext import SapioWebhookContext
from sapiopylib.rest.pojo.webhook.WebhookResult import SapioWebhookResult
from sapiopylib.rest.utils.FormBuilder import FormBuilder


# This is a demo action button that will prompt a callback
class DemoActionButtonHandler(AbstractWebhookHandler):
    def run(self, context: SapioWebhookContext) -> SapioWebhookResult:
        if context.client_callback_result is not None:
            # This is Round 2, user has answered the feedback form. We are parsing the results...
            form_result: Optional[FormEntryDialogResult] = cast(Optional[FormEntryDialogResult],
                                                                context.client_callback_result)
            if not form_result.user_cancelled:
                response_map: Dict[str, Any] = form_result.user_response_map
                feeling: bool = response_map.get('Feeling')
                comments: str = response_map.get('Comments')
                msg: str
                if feeling:
                    # Light Side, do something...
                    context.data_record.set_field_value('C_HomeWorld', 'Tatooine')
                else:
                    # Dark Side, do something else...
                    context.data_record.set_field_value('C_HomeWorld', 'Naboo')


                context.data_record.set_field_value('C_SapioConComments', comments)

                # Push the field changes to Sapio
                context.data_record_manager.commit_data_records([context.data_record])

                return SapioWebhookResult(True, client_callback_request=None)
            else:
                print("User Cancelled.")
                # Display text sent over will be a toastr on the web client in Sapio.
                return SapioWebhookResult(True, display_text="You have Cancelled!")
        else:
            # This is Round 1, user hasn't done anything we are just telling Sapio Platform to display a form...
            form_builder: FormBuilder = FormBuilder()
            feeling_field = VeloxBooleanFieldDefinition(form_builder.get_data_type_name(), 'Feeling',
                                                        "Are you feeling well?", default_value=False)
            feeling_field.required = True
            feeling_field.editable = True
            form_builder.add_field(feeling_field)
            comments_field = VeloxStringFieldDefinition(form_builder.get_data_type_name(), 'Comments',
                                                        "Additional Comments", max_length=2000)
            comments_field.editable = True
            form_builder.add_field(comments_field)
            temp_dt = form_builder.get_temporary_data_type()
            request = FormEntryDialogRequest("Feedback", "Please provide us with some feedback!", temp_dt)
            return SapioWebhookResult(True, client_callback_request=request)
