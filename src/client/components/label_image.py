import os
import streamlit as st
from streamlit_img_label import st_img_label
from streamlit_img_label.manage import (
    ImageManager,
    ImageDirManager,
)
from PIL import Image

LABELS = ["plant", "not a plant", "tree", "beer"]  # TODO: Set labels


def rect_to_txt(rect: dict[str, float | str]) -> str:
    x_center = rect["left"]
    y_center = rect["top"]
    if rect["label"] not in LABELS:
        raise ValueError(f"{rect['label']=} not in {LABELS=}")
    return f"{LABELS.index(rect['label'])} {x_center} {y_center} {rect['width']} {rect['height']}\n"


class CustomImageManager(ImageManager):
    def __init__(self, filename):
        """initiate module"""
        self._filename = filename
        _dir, image_file_name = list(os.path.split(filename))
        dir_path, _ = os.path.split(_dir)
        image_file_name: str
        image_file_name, _ = image_file_name.rsplit(".", maxsplit=1)
        image_file_name += ".txt"
        self._label_filename = os.path.join(dir_path, "labels", image_file_name)
        self._img = Image.open(filename)
        self._rects = []
        self._load_rects()
        self._resized_ratio_w = 1
        self._resized_ratio_h = 1

    def _load_rects(self):
        if not os.path.exists(self._label_filename):
            rects = []
        else:
            with open(self._label_filename, "r", encoding="utf-8") as f:
                rects = [
                    {
                        "label": LABELS[int(label)],
                        "top": float(y_center),
                        "left": float(x_center),
                        "width": float(width),
                        "height": float(height),
                    }
                    for label, x_center, y_center, width, height in map(
                        str.split, f.readlines()
                    )
                ]
        if rects:
            self._rects = rects

    def save_annotation(self):
        with open(self._label_filename, "w", encoding="utf-8") as f:
            f.writelines(map(rect_to_txt, self._current_rects))


class Labeller:
    def __init__(self, dir_path: str):
        self.dir_path = dir_path
        self.dir_manager = ImageDirManager(os.path.join(dir_path, "images"))

        self.image_index = 0
        self.files = self.dir_manager.get_all_files()
        self.num_images = len(self.files)

    def previous(self):
        self.image_index -= 1
        self.image_index %= self.num_images

    def next(self):
        self.image_index += 1
        self.image_index %= self.num_images

    def get_image(self) -> tuple[Image.Image, list, CustomImageManager]:
        img_file_name = self.dir_manager.get_image(self.image_index)
        img_path = os.path.join(self.dir_path, "images", img_file_name)
        manager = CustomImageManager(img_path)
        return manager.resizing_img(), manager.get_resized_rects(), manager


def next_image():
    image_index = st.session_state["image_index"]
    if image_index < len(st.session_state["files"]) - 1:
        st.session_state["image_index"] += 1
    else:
        st.warning("This is the last image.")


def image_labeler(dir_path: str):
    if "labeller" not in st.session_state:
        st.session_state["labeller"] = Labeller(dir_path)
    labeller: Labeller = st.session_state["labeller"]

    col1, col2 = st.columns(2)
    with col2:
        cols = st.columns(3)
        cols[0].button("Previous", on_click=labeller.previous)
        cols[2].button("Next", on_click=labeller.next)

    image, pre_rects, image_manager = labeller.get_image()

    cols[1].button("Save", on_click=image_manager.save_annotation)
    with col1:
        with st.container(width=700, height=700):
            rects = st_img_label(image, box_color="red", rects=pre_rects)

    with col2:
        for i, (preview_image, label) in enumerate(
            image_manager.init_annotation(rects)
        ):
            preview_image.thumbnail((200, 200))
            inner_col1, inner_col2 = st.columns(2)
            inner_col1.image(preview_image)
            image_manager.set_annotation(
                i,
                inner_col2.selectbox(
                    "Label",
                    LABELS,
                    index=LABELS.index(label) if label else 0,
                    key=f"label_{i}",
                ),
            )
