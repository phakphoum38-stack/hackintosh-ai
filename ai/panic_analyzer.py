def analyze(log):

    if "GPU Panic" in log:

        return {
            "issue":"GPU Configuration",
            "fix":"Check WhateverGreen"
        }

    if "ACPI Error" in log:

        return {
            "issue":"ACPI",
            "fix":"Patch DSDT"
        }

    return {
        "issue":"Unknown",
        "fix":"Verbose Boot Required"
    }
