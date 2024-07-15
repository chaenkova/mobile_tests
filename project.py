import pydantic
import dotenv


class Config(pydantic.BaseSettings):
    bstack_accessKey: str
    bstack_userName: str
    base_url: str

    @property
    def bstack_creds(self):
        return {
            'userName': self.bstack_userName,
            'accessKey': self.bstack_accessKey,
        }


project_config = Config(dotenv.find_dotenv())
config = Config()
