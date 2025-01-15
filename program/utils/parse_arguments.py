def parse_arguments(arguments):
    """Parses the command-line arguments in the form of --argument=value or just --flag."""
    args_dict = {}
    i = 0
    while i < len(arguments):
        arg = arguments[i]
        if '=' in arg and arg.startswith('--'):
            # Case for arguments like --argument=value
            key, value = arg.lstrip('--').split('=', 1)
            args_dict[key] = value
        elif arg.startswith('--'):
            # Case for flags with no equal sign
            key = arg.lstrip('--')
            if i + 1 < len(arguments) and not arguments[i + 1].startswith('--'):
                # If the next argument is not a flag, treat it as the value for this argument
                args_dict[key] = arguments[i + 1]
                i += 1  # Skip next argument
            else:
                # Treat as a flag with no value
                args_dict[key] = True
        i += 1
    return args_dict
