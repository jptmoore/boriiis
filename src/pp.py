import sys

def pp(msg):
    print(f"\U0001F680 {msg}", file=sys.stderr)

def pp_exit(msg):
    print(f"\n\U0001F4A5 {msg}", file=sys.stderr)
    sys.exit(1)