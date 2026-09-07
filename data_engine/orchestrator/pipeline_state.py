from datetime import datetime


class PipelineState:

    def __init__(self):

        self.started_at = (
            datetime.now()
            .isoformat()
        )

        self.completed_at = None

        self.status = "running"

        self.current_step = None

        self.steps = {}

        self.errors = []


    def start_step(
        self,
        step_name
    ):

        self.current_step = step_name

        self.steps[
            step_name
        ] = {

            "status": "running",

            "started_at":
                datetime.now()
                .isoformat(),

            "completed_at": None,

            "error": None
        }


    def complete_step(
        self,
        step_name
    ):

        if step_name in self.steps:

            self.steps[
                step_name
            ][
                "status"
            ] = "completed"

            self.steps[
                step_name
            ][
                "completed_at"
            ] = (

                datetime.now()
                .isoformat()
            )


    def fail_step(
        self,
        step_name,
        error
    ):

        error_message = str(error)

        if step_name in self.steps:

            self.steps[
                step_name
            ][
                "status"
            ] = "failed"

            self.steps[
                step_name
            ][
                "completed_at"
            ] = (

                datetime.now()
                .isoformat()
            )

            self.steps[
                step_name
            ][
                "error"
            ] = error_message

        self.errors.append({

            "step": step_name,

            "error": error_message,

            "timestamp":
                datetime.now()
                .isoformat()
        })


    def complete_pipeline(
        self
    ):

        self.status = "completed"

        self.completed_at = (

            datetime.now()
            .isoformat()
        )


    def fail_pipeline(
        self
    ):

        self.status = "failed"

        self.completed_at = (

            datetime.now()
            .isoformat()
        )


    def to_dict(
        self
    ):

        return {

            "status":
                self.status,

            "started_at":
                self.started_at,

            "completed_at":
                self.completed_at,

            "current_step":
                self.current_step,

            "steps":
                self.steps,

            "errors":
                self.errors
        }