def patch_gpu(hw):

    gpu = hw["gpu"]

    if "Intel" in gpu:

        return {

            "AAPL,ig-platform-id":
            "0000A7A1",

            "device-id":
            "A7A10000"

        }

    return {}
