"""Prepare and launch the pinned LLMD baseline on an assigned Linux AMD GPU host.

Development launcher only; does not implement hardened grading isolation or certify MI355X.
"""

import argparse
import json
import os
import re
import shlex
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOCK = ROOT / "baseline/lock.json"
MARKER = ".abstract-model.json"


def load_lock(path: Path = DEFAULT_LOCK) -> dict[str, Any]:
    lock = json.loads(path.read_text())
    if not re.fullmatch(r"[^\s]+@sha256:[0-9a-f]{64}", lock["image"]):
        raise ValueError("baseline image must be pinned by SHA-256 digest")
    if lock["platform"] != "linux/amd64":
        raise ValueError("baseline must target linux/amd64")
    for model in lock["models"].values():
        if not re.fullmatch(r"[0-9a-f]{40}", model["revision"]):
            raise ValueError("model revisions must be pinned full commits")
    return lock


def run_command(command: list[str], *, dry_run: bool) -> None:
    print(shlex.join(command), flush=True)
    if not dry_run:
        subprocess.run(command, check=True)


def build_command(lock: dict[str, Any], image: str) -> list[str]:
    return [
        "docker", "build", "--platform", lock["platform"],
        "--build-arg", "BASE_IMAGE=" + lock["image"],
        "-f", str(ROOT / "baseline/Dockerfile"), "-t", image, str(ROOT),
    ]


def start_command(
    lock: dict[str, Any],
    model_dir: Path,
    render_device: str,
    image: str,
    name: str,
    port: int,
    *,
    render_gid: int | None = None,
) -> list[str]:
    resolved = model_dir.resolve()
    if "," in str(resolved):
        raise ValueError("Docker bind mount paths cannot contain commas")
    if not re.fullmatch(r"/dev/dri/renderD[0-9]+", render_device):
        raise ValueError("render device must be /dev/dri/renderD<number>")
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    command = [
        "docker", "run", "--detach", "--name", name, "--platform", lock["platform"],
        "--device", "/dev/kfd", "--device", render_device,
        "--security-opt", "no-new-privileges", "--shm-size", "16g",
        "--cpus", "16", "--memory", "128g", "--env", "ROCR_VISIBLE_DEVICES=0",
        "--publish", f"127.0.0.1:{port}:8000",
        "--mount", f"type=bind,src={resolved},dst=/models/model,readonly",
    ]
    if render_gid is not None:
        command.extend(["--group-add", str(render_gid)])
    return command + [image, *lock["default_args"], "--model=/models/model"]


def prepare(args: argparse.Namespace, lock: dict[str, Any]) -> None:
    model = lock["models"][args.model]
    directory = args.model_dir.resolve()
    marker = directory / MARKER
    if marker.exists():
        previous = json.loads(marker.read_text())
        if any(previous.get(key) != model[key] for key in ("repository", "revision")):
            raise ValueError("model directory already belongs to another snapshot; use a new path")
    elif directory.exists() and any(directory.iterdir()):
        raise ValueError("refusing to mix a pinned snapshot into a nonempty unmarked directory")
    run_command(
        ["docker", "pull", "--platform", lock["platform"], lock["image"]], dry_run=args.dry_run
    )
    print(f"snapshot: {model['repository']}@{model['revision']} -> {directory}", flush=True)
    if not args.dry_run:
        from huggingface_hub import snapshot_download

        directory.mkdir(parents=True, exist_ok=True)
        marker.write_text(json.dumps({**model, "status": "preparing"}, indent=2) + "\n")
        # local_dir materializes files; avoid exposing HF-cache symlink paths to LLMD.
        snapshot_download(
            repo_id=model["repository"], revision=model["revision"], local_dir=directory
        )
        if not (directory / "config.json").is_file():
            raise ValueError("download did not produce a model config")
        marker.write_text(json.dumps({**model, "status": "complete"}, indent=2) + "\n")
    run_command(build_command(lock, args.image), dry_run=args.dry_run)


def validate_model_dir(directory: Path, lock: dict[str, Any]) -> None:
    if not (directory / "config.json").is_file():
        raise ValueError("model config not found; run prepare first")
    marker = json.loads((directory / MARKER).read_text())
    if marker.get("status") != "complete":
        raise ValueError("snapshot preparation is incomplete")
    if not any(
        all(marker.get(key) == model[key] for key in ("repository", "revision"))
        for model in lock["models"].values()
    ):
        raise ValueError("prepared snapshot does not match the baseline lock")
    # This marker is setup bookkeeping, not a grading integrity/checksum certificate.


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    commands = parser.add_subparsers(dest="action", required=True)
    prep = commands.add_parser("prepare", help="pull image, download pinned weights, build wrapper")
    start = commands.add_parser("start", help="launch baseline; use smoke to check readiness")
    stop = commands.add_parser("stop", help="stop and remove only the named baseline container")
    for command in (prep, start, stop):
        command.add_argument("--dry-run", action="store_true")
    for command in (prep, start):
        command.add_argument("--model-dir", type=Path, required=True)
        command.add_argument("--image", default="abstract-llmd-baseline:local")
    for command in (start, stop):
        command.add_argument("--name", default="abstract-baseline")
    prep.add_argument("--model", choices=("smoke", "target"), default="smoke")
    start.add_argument("--render-device", default="/dev/dri/renderD128")
    start.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    try:
        lock = load_lock(args.lock)
        if args.action == "prepare":
            prepare(args, lock)
        elif args.action == "start":
            gid = None
            if not args.dry_run:
                if not sys.platform.startswith("linux"):
                    raise ValueError("the serving baseline requires a Linux AMD GPU host")
                validate_model_dir(args.model_dir, lock)
                for path in ("/dev/kfd", args.render_device):
                    device = os.stat(path)
                    if not stat.S_ISCHR(device.st_mode):
                        raise ValueError(f"not a GPU character device: {path}")
                gid = device.st_gid
            run_command(
                start_command(
                    lock,
                    args.model_dir,
                    args.render_device,
                    args.image,
                    args.name,
                    args.port,
                    render_gid=gid,
                ),
                dry_run=args.dry_run,
            )
        else:
            run_command(["docker", "stop", "--time", "30", args.name], dry_run=args.dry_run)
            run_command(["docker", "rm", args.name], dry_run=args.dry_run)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"baseline: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
