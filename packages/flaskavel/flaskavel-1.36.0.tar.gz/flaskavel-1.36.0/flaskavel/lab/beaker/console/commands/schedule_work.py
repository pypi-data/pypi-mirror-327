from app.Console.Kernel import Kernel  # type: ignore
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command
from flaskavel.lab.beaker.scheduling.schedule import Schedule

@reactor.register
class ScheduleWork(Command):
    """
    Command class to handle scheduled tasks within the Flaskavel application.
    """

    # The command signature used to execute this command.
    signature = 'schedule:work'

    # A brief description of the command.
    description = 'Starts the scheduled tasks'

    def handle(self) -> None:
        """
        Execute the scheduled tasks.

        This method initializes the Schedule and Kernel classes,
        registers the schedule, and starts the runner to execute
        the scheduled tasks.
        """

        try:

            # Inform the user that the scheduled jobs execution has started
            self.newLine()
            self.info(f"The execution of the scheduled jobs has started successfully.", timestamp=True)
            self.newLine()

            # Initialize a new Schedule instance.
            schedule = Schedule()

            # Create an instance of the Kernel class to manage the scheduling.
            kernel = Kernel()

            # Schedule tasks in the kernel using the provided schedule instance.
            kernel.schedule(schedule=schedule)

            # Start running the scheduled tasks using the schedule runner.
            schedule.runner()

        except Exception as e:

            # Display general error message for any unexpected issue
            self.error(f"An unexpected error occurred: {e}", timestamp=True)
            exit(1)
