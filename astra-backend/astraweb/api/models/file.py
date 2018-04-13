from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def get_upload_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.user.email, filename)

class File(models.Model):
    NONE        =   "NO"
    SELFIE      =   "SF"
    ID_FILE     =   "ID"

    FILE_TYPES  =   (   
                        (SELFIE,    'Selfie'    ),
                        (ID_FILE,   'ID File'   ),
                    )

    created     =   models.DateTimeField(auto_now_add=True)
    name        =   models.CharField(max_length=300, null=True, blank=True)
    user        =   models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    datafile    =   models.FileField(upload_to=get_upload_path)
    filetype    =   models.CharField(max_length=2, default=NONE, choices=FILE_TYPES)
    verified    =   models.BooleanField(default=False)

    @property
    def email(self):
        return self.user.email

    @classmethod
    def id_file(cls, user):
        """
        Returns the latest identification file the user uploaded
        """
        try:
            return user.files.filter(filetype=cls.ID_FILE).latest('created')
        except cls.DoesNotExist:
            return False

    @classmethod 
    def selfie(cls, user):
        """
        Returns the latest self image the user uploaded
        """
        try:
            return user.files.filter(filetype=cls.SELFIE).latest('created')
        except cls.DoesNotExist:
            return False