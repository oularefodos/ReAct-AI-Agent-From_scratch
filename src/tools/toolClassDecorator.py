class Tool(object):
    """
    Represents a reusable, self-documented function (Tool).

    Attributes:
        name (str): The identifier for the tool.
        description (str): A concise explanation of the tool's functionality.
        func (callable): The underlying function that the tool encapsulates.
        arguments (list): A list detailing the expected parameters (name and type) for the function.
        outputs (str or list): A description of the return type(s) produced by the function.
    """
    def __init__(self,
                name: str,
                description: str,
                args: list,
                outputs: str,
                call_func: callable):
        self.name = name
        self.description = description
        self.call_func = call_func
        self.args = args
        self.outputs = outputs

    def __str__(self) -> str:
        """
        Returns a formatted string that details the tool's name, description, 
        input arguments, and output types.
        """
        args_str = ", ".join([
            f"{arg_name}: {arg_type}" for arg_name, arg_type in self.args
        ])

        return (
            f"Tool Name: {self.name},"
            f" Description: {self.description},"
            f" Arguments: {args_str},"
            f" Outputs: {self.outputs}"
        )
    
    def __call__(self, *args):
        """
        Invoke the underlying function (callable) with provided arguments.
        """
        if (len(self.args) == 0):
            return self.call_func();
        if (len(args) != len(self.args)):
            raise ValueError("Incorrect number of arguments provided.")
        return self.call_func(*args)

def tool(name: str, description: str, args: list, outputs: str):
    """
    Decorator function for creating a Tool object from a function.

    Args:
        name (str): The identifier for the tool.
        description (str): A concise explanation of the tool's functionality.
        args (list): A list detailing the expected parameters (name and type) for the function.
        outputs (str or list): A description of the return type(s) produced by the function.
    """
    def decorator(func):
        return Tool(name, description, args, outputs, func)
    return decorator