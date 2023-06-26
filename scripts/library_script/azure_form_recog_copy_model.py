# Python script to copy model from one Azure Form Recognizer resource to another
import sys
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentModelAdministrationClient
import click


def _get_form_recognizer_admin_client(
    form_recognizer_endpoint: str, form_recognizer_key: str
) -> DocumentModelAdministrationClient:
    """
    Creates a client for the Form Recognizer Admin API.

    :param form_recognizer_endpoint: The endpoint for the Form Recognizer Admin API.
    :param form_recognizer_key: The key for the Form Recognizer Admin API.
    :return: The client for the Form Recognizer Admin API.
    """
    return DocumentModelAdministrationClient(
        endpoint=form_recognizer_endpoint,
        credential=AzureKeyCredential(form_recognizer_key),
    )


def _validate_if_model_exist(
    admin_client: DocumentModelAdministrationClient, model_id: str
) -> bool:
    """
    Gets the list of models in the Form Recognizer resource.

    :param client: The client for the Form Recognizer Admin API.
    :param model_id: The model ID.
    :return: True if the model exists, False otherwise.
    """
    models = admin_client.list_document_models()
    return model_id in [model.model_id for model in models]


@click.command()
@click.option(
    "--source-endpoint",
    required=True,
    help="The endpoint for the source Form Recognizer resource.",
)
@click.option(
    "--source-key",
    required=True,
    help="The key for the source Form Recognizer resource.",
)
@click.option(
    "--dest-endpoint",
    required=True,
    help="The endpoint for the destination Form Recognizer resource.",
)
@click.option(
    "--dest-key",
    required=True,
    help="The key for the destination Form Recognizer resource.",
)
@click.option("--model-id", required=True, help="The model ID to copy.")
def main(
    source_endpoint: str,
    source_key: str,
    dest_endpoint: str,
    dest_key: str,
    model_id: str,
):
    """
    Copies a model from one Azure Form Recognizer resource to another.
    """
    print("copying model from source Azure Form Recognizer resource to destination...")
    source_client = _get_form_recognizer_admin_client(source_endpoint, source_key)
    dest_client = _get_form_recognizer_admin_client(dest_endpoint, dest_key)

    print("validating if model exists at source resource...")
    try:
        if not _validate_if_model_exist(source_client, model_id):
            print(f"model {model_id} does not exist in source resource")
            sys.exit(1)
    except Exception as e:
        print(f"error accessing Azure Form Recognizer source resource: {e}")
        print(
            "\nplease provide the correct Azure Form Recognizer source endpoint and key"
        )
        sys.exit(1)

    print("validating if model exists at destination resource...")
    try:
        if _validate_if_model_exist(dest_client, model_id):
            print(f"model {model_id} already exists in destination resource")
            sys.exit(0)
    except Exception as e:
        print(f"error accessing Azure Form Recognizer destination resource: {e}")
        print(
            "\nplease provide the correct Azure Form Recognizer destination endpoint and key"
        )
        sys.exit(1)

    print("starting to copy model...")
    try:
        dest_copy_auth = dest_client.get_copy_authorization(
            model_id=model_id,
            description="Pre Trained Model copied from source",
        )
        poller = source_client.begin_copy_document_model_to(
            model_id=model_id,
            target=dest_copy_auth,
        )
        print("waiting for model to be copied...")
        copied_over_model = poller.result()
    except Exception as e:
        print(f"error copying model: {e}")
        sys.exit(1)

    print(f"model {model_id} copied successfully")
    print("copied model details:")
    print("=======================================================================")
    print("Model ID: {}".format(copied_over_model.model_id))
    print("Description: {}".format(copied_over_model.description))
    print("Model created on: {}\n".format(copied_over_model.created_on))
    print("Doc types the model can recognize:")
    for name, doc_type in copied_over_model.doc_types.items():
        print("\nDoc Type: '{}' which has the following fields:".format(name))
        for field_name, field in doc_type.field_schema.items():
            print("Field: '{}' has type '{}".format(field_name, field["type"]))
    print("======================================================================")


if __name__ == "__main__":
    main()
