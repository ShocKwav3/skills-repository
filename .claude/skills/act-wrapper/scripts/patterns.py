"""
Filter patterns for act-wrapper.

PROGRESSIVE DEVELOPMENT: When you encounter verbose output that should be
filtered but isn't covered by these patterns, ADD a new pattern here.
Keep patterns as generic as possible to work across languages/ecosystems.
Document what each pattern matches with a comment.
"""

# Patterns to HIDE (filter out)
# Lines matching these are suppressed from output
HIDE_PATTERNS = [
    # === ACT Infrastructure ===
    r"🐳\s+docker",                            # Docker operations
    r"docker (pull|create|run|exec|cp)\s",     # Docker commands
    r"docker exec cmd=\[",                     # Docker exec details
    r"chown -R \d+:\d+",                       # Ownership changes
    r"node --no-warnings -e console\.log",     # Node path checks
    r"☁\s+git clone",                          # Action cloning
    r"⚙\s+::",                                 # Workflow commands
    r"::set-env::",                            # Set environment
    r"::set-output::",                         # Set output
    r"::add-path::",                           # Add to PATH
    r"❓\s+add-matcher",                        # Problem matchers
    r'msg="Using docker host',                 # Docker host info
    r"Cleaning up container for job",          # Container cleanup
    r"docker cp src=",                         # Action copying
    r"🚀\s+Start image=",                      # Container start

    # === Dependency Installation (generic) ===
    r"\|\s+\+\s+\S+[@=]",                      # + package==version or @version
    r"\|\s+(Downloading|Downloaded)\s+\S+",   # Download progress
    r"\|\s+Resolv(ed|ing)\s+\d+\s+package",   # Package resolution
    r"\|\s+Install(ed|ing)\s+\d+\s+package",  # Package installation
    r"\|\s+Prepared?\s+\d+\s+package",        # Package preparation
    r"\|\s+(Building|Built)\s+\S+\s+@",       # Package building
    r"\|\s+Found \S+ in .*(cache|toolcache)", # Cache hits
    r"\|\s+Added .+ to the path",             # Path additions

    # === Python/UV Specific ===
    r"\|\s+Creating virtual environment",     # Venv creation
    r"\|\s+Using (CPython|Python)",           # Python interpreter
    r"\|\s+warning:\s+Failed to hardlink",    # UV hardlink warnings
    r"\|\s+If the cache and target",          # Hardlink warning cont.
    r"\|\s+If this is intentional",           # Hardlink warning cont.
    r"\|\s+Trying to find version",           # UV version detection
    r"\|\s+Could not (find|determine)",       # UV config lookup
    r"\|\s+Getting latest version",           # UV version lookup
    r"\|\s+Set \w+(_\w+)* to",                # UV env var setting
    r"\|\s+Successfully installed \S+",       # pip install success
    r"\|\s+\S+_DIR is already set to",        # UV dir already set

    # === Node/npm Specific ===
    r"\|\s+Using (Node|npm)",                 # Node runtime
    r"\|\s+added \d+ packages",               # npm install summary
    r"\|\s+npm warn",                         # npm warnings

    # === Add new patterns below ===
]

# Patterns to KEEP (always show)
# These take priority over HIDE patterns - errors are never suppressed
KEEP_PATTERNS = [
    # === ACT Markers ===
    r"^level=warning",                        # ACT warnings
    r"🧪\s+Matrix:",                          # Matrix config
    r"⭐\s+Run",                              # Step start
    r"✅\s+Success",                          # Step success
    r"❌\s+Failure",                          # Step failure
    r"🏁\s+Job",                              # Job completion

    # === Error Indicators ===
    r"^Error:",                               # Error prefix
    r"^Error running",                        # ACT error
    r"\berror\b",                             # Word "error"
    r"\bfailed\b",                            # Word "failed"
    r"\bfailure\b",                           # Word "failure"
    r"\bexception\b",                         # Word "exception"
    r"Traceback \(most recent",               # Python traceback
    r"^\s+at\s+.+:\d+:\d+",                   # JS stack trace
    r"panic:",                                # Go panic
    r"FAILED",                                # Test failure
    r"ERROR",                                 # Error (caps)
    r"exit code [1-9]",                       # Non-zero exit
    r"exit status [1-9]",                     # Non-zero status
    r"returned non-zero",                     # Command failure
]
