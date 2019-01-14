from pymitter import EventEmitter

"""
This list contains the list of loggers which log each event occuring in the experiment
"""
logger_list = []

def log_start_experiment(args):
    experiment = args.get('experiment', None)
    append_runs = args.get('append_runs', False)

    if experiment is not None:
        for logger in logger_list:
            logger.log_start_experiment(experiment=experiment, append_runs=append_runs)


def log_stop_experiment(args):
    experiment = args.get('experiment', None)

    if experiment is not None:
        for logger in logger_list:
            logger.log_stop_experiment(experiment=experiment)


def put_experiment_configuration(args):
    experiment = args.get('experiment', None)

    if experiment is not None:
        for logger in logger_list:
            logger.put_experiment_configuration(experiment=experiment)


def log_start_run(args):
    run = args.get('run', None)
    if run is not None:
        for logger in logger_list:
            logger.log_start_run(run=run)


def log_stop_run(args):
    run = args.get('run', None)
    if run is not None:
        for logger in logger_list:
            logger.log_stop_run(run=run)


def log_start_split(args):
    split = args.get('split', None)
    if split is not None:
        for logger in logger_list:
            logger.log_start_split(split=split)


def log_stop_split(args):
    split = args.get('split', None)
    if split is not None:
        for logger in logger_list:
            logger.log_start_split(split=split)


def log_score(args):
    pass


def log_results(args):
    pass


def log_event(args):
    pass


def log(args):
    print(args)


def warn(args):
    pass


def error(args):
    pass


"""
This dictionary contains all the events that are to be handled and also their corresponding event handling function
"""
EVENT_HANDLER_DICT = {
    'EVENT_START_EXPERIMENT': [log_start_experiment],
    'EVENT_STOP_EXPERIMENT': [log_stop_experiment],
    'EVENT_START_RUN': [log_start_run],
    'EVENT_STOP_RUN': [log_stop_run],
    'EVENT_START_SPLIT': [log_start_split],
    'EVENT_STOP_SPLIT': [log_stop_split],
    'EVENT_PUT_EXPERIMENT_CONFIGURATION': [put_experiment_configuration],
    'EVENT_LOG_SCORE': [log_score],
    'EVENT_LOG_RESULTS': [log_results],
    'EVENT_LOG_EVENT': [log_event],
    'EVENT_LOG': [log],
    'EVENT_WARN': [warn],
    'EVENT_ERROR': [error]
}

"""
The event names are taken from the event handler dictionary
"""
EVENT_NAMES = list(EVENT_HANDLER_DICT.keys())

"""
As each event occurs, the event is pushed into the event queue, this would allow the events to be handled at their own 
pace and would not cause any out of order event handling(like closing the experiment while results are being written to 
the backend)
"""
EVENT_QUEUE = []
class event_queue:
    _event_queue = []
    _emptying_queue = False

    def process_events(self):
        """
        This function processes the events currently pending in the queue.
        Functions corresponding to each event are obtained from the EVENT_HANDLER_DICT
        :return:
        """

        while self._event_queue:
            """
            The event should contain the EVENT_NAME and the args for the function call
            Args is a dictionary which would be unwrapped by the corresponding function call to obtain the required
            parameters
            """
            self._emptying_queue = True
            event = self._event_queue.pop(0)
            print(event)
            event_handlers = EVENT_HANDLER_DICT.get(event['EVENT_NAME'], None)
            if event_handlers is None:
                """
                UNHANDLED EVENT ENCOUNTERED
                """
                print('UNHANDLED EVENT ENCOUNTERED')
                return

            args = event.get('args', None)
            # If there are multiple event handlers for the same event, iterate through each handler
            if len(event_handlers) > 1:
                for event_handler in event_handlers:
                    event_handler(args=args)
            else:
                event_handlers[0](args)

        self._emptying_queue = False

    @property
    def event_queue(self):
        return self._event_queue

    @event_queue.setter
    def event_queue(self, event):
        self._event_queue.append(event)
        if not self._emptying_queue:
            # Create thread and empty queue
            self.process_events()


event_queue_obj = event_queue()

"""
This list contains all the loggers for the experiment. Each logger can have a backend. In this way the experiment 
can support multiple loggers and multiple backends
"""
logger_list = []


def add_event_to_queue(args):
    """
    This function appends the newly fired event to the event queue
    :param args: Arguments to be used for the event
    :return:
    """
    print('Adding event to Queue')
    event_queue_obj.event_queue = args

eventemitter = EventEmitter()
eventemitter.on('EVENT', add_event_to_queue)


def process_events():
    """
    This function processes the events currently pending in the queue.
    Functions corresponding to each event are obtained from the EVENT_HANDLER_DICT
    :return:
    """

    while EVENT_QUEUE:
        """
        The event should contain the EVENT_NAME and the args for the function call
        Args is a dictionary which would be unwrapped by the corresponding function call to obtain the required
        parameters
        """
        event = EVENT_QUEUE.pop(0)
        print(event)
        event_handlers = EVENT_HANDLER_DICT.get(event['EVENT_NAME'], None)
        if  event_handlers is None:
            """
            UNHANDLED EVENT ENCOUNTERED
            """
            print('UNHANDLED EVENT ENCOUNTERED')
            return


        args = event.get('args', None)
        # If there are multiple event handlers for the same event, iterate through each handler
        if len(event_handlers) > 1:
            for event_handler in event_handlers:
                event_handler(args=args)
        else:
            event_handlers[0](args)


class EventHandler:

    _eventemitter = EventEmitter()
    _logger_list = None

    def __init__(self, logger_list=None):
        """
        This function initializes the event emitter object for handling the different events.
        A list of loggers should also be passed for logging the events
        """
        _logger_list = logger_list

    def log_start_experiment(self, args):
        experiment = args.get('experiment', None)
        append_runs = args.get('append_runs', False)

        if experiment is not None:
            for logger in self._logger_list:
                logger.log_start_experiment(experiment=experiment, append_runs=append_runs)

    def log_stop_experiment(self, args):
        experiment = args.get('experiment', None)

        if experiment is not None:
            for logger in self._logger_list:
                logger.log_stop_experiment(experiment=experiment)

    def put_experiment_configuration(self, args):
        pass

    def log_start_run(self, args):
        run = args.get('run', None)
        if run is not None:
            for logger in self._logger_list:
                logger.log_start_run(run=run)

    def log_stop_run(self, args):
        run = args.get('run', None)
        if run is not None:
            for logger in self._logger_list:
                logger.log_stop_run(run=run)

    def log_start_split(self, args):
        split = args.get('split', None)
        if split is not None:
            for logger in self._logger_list:
                logger.log_start_split(split=split)

    def log_stop_split(self, args):
        split = args.get('split', None)
        if split is not None:
            for logger in self._logger_list:
                logger.log_start_split(split=split)

    def log_score(self, args):
        pass

    def log_results(self, args):
        pass

    def log_event(self, args):
        pass

    def log(self, args):
        print(args)

    def warn(self, args):
        pass

    def error(self, args):
        pass

    # Binding events to event handlers
    _eventemitter.on("start_experiment", log_start_experiment)
    _eventemitter.on("stop_experiment", log_stop_experiment)

    _eventemitter.on("start_run", log_start_run)
    _eventemitter.on("stop_run", log_stop_run)

    _eventemitter.on("start_split", log_start_split)
    _eventemitter.on("stop_split", log_stop_split)

    _eventemitter.on("log_score", log_score)
    _eventemitter.on("log_results", log_results)

    _eventemitter.on("log_event", log_event)
    _eventemitter.on("log", log)
    _eventemitter.on("warn", warn)
    _eventemitter.on("error", error)

    @property
    def eventemitter(self):
        return self._eventemitter