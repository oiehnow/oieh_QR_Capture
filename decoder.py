"""QR 디코딩 모듈.

OpenCV의 QRCodeDetector를 사용해 외부 DLL 의존 없이 QR을 읽는다.
"""
from __future__ import annotations

import cv2
import numpy as np


def _to_bgr(image) -> np.ndarray:
    """PIL.Image 또는 numpy 배열을 OpenCV용 BGR 배열로 변환."""
    if isinstance(image, np.ndarray):
        arr = image
    else:  # PIL.Image
        arr = np.array(image)

    if arr.ndim == 2:  # grayscale
        return cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
    if arr.shape[2] == 4:  # RGBA
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
    # mss/PIL은 RGB로 주므로 BGR로 변환
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def _try_decode(detector: "cv2.QRCodeDetector", bgr: np.ndarray) -> list[str]:
    """단일/다중 QR을 시도해 디코딩된 문자열 리스트를 반환."""
    results: list[str] = []

    # 다중 QR 먼저 시도
    try:
        ok, decoded, _points, _ = detector.detectAndDecodeMulti(bgr)
        if ok:
            results.extend(s for s in decoded if s)
    except cv2.error:
        pass

    if not results:
        text, _points, _ = detector.detectAndDecode(bgr)
        if text:
            results.append(text)

    return results


def decode_qr(image) -> str | None:
    """이미지에서 QR 코드를 읽어 문자열을 반환. 실패 시 None.

    인식률을 높이기 위해 원본 → 확대본 순으로 시도한다.
    여러 개가 인식되면 줄바꿈으로 합쳐서 반환한다.
    """
    detector = cv2.QRCodeDetector()
    bgr = _to_bgr(image)

    candidates = [bgr]
    # 작은 QR 대비 2배 확대본도 시도
    candidates.append(
        cv2.resize(bgr, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    )

    for candidate in candidates:
        results = _try_decode(detector, candidate)
        if results:
            # 중복 제거(순서 유지)
            seen: dict[str, None] = {}
            for r in results:
                seen.setdefault(r, None)
            return "\n".join(seen.keys())

    return None
