import os
import streamlit as st
from streamlit_img_label import st_img_label
from streamlit_img_label.manage import ImageManager, ImageDirManager

LABELS = ["yes", "no"]  # TODO: Set labels


def previous():
    st.session_state["image_index"] -= 1


def next():
    st.session_state["image_index"] += 1


def next_image():
    image_index = st.session_state["image_index"]
    if image_index < len(st.session_state["files"]) - 1:
        st.session_state["image_index"] += 1
    else:
        st.warning("This is the last image.")


def image_labeler(dir_path: str):
    dir_manager = ImageDirManager(dir_path)
    if "files" not in st.session_state:
        st.session_state["files"] = dir_manager.get_all_files()
        st.session_state["annotation_files"] = dir_manager.get_exist_annotation_files()
        st.session_state["image_index"] = 0
    else:
        dir_manager.set_all_files(st.session_state["files"])
        dir_manager.set_annotation_files(st.session_state["annotation_files"])

    def get_image() -> tuple[list, list, ImageManager]:
        img_file_name = dir_manager.get_image(st.session_state["image_index"])
        img_path = os.path.join(dir_path, img_file_name)
        manager = ImageManager(img_path)
        return manager.resizing_img(), manager.get_resized_rects(), manager

    col1, col2 = st.columns(2)
    with col2:
        cols = st.columns(3)
        cols[0].button("Previous", on_click=previous)
        cols[1].button("Save")
        cols[2].button("Next", on_click=next)

    image, pre_rects, manager = get_image()
    with col1:
        with st.container(width=700, height=700):
            rects = st_img_label(image, pre_rects)
    with col2:
        for i, (preview_image, label) in enumerate(manager.init_annotation(rects)):
            preview_image.thumbnail((200, 200))
            inner_col1, inner_col2 = st.columns(2)
            inner_col1.image(preview_image)
            inner_col2.selectbox(
                "Label", LABELS, index=label if label else 0, key=f"label_{i}"
            )
