import time


class Timer:
    """
    Simple timer for measuring
    execution time.
    """

    def __init__(self):

        self.start_time = None

        self.end_time = None


    def start(self):

        """
        Start timer.
        """

        self.start_time = time.perf_counter()

        self.end_time = None


    def stop(self):

        """
        Stop timer and return
        elapsed time.
        """

        if self.start_time is None:

            raise RuntimeError(
                "Timer has not been started."
            )

        self.end_time = time.perf_counter()

        return self.get_elapsed_time()


    def get_elapsed_time(self):

        """
        Return elapsed time
        in seconds.
        """

        if self.start_time is None:

            return 0.0


        end_time = (

            self.end_time

            if self.end_time is not None

            else time.perf_counter()
        )


        return round(

            end_time - self.start_time,

            4
        )


def measure_execution_time(
    function,
    *args,
    **kwargs
):
    """
    Run a function and measure
    its execution time.
    """

    timer = Timer()

    timer.start()


    result = function(
        *args,
        **kwargs
    )


    execution_time = timer.stop()


    return {

        "result": result,

        "execution_time_seconds":
            execution_time
    }