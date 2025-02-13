from abc import ABC, abstractmethod
from enum import Enum
import re


class CONFIG_ADDONS(Enum):
    UPDATER = "updater"
    VALIDATOR = "validator"
    TEMPLATE = "template"


# Constants for addon signs
VALIDATOR_SIGN = "!"
UPDATER_SIGN = "&"
TEMPLATE_SIGN = "#"

# Pattern to match addon annotations
_ADDON_PATTERN = rf"@(\w+)\(([^)]+)\)|([{VALIDATOR_SIGN}{UPDATER_SIGN}{TEMPLATE_SIGN}])(\w+)"


def process_addons(key: str):
    """
    Extracts addons and their arguments from the key.
    Removes all addon annotations from the key and returns the cleaned key.
    
    :param key: The input key string with addon annotations.
    :return: A tuple of cleaned key and a list of extracted addons.
    """
    matches = re.findall(_ADDON_PATTERN, key)
    addons = []
    
    for match in matches:
        if match[0]:
            addons.append((match[0], match[1]))
        elif match[2] == VALIDATOR_SIGN:  
            addons.append((CONFIG_ADDONS.VALIDATOR.value, match[3]))
        elif match[2] == UPDATER_SIGN:  
            addons.append((CONFIG_ADDONS.UPDATER.value, match[3]))
        elif match[2] == TEMPLATE_SIGN:  
            addons.append((CONFIG_ADDONS.TEMPLATE.value, match[3]))

    key = re.sub(_ADDON_PATTERN, "", key).strip()
    return key, addons


class UnsupportedAddonError(Exception):
    """Exception raised when an unsupported addon is used"""


class Addon(ABC):
    """Base class for config validators"""

    __registry = None
    NAME = None

    def __init_subclass__(cls: "Addon", **kwargs):
        if cls.__registry is None:
            cls.__registry = {}

        if cls.NAME in cls.__registry:
            raise ValueError(f"Addon with name '{cls.NAME}' already exists.")

        cls.__registry[cls.NAME] = cls
        super().__init_subclass__(**kwargs)

    @classmethod
    def get_addon(cls, name: str) -> "Addon":
        if name not in cls.__registry:
            raise UnsupportedAddonError(
                f"Addon {cls.NAME} with name '{name}' not found."
            )
        return cls.__registry[name]


class TemplateAddon(Addon):
    """Template addon for config values to be used for predefined templates"""

    NAME = "template"

    @classmethod
    def data(cls):
        dat = {"*object": cls._get_object_ref()}
        dat.update(cls._data())
        return dat
    
    @classmethod
    def _get_object_ref(cls):
        return f"{cls.__module__}.{cls.__name__}"

    @classmethod
    def _data(cls):
        """Data to be used for template"""


class ValidatorAddon(Addon):
    """Validator addon for config values to be used to validate data"""

    NAME = "validator"

    @classmethod
    def validate(cls, value):
        """Validate the value"""


class UpdaterAddon(Addon):
    """Replace addon for config values to be used to replace or merge data"""

    NAME = "updater"

    @classmethod
    def update(cls, a, b):
        """Update a with b"""


_ADDONS = {
    CONFIG_ADDONS.UPDATER: UpdaterAddon,
    CONFIG_ADDONS.VALIDATOR: ValidatorAddon,
    CONFIG_ADDONS.TEMPLATE: TemplateAddon,
}


def select_addon(addon: str, name: str) -> Addon:
    try:
        _addon: Addon = _ADDONS[CONFIG_ADDONS(addon)]
    except ValueError:
        raise UnsupportedAddonError(f"Addon {addon} not found.")
    return _addon.get_addon(name)
