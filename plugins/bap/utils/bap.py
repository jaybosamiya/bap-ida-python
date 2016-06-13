"""Utilities that interact with BAP."""


def run_bap_with(argument_string):
    """
    Run bap with the given argument_string.

    Uses the currently open file, dumps latest symbols from IDA and runs
    BAP with the argument_string

    Also updates the 'BAP View'
    """
    from bap.plugins.bap_view import BAP_View
    from bap.utils import config
    import ida
    import idc
    import tempfile

    args = {
        'bap_executable_path': config.get('bap_executable_path'),
        'bap_output_file': tempfile.mkstemp(suffix='.out',
                                            prefix='ida-bap-')[1],
        'input_file_path': idc.GetInputFilePath(),
        'symbol_file_location': tempfile.mkstemp(suffix='.sym',
                                                 prefix='ida-bap-')[1],
        'remaining_args': argument_string
    }

    ida.dump_symbol_info(args['symbol_file_location'])

    command = (
        "\
        \"{bap_executable_path}\" \"{input_file_path}\" \
        --read-symbols-from=\"{symbol_file_location}\" --symbolizer=file \
        {remaining_args} \
        -d > \"{bap_output_file}\" 2>&1 \
        ".format(**args)
    )

    idc.Exec(command)

    with open(args['bap_output_file'], 'r') as f:
        BAP_View.update(
            "BAP execution string\n" +
            "--------------------\n" +
            "\n" +
            '\n    --'.join(('bap'+argument_string).split('--')) +
            "\n" +
            "\n" +
            "Output\n" +
            "------\n" +
            "\n" +
            f.read()
        )

    # Force close BAP View
    # This forces the user to re-open the new view if needed
    # This "hack" is needed since IDA decides to give a different BAP_View
    #   class here, than the cls parameter it sends to BAP_View
    # TODO: Fix this
    import idaapi
    tf = idaapi.find_tform("BAP View")
    if tf:
        idaapi.close_tform(tf, 0)

    idc.Exec("rm -f \"{symbol_file_location}\" \
             \"{bap_output_file}\"".format(**args))  # Cleanup
