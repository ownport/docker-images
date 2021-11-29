
import subprocess


class CommandException(Exception):
    pass


class Command:

    @classmethod
    def invoke(cls, cmd, stderr=None):
        """Invoke the given command, and return a tuple of process and raw binary output.

        If stderr is defined as None, it will flow to wherever it is currently mapped
        for the parent process, generally to the terminal where the user can see the error
        (cf. https://docs.python.org/3.7/library/subprocess.html#subprocess.Popen ). In
        some cases we want to treat it specially, which is why it is exposed
        in the signature of _invoke.

        :param list cmd: The command in the form of a list of strings
        :returns: The completed process object and its standard output.
        :raises: Scm.LocalException if there was a problem exec'ing the command at all.
        """
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=stderr)
        except OSError as e:
            # Binary DNE or is not executable
            cmd_str = " ".join(cmd)
            raise CommandException(f"Failed to execute command {cmd_str}: {e!r}")
        out, err = process.communicate()
        return process, out, err

    @classmethod
    def cleanse(cls, output, errors="strict"):
        return output.strip().decode("utf-8", errors=errors)

    @classmethod
    def check_result(cls, cmd, result_code, err, failure_msg=None):
        if result_code != 0:
            cmd_str = " ".join(cmd)
            raise CommandException(failure_msg or f"{cmd_str} failed with exit code {result_code}, error: {err}")
