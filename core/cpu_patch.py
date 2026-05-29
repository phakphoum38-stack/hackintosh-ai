def patch_cpu(hw):

    cpu = hw["cpu"]

    if "13" in cpu:

        return {

            "FakeCPUID":
            "A9060300",

            "boot_args":
            "-v keepsyms=1 debug=0x100"

        }

    return {}
