# oieh QR reader

화면에서 마우스로 영역을 드래그해 캡처하고, 그 안의 **QR 코드를 읽어주는** Windows 데스크톱 프로그램입니다.

![UI](초안UI%20디자인.png)

## 기능
- "+ 다시 캡처" 버튼 → 반투명 전체화면 오버레이에서 마우스로 영역 드래그
- 선택 영역을 캡처해 QR 코드 자동 디코딩
- 결과 텍스트 표시 + **복사 버튼**으로 클립보드 복사
- 멀티모니터 / 고DPI 지원, 외부 DLL 불필요(OpenCV 디코더)

## 실행 (개발자용)
```bash
pip install -r requirements.txt
python main.py
```

## 원클릭 EXE 빌드
`build.bat` 을 더블클릭하면 의존성 설치 후 단일 실행파일이 만들어집니다.

```bash
build.bat
```

빌드 결과: `dist\oieh QR reader.exe` (의존성 없이 단독 실행)

## 기술 스택
- GUI: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- 화면 캡처: [mss](https://github.com/BoboTiG/python-mss)
- QR 디코딩: OpenCV `QRCodeDetector`
- 패키징: PyInstaller

## 파일 구조
| 파일 | 역할 |
|------|------|
| `main.py` | 메인 창 UI + 앱 진입점 |
| `capture.py` | 화면 영역 드래그 선택 및 캡처 |
| `decoder.py` | 이미지에서 QR 디코딩 |
| `build.bat` | 원클릭 EXE 빌드 |
