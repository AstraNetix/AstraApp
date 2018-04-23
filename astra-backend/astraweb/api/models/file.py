from django.db import models
from django.contrib.auth import get_user_model
import mimetypes

User = get_user_model()

def get_upload_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.user.email, filename)

class FileManager(models.Manager):
    def create(self, **extra_fields):
        new_file = self.model(**extra_fields)
        if not new_file.mimetype and new_file.name:
            new_file.mimetype = mimetypes.guess_type(new_file.name)
        new_file.save()

class File(models.Model):
    NONE        =   "NO"
    SELFIE      =   "SF"
    ID_FILE     =   "ID"

    FILE_TYPES  =   (   
                        (NONE,      'None'      ),
                        (SELFIE,    'Selfie'    ),
                        (ID_FILE,   'ID File'   ),
                    )
    
    MIME_TYPES  =   (
                        ('text/plain',                  'Plain Text'    ),
                        ('text/html',                   'HTML'          ),
                        ('text/css',                    'CSS'           ),
                        ('text/javascript',             'Javascript'    ),
                        ('image/gif',                   'GIF'           ),
                        ('image/png',                   'PNG'           ),
                        ('image/png',                   'PNG'           ),
                        ('image/jpeg',                  'JPEG'          ),
                        ('image/bmp',                   'BMP'           ),
                        ('image/webp',                  'WEBP'          ),
                        ('audio/midi',                  'MIDI'          ),
                        ('audio/mpeg',                  'MPEG'          ),
                        ('audio/webm',                  'WEBM'          ),
                        ('audio/ogg',                   'OGG'           ),
                        ('audio/wav',                   'WAV'           ),
                        ('video/webm',                  'WEBM'          ),
                        ('video/ogg',                   'OGG'           ),
                        ('application/octet-stream',    'Octet Stream'  ),
                        ('application/pkcs12',          'PKCS12'        ),
                        ('application/vnd.mspowerpoint','MS Powerpoint' ),
                        ('application/xhtml+xml',       'XHTML XML'     ),
                        ('application/xml',             'XML'           ),
                        ('application/pdf',             'PDF'           ),
                        ('multipart/form-data',         'Form Data'     ),
                        ('multipart/byteranges',        'Byte Ranges'   ),
                    )
    
    objects     =   FileManager()

    created     =   models.DateTimeField(auto_now_add=True)
    name        =   models.CharField(max_length=300, null=True, blank=True)
    user        =   models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    datafile    =   models.FileField(upload_to=get_upload_path)
    filetype    =   models.CharField(max_length=2, default=NONE, choices=FILE_TYPES)
    mimetype    =   models.CharField(max_length=50, default='text/plain', choices=MIME_TYPES)
    verified    =   models.BooleanField(default=False)

    @property
    def email(self):
        return self.user.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not kwargs['mimetype']:
            mimetypes.guess_type(kwargs.pop('name', ''))[0]


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