class NotFoundError(Exception):
    pass


class StorageError(Exception):
    pass


class StorageFKError(Exception):
    pass


class StorageConstraintError(Exception):
    pass


class S3Error(Exception):
    pass


class DiskStorageError(Exception):
    pass


class PermissionsError(Exception):
    pass


class ValidationError(Exception):
    pass
