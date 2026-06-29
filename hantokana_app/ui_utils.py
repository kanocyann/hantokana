import os

from .storage_core import resource_path as storage_resource_path


def resolve_icon_path(parent, relative_path="icon.ico"):
    if parent and hasattr(parent, "resource_path"):
        try:
            return parent.resource_path(relative_path)
        except Exception:
            pass
    return storage_resource_path(relative_path, __file__)


def center_on_parent(widget, parent):
    if parent:
        widget.move(parent.frameGeometry().center() - widget.rect().center())


def icon_path_exists(parent, relative_path="icon.ico"):
    icon_path = resolve_icon_path(parent, relative_path)
    return icon_path, os.path.exists(icon_path)
