import configparser


from pydantic import BaseSettings


class GlobalSettings(BaseSettings):
    APP_ENV: str = 'prod'


class DevSettings(GlobalSettings):
    class Config:
        env_file = 'config-dev.ini'


class ProdSettings(GlobalSettings):
    class Config:
        env_file = 'config.ini'


class FactorySettings(object):
    @staticmethod
    def load():
        config = configparser.ConfigParser()
        app_env = GlobalSettings().APP_ENV
        if app_env == 'dev':
            config.read(DevSettings.Config.env_file)
        elif app_env == 'prod':
            config.read(ProdSettings.Config.env_file)
        else:
            raise
        return config


config_obj = FactorySettings.load()
