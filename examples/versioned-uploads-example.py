from pestuary import versioned_uploads

if __name__ == '__main__':
    uploads = versioned_uploads.VersionedUploads()

    response = uploads.add_with_version('a.txt')
    print(response)

