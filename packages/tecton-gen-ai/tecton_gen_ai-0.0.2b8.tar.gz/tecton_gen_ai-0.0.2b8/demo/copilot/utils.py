import os
import re
from dataclasses import dataclass
from typing import Any
from tecton._internals.utils import cluster_url

# 7-bit C1 ANSI sequences
ANSI_ESCAPE = re.compile(
    r"""
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
""",
    re.VERBOSE,
)

_DIAGRAM_REGEX = re.compile(r"```tecton_diagram(.*?)```", re.DOTALL)
_DIAGRAM_PLACEHOLDER = "((tecton_diagram))"


_CODE_CONTAINER = None


def set_code_container(code_container):
    global _CODE_CONTAINER
    _CODE_CONTAINER = code_container


def get_code_container():
    return _CODE_CONTAINER


def get_cwd():
    # use python to get the current working directory
    import os

    return os.getcwd()


def run_command(command):
    import subprocess

    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = process.communicate()
    out = out.decode("utf-8") if out else ""
    out = ANSI_ESCAPE.sub("", out.replace("\n", "<|__newline__|>")).replace(
        "<|__newline__|>", "\n"
    )
    err = err.decode("utf-8") if err else ""
    err = ANSI_ESCAPE.sub("", err.replace("\n", "<|__newline__|>")).replace(
        "<|__newline__|>", "\n"
    )
    return process.returncode, out, err


def validate_syntax(path: str) -> None:
    code, out, err = run_command(f"python -m py_compile {path}")
    if code != 0:
        raise SyntaxError(str(err))


def is_in_feature_repo():
    return _is_feature_repo(get_cwd())


def _is_feature_repo(path: str) -> bool:
    import os

    path = os.path.join(path, ".tecton")
    return os.path.exists(path)


def _log(msg: str) -> str:
    from tecton_gen_ai.testing.log_utils import get_ui_logger

    logger = get_ui_logger()
    extra = {"copilot_flag": "log"}
    logger.info(msg, extra=extra)
    return msg

def _log_with_details(msg: str, details: str) -> str:
    from tecton_gen_ai.testing.log_utils import get_ui_logger

    logger = get_ui_logger()
    extra = {"copilot_flag": "log_with_details", "details": details}
    logger.info(msg, extra=extra)
    return msg

def _log_image(title: str, image_base64: str) -> str:
    from tecton_gen_ai.testing.log_utils import get_ui_logger

    logger = get_ui_logger()
    extra = {"copilot_flag": "image", "title": title, "image_base64": image_base64}
    logger.info("Rendering image", extra=extra)
    return title


def _success(msg: str) -> str:
    from tecton_gen_ai.testing.log_utils import get_ui_logger

    logger = get_ui_logger()
    extra = {"copilot_flag": "success"}
    logger.info(msg, extra=extra)
    return msg


def _err(_msg: Any, prefix: str = "Error") -> str:
    from tecton_gen_ai.testing.log_utils import get_ui_logger

    msg = str(_msg)

    logger = get_ui_logger()
    extra = {"copilot_flag": "error"}
    logger.error(msg, extra=extra)
    return prefix + ": " + msg


def _code():
    container = get_code_container()
    if container is not None:
        container.code(_get_source_code(), language="python")


@dataclass
class TectonAccountInfo:
    """Represents system information about the tecton account. Cluster is sometimes also referred to as account or endpoint."""

    rift_compute_supported: bool  # Whether Rift Compute is supported
    spark_compute_supported: bool  # Whether Spark Compute is supported
    caller_identity: str
    cluster_url: str

    def to_dict(self) -> dict:
        return {
            "rift_compute_supported": self.rift_compute_supported,
            "spark_compute_supported": self.spark_compute_supported,
            "caller_identity": self.caller_identity,
            "cluster_url": self.cluster_url,
        }


def get_current_tecton_account_info() -> dict:
    """
    Returns information about the currently logged in Tecton account.
    This information is important as it indicates what types of tecton capabilities are available or not supported.

    Returns:
        dict: A dictionary containing account information with the following keys:
            - rift_compute_supported (bool): Whether Rift Compute is supported
            - spark_compute_supported (bool): Whether Spark Streaming is supported
    """
    import tecton

    # Ensure we're logged into a cluster
    caller_identity = str(tecton.get_caller_identity())

    tecton.conf._force_initialize_mds_config()
    batch_compute_mode = tecton.conf._get("TECTON_BATCH_COMPUTE_MODE")
    print(tecton.conf._get("TECTON_BATCH_COMPUTE_MODE"))
    print(tecton.version.summary())

    rift_compute_supported = batch_compute_mode == "rift"
    spark_compute_supported = batch_compute_mode == "spark"

    return TectonAccountInfo(
        rift_compute_supported=rift_compute_supported,
        spark_compute_supported=spark_compute_supported,
        caller_identity=caller_identity,
        cluster_url= cluster_url(),
    ).to_dict()


def display(markdown_text, write_text_func, write_diagram_func):
    code_snippets = _DIAGRAM_REGEX.findall(markdown_text)
    # Replace all found code snippets with <>
    replaced_text = _DIAGRAM_REGEX.sub(_DIAGRAM_PLACEHOLDER, markdown_text)
    n = 0
    parts = replaced_text.split(_DIAGRAM_PLACEHOLDER)
    if len(parts) <= 1:
        write_text_func(markdown_text)
        return
    if parts[0]:
        write_text_func(parts[0])
    for part in parts[1:]:
        write_diagram_func(code_snippets[n])
        if part:
            write_text_func(part)
        n += 1


def _get_source_code() -> str:
    if not is_in_feature_repo():
        return ""

    path = os.path.join(get_cwd(), "features.py")
    if not os.path.exists(path):
        return ""
    else:
        with open(path, "r") as f:
            return f.read()
