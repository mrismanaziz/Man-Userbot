import asyncio
import shlex
from base64 import b64decode
from typing import Tuple

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from userbot import LOGS, branch


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())


def git():
    UPSTREAM_REPO = b64decode(
        "aHR0cHM6Ly9naXRodWIuY29tL21yaXNtYW5heml6L01hbi1Vc2VyYm90"
    ).decode("utf-8")
    try:
        repo = Repo()
        LOGS.info("Git Client Found")
    except GitCommandError:
        LOGS.info("Invalid Git Command")
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "origin" in repo.remotes:
            origin = repo.remote("origin")
        else:
            origin = repo.create_remote("origin", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(
            branch,
            origin.refs[branch],
        )
        repo.heads[branch].set_tracking_branch(origin.refs[branch])
        repo.heads[branch].checkout(True)
        try:
            repo.create_remote("origin", UPSTREAM_REPO)
        except BaseException:
            pass
        nrs = repo.remote("origin")
        nrs.fetch(branch)
        try:
            nrs.pull(branch)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        install_req("pip3 install --no-cache-dir -r requirements.txt")
        LOGS.info("Fetched Updates from Man-Userbot")
