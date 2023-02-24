import importlib
import pkgutil
from typing import Iterable

from src.bot.core.logging import get_logger

logger = get_logger(__name__)


REQUIREMENT_SEPARATOR = "::"


class PackagesLoader:
    def __init__(self, *, debug: bool = False):
        self._debug = debug

        self.modules = {}

    def load_package(self, package: str, recursive: bool = True):
        """
        Import all submodules of a module, recursively, including subpackages

        :param package: package (name or actual module)
        :type package: str | module
        :param recursive: recursive import
        :type recursive: :obj:`bool`
        :rtype: dict[str, types.ModuleType]
        """
        if isinstance(package, str):
            package = importlib.import_module(package)

        full_name = package.__name__
        results = {full_name: package}

        if self._debug:
            logger.debug("Root package <%s> loaded", full_name)

        for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + "." + name
            module = self.modules[full_name] = results[
                full_name
            ] = importlib.import_module(full_name)
            if self._debug:
                logger.debug("Sub package <%s> loaded", full_name)

            if hasattr(module, "includeme") and callable(module.includeme):
                module.includeme()

            if recursive and is_pkg:
                results.update(self.load_package(full_name))
        return results

    def load_packages(self, packages: Iterable[str], recursive=True):
        """
        Load list of the packages

        :param packages:
        :param recursive:
        :return:
        """
        result = []
        for package in packages:
            result.append(self.load_package(package, recursive))
        return result
