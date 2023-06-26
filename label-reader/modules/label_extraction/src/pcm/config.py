class ProcessControllerConfig:
    def __init__(self, admin_internal_url: str) -> None:
        """
        Initialize the process controller.

        @param:
            admin_internal_url (str): Admin internal url
        """
        self.admin_internal_url = admin_internal_url
