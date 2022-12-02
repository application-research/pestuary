from pestuary import Pestuary

pestuary = Pestuary()
pinningApi = pestuary.get_pinning_api()


# creates a new pin
def pin_create(cid, name):
    return pinningApi.pinning_pins_post({
        "cid": cid,
        "name": name
    })


# list all pins for this user
def pin_list():
    return pinningApi.pinning_pins_get()

