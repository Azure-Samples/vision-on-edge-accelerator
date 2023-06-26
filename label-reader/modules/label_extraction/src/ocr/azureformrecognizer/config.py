class AzureFormRecognizerConfig:

    """Contains all the configurations specific to Azure Cognitive Services -
    Form Recognizer Service.
    """

    # The singleton instance of the current class
    __instance = None

    def __init__(
        self,
        cogs_formrecog_key: str,
        cogs_formrecog_endpoint: str,
        cogs_formrecog_model_id: str,
    ) -> None:
        """Initializes the configuration for the Form Recognizer calls

        Args:
            cogs_formrecog_key (str): azure cognitive services - form recognizer endpoint api key
            cogs_formrecog_endpoint (str): endpoint URL of the Form Recognizer Service
            cogs_formrecog_model_id (str): id of the Form Recognizer custom model
        """
        self.l_cogs_formrecog_key = cogs_formrecog_key
        self.l_cogs_formrecog_endpoint = cogs_formrecog_endpoint
        self.l_cogs_formrecog_model_id = cogs_formrecog_model_id
