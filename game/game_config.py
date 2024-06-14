import yaml


class GameConfig:
    with open("game/config.yaml", 'r') as file:
        config = yaml.load(file, yaml.FullLoader)

    @classmethod
    @property
    def ROWS(cls) -> int:
        return cls.config['board_size']['rows']

    @classmethod
    @property
    def COLS(cls) -> int:
        return cls.config['board_size']['cols']
