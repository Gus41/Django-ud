from .envioroment import BASE_DIR


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'base_static'
]

#collectstatic
STATIC_ROOT = BASE_DIR / 'static'

#caminhos para os arquivos que forem recebidos
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'