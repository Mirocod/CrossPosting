from django.core import signing
from django.core.management import BaseCommand

from crossposting_backend.settings import SALT, BASE_DIR


class Command(BaseCommand):
    def handle(self, *args, **options):
        environments = {}
        with open(BASE_DIR / '.env') as env_file:
            for line in env_file:
                env_key, env_value = line.strip().split('=')
                environments[env_key] = env_value

        signer = signing.Signer(salt=SALT)
        with open(BASE_DIR / '.env.encoded', 'w') as out_env_file:
            for env_key, env_value in environments.items():
                env_item = {
                    env_key: env_value
                }
                encoded_env_item = signer.sign_object(env_item)
                line_with_encoded_value = '%s=%s\n' % (env_key, encoded_env_item)
                out_env_file.write(line_with_encoded_value)
