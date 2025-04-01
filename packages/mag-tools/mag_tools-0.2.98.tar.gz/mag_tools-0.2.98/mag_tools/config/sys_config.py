import json
import os
from typing import Any, Dict, Optional

from bean.easy_map import EasyMap


class SysConfig:
    __instance = None

    def __init__(self, root_dir: Optional[str]):
        # 获取工程的根目录
        self.__root_dir = root_dir if root_dir else os.getcwd()

        # 读取配置文件
        self.config = self.__load_config()

    @classmethod
    def set_root_dir(cls, root_dir: str):
        cls.__instance = None
        cls.__get_instance(root_dir).__root_dir = root_dir

    @classmethod
    def root_dir(cls) -> str:
        return cls.__get_instance().__root_dir

    @classmethod
    def resource_dir(cls)->str:
        return os.path.join(cls.__get_instance().__root_dir, 'resources')

    @classmethod
    def data_dir(cls)->str:
        return os.path.join(cls.__get_instance().__root_dir, 'data')

    @classmethod
    def bin_dir(cls)->str:
        return os.path.join(cls.__get_instance().__root_dir, 'bin')

    @classmethod
    def logging_conf(cls)->str:
        return os.path.join(cls.__get_instance().__root_dir, 'resources', 'config', 'logging.conf')

    @classmethod
    def get(cls, key: str, default=None)->Any:
        return cls.__get_instance().config.get(key, default)

    @classmethod
    def get_datasources(cls) -> Dict[str, Dict[str, Any]]:
        return cls.__get_instance().config.get("datasources")

    @classmethod
    def get_datasource(cls, datasource_name : str) -> Dict[str, Any]:
        datasources = cls.__get_instance().config.get("datasources")
        return datasources.get(datasource_name, None)

    @classmethod
    def get_user_dir(cls, *args: str) -> Optional[str]:
        return os.path.join(cls.__get_instance().__root_dir, 'data', *args)

    @classmethod
    def get_com_info(cls):
        config = cls.__get_instance().config
        info = {
            "host": config.get("host"),
            "port": config.get("port", 80),
            "ssl": config.get("ssl", False),
            "clientType": config.get("clientType", "Windows"),
            "userType": config.get("userType", "Person"),
            "appId": config.get("appId", ""),
            "Content-Type": config.get("Content-Type", "application/json")
        }
        return info

    @classmethod
    def __get_instance(cls, root_dir: Optional[str] = None):
        if not cls.__instance:
            cls.__instance = cls(root_dir)
        return cls.__instance

    def __load_config(self)->Dict[str, Any]:
        config_file = os.path.join(self.__root_dir, 'resources', 'config', 'sys_config.json')

        if not os.path.exists(config_file):
            raise FileNotFoundError(f"配置文件 {config_file} 不存在")

        with open(config_file, 'r', encoding='utf-8') as file:
            config = json.load(file)
        return config
