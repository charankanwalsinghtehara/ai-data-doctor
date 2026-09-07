from .timer import (
    Timer
)

from .memory_monitor import (

    get_memory_usage,

    get_memory_difference
)


class PerformanceMonitor:
    """
    Monitor execution time
    and memory usage.
    """

    def __init__(self):

        self.step_name = None

        self.timer = Timer()

        self.memory_before = None

        self.memory_after = None


    def start(
        self,
        step_name
    ):
        """
        Start monitoring.
        """

        self.step_name = step_name


        self.memory_before = (

            get_memory_usage()
        )


        self.timer.start()


    def stop(self):
        """
        Stop monitoring and
        return performance data.
        """

        execution_time = (

            self.timer.stop()
        )


        self.memory_after = (

            get_memory_usage()
        )


        memory_difference = (

            get_memory_difference(

                self.memory_before,

                self.memory_after
            )
        )


        return {

            "step_name":

                self.step_name,


            "execution_time_seconds":

                execution_time,


            "memory":

                memory_difference
        }