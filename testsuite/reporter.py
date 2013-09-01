#Copyright (C) 2013 CERN
#
#    Author: Artem Tsikiridis <artem.tsikiridis@cern.ch>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3, as
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
            func_table.add_row([action, "will be there soon", result])
        return func_table
