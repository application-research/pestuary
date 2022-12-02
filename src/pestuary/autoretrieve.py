from pestuary import Pestuary

pestuary = Pestuary()
autoretrieveApi = pestuary.get_autoretrieve_api()


def autoretrieve_create(pub_key, addresses):
    return autoretrieveApi.admin_autoretrieve_init_post(addresses, pub_key)


def autoretrieve_list():
    return autoretrieveApi.admin_autoretrieve_list_get()


def autoretrieve_heartbeat(token):
    return autoretrieveApi.autoretrieve_heartbeat_post(token)
