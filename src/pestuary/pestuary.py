# is this deprecated? I don't see it in the docs
def shuttle_create():
    response = requests.post(ESTUARY_URL + 'admin/shuttle/init',
                             headers={'Authorization': 'Bearer ' + ESTUARY_KEY})
    return response.json()


# TODO I don't really understand this method
# I think we want to use this https://github.com/snissn/estuary-swagger-clients/blob/main/python/docs/CollectionsApi.md#collections_coluuid_get
def collection_fs_list(collection_uuid, collection_path, recursive=False):
    query_params = f'col={collection_uuid}&dir={collection_path}'

    response = requests.get(ESTUARY_URL + f'collections/fs/list?{query_params}',
                            headers={'Authorization': 'Bearer ' + ESTUARY_KEY},
                            )

    if not recursive:
        return response.json()

    responses = []
    for entry in response.json():
        responses.append(entry)
        if entry["type"] == "directory":
            responses[-1]["contents"] = collection_fs_list(collection_uuid, collection_path + "/" + entry["name"])

    return responses


def main():
    cli()


if __name__ == '__main__':
    main()
