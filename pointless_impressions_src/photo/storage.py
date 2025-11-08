from django.core.files.storage import FileSystemStorage


# Write your classes here.
class OverwriteStorage(FileSystemStorage):
    """Custom storage system that overwrites files with the same name."""
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name
