def parse_arguments(arguments):
    """Parses the command-line arguments in the form of --argument=value or just --flag."""
    args_dict = {}
    for arg in arguments:
        if '=' in arg and arg.startswith('--'):
            key, value = arg.lstrip('-').split('=', 1)
            args_dict[key] = value
        elif arg.startswith('--'):
            key = arg.lstrip('-')
            # Treat flags without values as True
            args_dict[key] = True
    return args_dict

