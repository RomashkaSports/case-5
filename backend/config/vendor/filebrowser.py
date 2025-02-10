# FileBrowser
# https://django-filebrowser.readthedocs.io/en/latest/settings.html

FILEBROWSER_DIRECTORY = ''
FILEBROWSER_VERSION_QUALITY = 80
VERSION_QUALITY = FILEBROWSER_VERSION_QUALITY

FILEBROWSER_VERSIONS = {
    'thumbnail': {
        'verbose_name': 'Thumbnail',
        'width': 60,
    }
}

FILEBROWSER_ADMIN_THUMBNAIL = 'thumbnail'
FILEBROWSER_ADMIN_VERSIONS = [
    'thumbnail',
]

FILEBROWSER_EXTENSIONS = {
    'Image': [
        '.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff',
        '.svg', '.webp',
    ],
    'Document': [
        '.csv', '.doc', '.docx', '.odp', '.ods', '.odt',
        '.ppt', '.pptx', '.txt', '.xls', '.xlsx', '.zip',
        '.pdf', '.rtf', '.vcf', '.svg',
    ],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p'],
}

MAX_UPLOAD_SIZE = 1024 ** 2 * 10
FILEBROWSER_MAX_UPLOAD_SIZE = MAX_UPLOAD_SIZE
NORMALIZE_FILENAME = True

FILEBROWSER_SHOW_IN_DASHBOARD = False
