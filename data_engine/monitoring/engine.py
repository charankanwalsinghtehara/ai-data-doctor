from datetime import datetime

from .performance_monitor import (
    PerformanceMonitor
)


class MonitoringEngine:
    """
    Monitor the complete
    AI Data Doctor pipeline.
    """

    def __init__(self):

        self.pipeline_start_time = None

        self.pipeline_end_time = None

        self.step_results = {}


    def start_pipeline(self):

        """
        Start pipeline monitoring.
        """

        self.pipeline_start_time = (
            datetime.now()
        )


    def stop_pipeline(self):

        """
        Stop pipeline monitoring.
        """

        self.pipeline_end_time = (
            datetime.now()
        )


    def start_step(
        self,
        step_name
    ):

        """
        Start monitoring one step.
        """

        monitor = PerformanceMonitor()

        monitor.start(
            step_name
        )


        return monitor


    def complete_step(
        self,
        monitor
    ):

        """
        Complete monitoring
        for one step.
        """

        result = monitor.stop()


        step_name = result[
            "step_name"
        ]


        self.step_results[
            step_name
        ] = result


        return result


    def get_pipeline_report(self):

        """
        Return complete
        monitoring report.
        """

        total_time = None


        if (

            self.pipeline_start_time

            and

            self.pipeline_end_time
        ):

            total_time = (

                self.pipeline_end_time

                - self.pipeline_start_time

            ).total_seconds()


        return {

            "pipeline_monitoring": {

                "started_at":

                    (

                        self.pipeline_start_time.isoformat()

                        if self.pipeline_start_time

                        else None
                    ),


                "completed_at":

                    (

                        self.pipeline_end_time.isoformat()

                        if self.pipeline_end_time

                        else None
                    ),


                "total_execution_time_seconds":

                    (

                        round(
                            total_time,
                            4
                        )

                        if total_time is not None

                        else None
                    ),


                "steps":

                    self.step_results
            }
        }