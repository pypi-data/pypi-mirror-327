from __future__ import annotations

import abc
import asyncio
import logging
import pathlib
from typing import Any

from ks_session_manager.types import SessionData
from ks_session_manager.types import SessionMetadata


async def _read_2fa(file_path: str | pathlib.Path) -> str | None:
    file_path = pathlib.Path(file_path)
    two_fa_file_names = [
        'pass', 'pass.txt',
        'password', 'password.txt',
        '2FA', '2FA.txt',
        '2fa', '2fa.txt',
        'Password2FA', 'Password2FA.txt',
        'twoFA', 'twoFA.txt',
        'twofa', 'twofa.txt',
    ]
    two_fa_file = next((
        file_path.with_name(file_name)
        for file_name in two_fa_file_names
        if file_path.with_name(file_name).exists()
    ), None)

    if two_fa_file:
        return await asyncio.to_thread(two_fa_file.read_text, encoding='utf-8', errors=None)

    return None


class BaseSessionFileManager(abc.ABC):
    def __init__(self, session_name: str, *, workdir: str | pathlib.Path | None = None):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.session_name = session_name
        self.workdir = pathlib.Path(workdir).absolute() if workdir is not None else pathlib.Path.cwd().absolute()

    @property
    @abc.abstractmethod
    def session_file_extension(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def read_session_storage(self) -> SessionData:
        raise NotImplementedError

    @abc.abstractmethod
    async def write_session_storage(
            self,
            session_data: SessionData,
            *,
            in_memory: bool = False,
            exist_ok: bool = False
    ) -> Any:
        raise NotImplementedError

    @property
    def session_path(self) -> pathlib.Path:
        return (self.workdir / self.session_name).with_suffix(self.session_file_extension).absolute()

    @property
    def session_json_metadata_path(self) -> pathlib.Path:
        return self.session_path.with_suffix('.json').absolute()

    async def read_session_metadata(self) -> SessionMetadata:
        if not self.session_json_metadata_path.exists():
            raise FileNotFoundError(f"Session metadata file not found in {self.session_json_metadata_path}")

        if not self.session_json_metadata_path.is_file():
            raise IsADirectoryError(
                f"Session metadata file path "
                f"{self.session_json_metadata_path} points to a directory"
            )

        # noinspection PyTypeChecker
        metadata_json = await asyncio.to_thread(self.session_json_metadata_path.read_text, encoding='utf-8')
        session_metadata = SessionMetadata.model_validate_json(metadata_json)

        if not bool(session_metadata.two_factor_password):
            session_metadata.two_factor_password = await _read_2fa(self.session_json_metadata_path)

        return session_metadata

    async def write_session_metadata(self, session_metadata: SessionMetadata):
        session_metadata_file_path = self.session_json_metadata_path

        if session_metadata_file_path.exists():
            raise FileExistsError(f"Metadata JSON file is already exists in {session_metadata_file_path}")

        metadata_json = session_metadata.model_dump_json(indent=4, by_alias=True)
        # noinspection PyTypeChecker
        await asyncio.to_thread(session_metadata_file_path.write_text, metadata_json, encoding='utf-8')

    async def delete_session(self, *, i_accept_possible_lost_of_data: bool = False):
        if not i_accept_possible_lost_of_data:
            self.logger.warning(
                "You are about to delete session. Pass i_accept_possible_lost_of_data=True to remove session"
            )
            return

        self.session_path.unlink(missing_ok=True)
        self.session_json_metadata_path.unlink(missing_ok=True)
