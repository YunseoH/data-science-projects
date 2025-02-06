import sys

_DEBUG_MODE_ = False


def print_log(tag, msg):
    sys.stderr.write(f"[{tag}] {str(msg)}\n")


def debug_log(msg):
    if _DEBUG_MODE_:
        print_log("DEBUG", msg)


def info_log(msg):
    print_log("INFO", msg)


def warning_log(msg):
    print_log("WARNING", msg)


def error_log(msg):
    print_log("ERROR", msg)
