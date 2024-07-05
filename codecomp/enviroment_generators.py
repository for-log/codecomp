def python_generate(func_call, tests_input_output, upload_filename):
    start_code = "true_exit = exit\n\ndef exit(x): true_exit(2)\n\n"
    
    with open(f"./uploads/{upload_filename}", "r") as f:
        start_code += f.read()

    start_code += "\n\n"
    for input, output in tests_input_output:
        tmp = start_code +  f"if {func_call}("
        for key in input:
            tmp += f"{key}={input[key]},"
        tmp += f") != {output}:\n\ttrue_exit(2)\n"
        yield tmp
