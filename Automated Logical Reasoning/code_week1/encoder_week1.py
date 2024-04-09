class DimacsCnfEncoding:
    """
    Class for DIMACS CNF Encoding. Currently functions for assignment 1 of Automated Logical Reasoning/color graphs.
    """

    def __init__(self):
        # Uses self.reset_variables to init for efficiencies sake.
        self.dimacs_cnf = None
        self.edges = None
        self.arg_index = None
        self.arg_set = None
        self.reset_variables()

    def reset_variables(self):
        """
        Resets all variables used for the DIMACS CNF Encoding.
        """
        self.arg_set = set()
        self.arg_index = dict()
        self.edges = list()
        self.dimacs_cnf = list()

    def read_graph_input(self, input_file, reset=True):
        """
        Reads an input file and provides the basic systems for future interpretation. Requires a "x y" variable
        encoding, where there is an edge between x and y. Provides a dictionary and list that define translations
        between the variable names and the graph edges.
        :param reset:
        :param input_file: The location for the input file.
        """

        # Resets all variables in play.
        if reset:
            self.reset_variables()

        # Opening text document and reading its contents to establish edges and an arg set
        text = open(input_file, "r").read().split("\n")
        for i, line in enumerate(text):
            self.edges.append(line.split())
            for item in self.edges[-1]:
                self.arg_set.add(item)

        # Creating arg_index dictionary from arg_set
        self.arg_index = {var: i + 1 for i, var in enumerate(sorted(self.arg_set))}

    def add_colors(self, colors):
        """
        Adds an unspecified # of colors to the arg_index dict (i.e. 2 colors for a, b would make a:1 b:2 -> a:1,
        3 b:2,4).
        :param colors: number of colors to use.
        """
        # Making sure that the # of colors is an integer, else inform the user.
        if type(colors) is int:
            num_args = len(self.arg_index)

            # Setting color variables to the dict
            for key, value in self.arg_index.items():
                color_nums = []
                for i in range(colors):
                    color_nums.append(value + i * num_args)
                self.arg_index[key] = color_nums
        else:
            print("Colors is not an integer! Add_colors will not run.")

    def cnf_color_encoding(self, colors=False):
        """
        Encodes a graph with a # of colors into DIMACS CNF format through the self.dimacs_cnf value in list form (
        i.e. [1 2 0], [-2 3 0]).
        :param colors: number of colors to use. Uses self.add_colors.
        """
        # Adding colors
        if colors:
            self.add_colors(colors)

        # Ensuring each node is assigned exactly one color
        for key, indices in self.arg_index.items():
            # Adding clauses to ensure only one color for A, B, C
            self.dimacs_cnf.append(indices)
            for i in range(len(indices)):
                for j in range(i + 1, len(indices)):
                    # Ensuring no adjacent nodes have the same color
                    self.dimacs_cnf.append([-indices[i], -indices[j]])

        # Clauses to ensure no conflicting colors
        for edge in self.edges:
            for i in range(len(self.arg_index[edge[0]])):
                self.dimacs_cnf.append([-self.arg_index[edge[0]][i], -self.arg_index[edge[1]][i]])

        # num_variables = max(max(abs(literal) for literal in clause) for clause in self.dimacs_cnf)
        # num_clauses = len(self.dimacs_cnf)
        # self.dimacs_cnf.insert(0, f"p cnf {num_variables} {num_clauses}")

    def cnf_printing(self, console=True, file_print_loc=""):
        """
        Will return a dimacs cnf form into the console and/or a file.
        :param console: Prints the output to a console. Set as true. Should be a true/false boolean.
        :param file_print_loc: The location to print your file. Set as empty.
        """
        # Setting number of variables, clauses for 1st p cnf line
        num_variables = max(max(abs(literal) for literal in clause) for clause in self.dimacs_cnf)
        num_clauses = len(self.dimacs_cnf)

        # Printing to console
        if console:
            print(f"p cnf {num_variables} {num_clauses}")
            for clause in self.dimacs_cnf:
                print(' '.join(map(str, clause + [0])))

        # Printing to file
        if file_print_loc:
            with open(file_print_loc, 'w') as file:
                file.write(f"p cnf {num_variables} {num_clauses}\n")
                for clause in self.dimacs_cnf:
                    file.write(' '.join(map(str, clause + [0])) + '\n')
