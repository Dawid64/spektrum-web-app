from collections.abc import Callable
import logging
import os
from typing import Literal
import yaml
import streamlit_authenticator as stauth
import streamlit as st

with open(os.path.join(".secrets", "config.yaml")) as file:
    _config = yaml.load(file, Loader=yaml.SafeLoader)

RANKS = Literal["admin", "maintainer", "user"]

AUTHENTICATOR = stauth.Authenticate(
    _config["credentials"],
    _config["cookie"]["name"],
    _config["cookie"]["key"],
    _config["cookie"]["expiry_days"],
)


def after_login(func: Callable[[], None], required_role: RANKS):
    roles = get_login_widget()
    if roles is None:
        st.write("You need to log in to continue, you can log in in sidebar.")
    elif required_role in roles:
        func()
    else:
        st.warning("You have not enough permissions.")


def get_login_widget() -> None | list[RANKS]:
    def callback():
        st.snow()

    if not st.session_state.get("authentication_status"):
        try:
            AUTHENTICATOR.login(location="sidebar", callback=lambda x: st.rerun())
        except Exception as e:
            st.error(e)

    if st.session_state.get("authentication_status"):
        st.sidebar.button(
            f"Welcome {st.session_state['name']}",
            key="disabled-name",
            on_click=callback,
        )
        AUTHENTICATOR.logout(location="sidebar")
    elif st.session_state.get("authentication_status") is False:
        st.sidebar.error("Username/password is incorrect")
    elif st.session_state.get("authentication_status") is None:
        st.sidebar.warning("Please enter your username and password")

    return st.session_state.get("roles")


class CustomFormatter(logging.Formatter):
    cyan = "\x1b[96m"
    grey = "\x1b[30;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    text_format = "%(asctime)s - %(name)s [%(levelname)s]: %(message)s"

    FORMATS = {
        logging.DEBUG: cyan + text_format + reset,
        logging.INFO: grey + text_format + reset,
        logging.WARNING: yellow + text_format + reset,
        logging.ERROR: red + text_format + reset,
        logging.CRITICAL: bold_red + text_format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(CustomFormatter())
        logger.addHandler(ch)
    logger.propagate = False
    return logger
