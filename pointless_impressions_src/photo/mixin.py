import cloudinary.uploader


# Create your classes here.
class PhotoUploadMixin:
    """
    Mixin to handle photo uploads to Cloudinary with overwrite and public_id
    options. Can be used in CBVs or FBVs across apps.
    """
    def upload_photo_to_cloudinary(self, photo_instance, file, overwrite=True):
        """
        Uploads a file to Cloudinary using options from the photo instance.
        Returns the Cloudinary upload result dict.
        """
        options = photo_instance.upload_options(overwrite=overwrite)
        result = cloudinary.uploader.upload(file, **options)
        return result

    def save_photo_url(self, photo_instance, cloudinary_result):
        """
        Saves the Cloudinary URL and public_id to the photo instance.
        Call this after upload_photo_to_cloudinary.
        """
        photo_instance.image = cloudinary_result.get('secure_url')
        # Optionally save public_id or other metadata
        # photo_instance.cloudinary_public_id = cloudinary_result.get(
        #     'public_id'
        # )
        photo_instance.save()
