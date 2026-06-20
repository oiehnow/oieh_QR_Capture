"""화면 영역 선택 + 캡처 모듈.

반투명 전체화면 오버레이를 띄우고 마우스 드래그로 사각 영역을 선택하면
해당 영역을 mss로 캡처해 PIL.Image로 반환한다. ESC 또는 빈 선택은 취소(None).
"""
from __future__ import annotations

import tkinter as tk

import mss
from PIL import Image


class _RegionSelector:
    def __init__(self, root: tk.Misc):
        # 부모 root 위에 전체화면 오버레이 Toplevel을 띄운다.
        self.top = tk.Toplevel(root)
        self.top.attributes("-fullscreen", True)
        self.top.attributes("-alpha", 0.3)
        self.top.attributes("-topmost", True)
        self.top.configure(bg="black", cursor="cross")

        self.canvas = tk.Canvas(self.top, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.hint = self.canvas.create_text(
            self.top.winfo_screenwidth() // 2,
            40,
            text="QR 영역을 드래그하세요  (취소: ESC)",
            fill="white",
            font=("맑은 고딕", 16),
        )

        self.start_x = self.start_y = 0
        self.rect = None
        self.bbox: tuple[int, int, int, int] | None = None

        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.top.bind("<Escape>", self._on_cancel)

    def _on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.rect is not None:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline="#3b82f6", width=2,
        )

    def _on_drag(self, event):
        if self.rect is not None:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def _on_release(self, event):
        x1, x2 = sorted((self.start_x, event.x))
        y1, y2 = sorted((self.start_y, event.y))
        if x2 - x1 < 5 or y2 - y1 < 5:
            self.bbox = None  # 너무 작은 선택은 취소 처리
        else:
            # 오버레이 창의 화면상 위치를 더해 절대 좌표로 변환
            ox = self.top.winfo_rootx()
            oy = self.top.winfo_rooty()
            self.bbox = (x1 + ox, y1 + oy, x2 + ox, y2 + oy)
        self.top.destroy()

    def _on_cancel(self, _event):
        self.bbox = None
        self.top.destroy()


def select_region(root: tk.Misc) -> Image.Image | None:
    """드래그로 선택한 화면 영역을 캡처해 PIL.Image로 반환. 취소 시 None."""
    selector = _RegionSelector(root)
    root.wait_window(selector.top)

    bbox = selector.bbox
    if bbox is None:
        return None

    x1, y1, x2, y2 = bbox
    with mss.mss() as sct:
        monitor = {"left": x1, "top": y1, "width": x2 - x1, "height": y2 - y1}
        shot = sct.grab(monitor)
        return Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
