import dataclasses as dc
import json
import requests
from typing import Optional, Dict, List


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dc.is_dataclass(o):
            return dc.asdict(o)
        return super().default(o)


@dc.dataclass
class WebsiteAuthData(object):
    cookie_jar: requests.cookies.RequestsCookieJar
    access_token: str
    region: str


@dc.dataclass(frozen=True)
class BlizzardGame:
    uid: str
    name: str
    family: str


@dc.dataclass(frozen=True)
class ClassicGame(BlizzardGame):
    registry_path: Optional[str] = None
    registry_installation_key: Optional[str] = None
    exe: Optional[str] = None
    bundle_id: Optional[str] = None


@dc.dataclass
class RegionalGameInfo:
    uid: str
    try_for_free: bool


@dc.dataclass
class ConfigGameInfo(object):
    uid: str
    uninstall_tag: Optional[str]
    last_played: Optional[str]


@dc.dataclass
class ProductDbInfo(object):
    uninstall_tag: str
    ngdp: str = ''
    install_path: str = ''
    version: str = ''
    playable: bool = False
    installed: bool = False


class Singleton(type):
    _instances = {}  # type: ignore

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _Blizzard(object, metaclass=Singleton):
    TITLE_ID_MAP = {
        1095647827: RegionalGameInfo('anbs', False),
        1095849281: RegionalGameInfo('aqua', False),
        1095911763: RegionalGameInfo('aris', False),
        4280907: RegionalGameInfo('ark', False),
        1096108883: RegionalGameInfo('auks', False),
        17459: RegionalGameInfo('diablo3', True),
        1146246220: RegionalGameInfo('drtl', False),
        4613486: RegionalGameInfo('fenris', False),
        4674137: RegionalGameInfo('gry', False),
        1179603525: RegionalGameInfo('fore', False),
        1179603526: RegionalGameInfo('fore', False),
        1179603527: RegionalGameInfo('fore', False),
        1214607983: RegionalGameInfo('heroes', True),
        1465140039: RegionalGameInfo('hs_beta', True),
        1279351378: RegionalGameInfo('lazarus', False),
        1279414849: RegionalGameInfo('lbra', False),
        1329875278: RegionalGameInfo('odin', True),
        1330467921: RegionalGameInfo('odin', True),
        1330467922: RegionalGameInfo('odin', True),
        1330467923: RegionalGameInfo('odin', True),
        5198665: RegionalGameInfo('osi', False),
        5272175: RegionalGameInfo('prometheus', False),
        1381257807: RegionalGameInfo('rtro', False),
        21297: RegionalGameInfo('s1', True),
        21298: RegionalGameInfo('s2', True),
        1396920146: RegionalGameInfo('scor', False),
        1430151241: RegionalGameInfo('viper', False),
        1430151242: RegionalGameInfo('viper', False),
        1430151243: RegionalGameInfo('viper', False),
        1447645266: RegionalGameInfo('viper', False),
        1514493267: RegionalGameInfo('zeus', False),
        1514558547: RegionalGameInfo('zeus', False),
        1514558548: RegionalGameInfo('zeus', False),
        1514558549: RegionalGameInfo('zeus', False),
        1463898673: RegionalGameInfo('w1', False),
        5714258: RegionalGameInfo('w1r', False),
        1462911566: RegionalGameInfo('w2', False),
        5714514: RegionalGameInfo('w2r', False),
        22323: RegionalGameInfo('w3', False),
        1464615513: RegionalGameInfo('wlby', False),
        5730135: RegionalGameInfo('wow', True)
    }
    TITLE_ID_MAP_CN = {
        **TITLE_ID_MAP,
        17459: RegionalGameInfo('d3cn', False)
    }
    BATTLENET_GAMES = [
        BlizzardGame('d3cn', '暗黑破壞神III', 'D3CN'),
        BlizzardGame('aqua', 'Avowed', 'AQUA'),
        BlizzardGame('rtro', 'Blizzard Arcade Collection', 'RTRO'),
        BlizzardGame('auks', 'Call of Duty®', 'AUKS'), # incl. Warzone, Black Ops 6 & 7
        BlizzardGame('viper', 'Call of Duty: Black Ops 4', 'VIPR'),
        BlizzardGame('zeus', 'Call of Duty: Black Ops Cold War', 'ZEUS'),
        BlizzardGame('odin', 'Call of Duty: Modern Warfare', 'ODIN'),
        BlizzardGame('nina', 'Call of Duty: Modern Warfare II (Standalone)', 'NINA'), # Missing ID in TITLE_ID_MAP
        BlizzardGame('pnta', 'Call of Duty: Modern Warfare III (Standalone)', 'PNTA'), # Missing ID in TITLE_ID_MAP
        BlizzardGame('lazarus', 'Call of Duty: MW2 Campaign Remastered', 'LAZR'),
        BlizzardGame('fore', 'Call of Duty: Vanguard', 'FORE'),
        BlizzardGame('wlby', 'Crash Bandicoot™ 4: It\'s About Time', 'WLBY'),
        BlizzardGame('drtl', 'Diablo®', 'DRTL'),
        BlizzardGame('anbs', 'Diablo® Immortal™', 'ANBS'),
        BlizzardGame('osi', 'Diablo® II: Resurrected', 'OSI'),
        BlizzardGame('diablo3', 'Diablo® III', 'D3'),
        BlizzardGame('fenris', 'Diablo® IV', 'Fen'),
        BlizzardGame('aris', 'DOOM: The Dark Ages', 'ARIS'),
        BlizzardGame('hs_beta', 'Hearthstone®', 'WTCG'),
        BlizzardGame('heroes', 'Heroes of the Storm', 'Hero'),
        BlizzardGame('prometheus', 'Overwatch® 2', 'Pro'),
        BlizzardGame('scor', 'Sea of Thieves', 'SCOR'),
        BlizzardGame('s1', 'StarCraft® Remastered', 'S1'),
        BlizzardGame('s2', 'StarCraft® II', 'S2'),
        BlizzardGame('ark', 'The Outer Worlds 2', 'ARK'),
        BlizzardGame('lbra', 'Tony Hawk\'s™ Pro Skater™ 3 + 4', 'LBRA'),
        BlizzardGame('w1', 'Warcraft: Orcs & Humans', 'W1'),
        BlizzardGame('w1r', 'Warcraft® I: Remastered', 'W1R'),
        BlizzardGame('w2', 'Warcraft II: Battle.net Edition', 'W2'),
        BlizzardGame('w2r', 'Warcraft® II: Remastered', 'W2R'),
        BlizzardGame('w3', 'Warcraft III: Reforged', 'W3'),
        BlizzardGame('gry', 'Warcraft Rumble', 'GRY'),
        BlizzardGame('wow', 'World of Warcraft®', 'WoW'),
        BlizzardGame('wow_classic', 'World of Warcraft Classic', 'WoW_wow_classic')
    ]
    CLASSIC_GAMES = [
        ClassicGame('d2', 'Diablo® II', 'Diablo II', 'Diablo II', 'DisplayIcon', "Diablo II.exe", "com.blizzard.diabloii"),
        ClassicGame('d2LOD', 'Diablo® II: Lord of Destruction®', 'Diablo II', 'Diablo II', 'DisplayIcon', "Diablo II.exe", "com.blizzard.diabloii"),
        ClassicGame('sca', 'StarCraft® Anthology', 'Starcraft', 'StarCraft', 'InstallLocation', 'StarCraft.exe', 'com.blizzard.starcraft'),
        ClassicGame('w3ROC', 'Warcraft® III: Reign of Chaos',  'Warcraft III', 'Warcraft III', 'InstallLocation', 'Warcraft III.exe', 'com.blizzard.WarcraftIII'),
        ClassicGame('w3tft', 'Warcraft® III: The Frozen Throne®',  'Warcraft III', 'Warcraft III', 'InstallLocation', 'Frozen Throne.exe', 'com.blizzard.WarcraftIII')
    ]

    def __init__(self):
        self._games = {game.uid: game for game in self.BATTLENET_GAMES + self.CLASSIC_GAMES}

    def __getitem__(self, key: str) -> BlizzardGame:
        """
        :param key: str uid (eg. "prometheus")
        :returns: game by `key`
        """
        return self._games[key]

    def game_by_title_id(self, title_id: int, cn: bool) -> BlizzardGame:
        """
        :param cn: flag if china game definitions should be search though
        :raises KeyError: when unknown title_id for given region
        """
        if cn:
            regional_info = self.TITLE_ID_MAP_CN[title_id]
        else:
            regional_info = self.TITLE_ID_MAP[title_id]
        return self[regional_info.uid]

    def try_for_free_games(self, cn: bool) -> List[BlizzardGame]:
        """
        :param cn: flag if china game definitions should be search though
        """
        return [
            self[info.uid] for info
            in (self.TITLE_ID_MAP_CN if cn else self.TITLE_ID_MAP).values()
            if info.try_for_free
        ]


Blizzard = _Blizzard()
