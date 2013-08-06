"""This module is responsible for printing
   the results from the cloud endpoint."""

import prettytable

class Reporter(object):
    """The reporter class."""
    def __init__(self):
        pass

    @staticmethod
    def get_pretty_params(params):
        """Returns a pretty reprsentation of conf params."""
        conf_table = prettytable.PrettyTable(["Configuration parameter"
            ,"Value"])
        for param, value in params.items():
            if value == True:
                value = "Yes"
            elif value == False:
                value == "No"
            conf_table.add_row([param, value])
        return conf_table

    @staticmethod
    def get_pretty_func(func_results):
        """Returns a pretty representation of funcionality params."""
        func_table = prettytable.PrettyTable(["Action", "Parameters used",
            "Is Functional"])
        for action, result in func_results.items():
            if result == True:
                result = "Yes"
            else:
                result = "No"
            # Arguments support  has not been implemented yet.
            func_table.add_row([action, "Not Implemented", result])
        return func_table
