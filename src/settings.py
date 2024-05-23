from decouple import config

# load database url from env
DATABASE_URL = config('DATABASE_URL')
