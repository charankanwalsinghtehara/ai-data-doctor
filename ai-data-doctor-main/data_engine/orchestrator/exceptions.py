class PipelineError(Exception):
    """Base exception for pipeline errors."""
    pass


class PipelineStepError(PipelineError):
    """Raised when a pipeline step fails."""

    def __init__(
        self,
        step_name,
        original_error
    ):
        self.step_name = step_name
        self.original_error = original_error

        message = (
            f"Pipeline step "
            f"'{step_name}' failed: "
            f"{original_error}"
        )

        super().__init__(message)