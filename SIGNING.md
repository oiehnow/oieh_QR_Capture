# 코드 서명 (SignPath Foundation, 무료)

오픈소스 프로젝트는 [SignPath Foundation](https://signpath.org/)을 통해 **무료 코드 서명**을 받을 수 있습니다.
서명이 붙으면 Windows Defender / SmartScreen 경고와 백신 오탐이 크게 줄어듭니다.

## 신청 절차

1. **OSS 라이선스** — 이미 `LICENSE`(MIT) 추가됨 ✓
2. **CI 빌드** — 이미 `.github/workflows/build.yml` 추가됨 ✓ (SignPath은 CI 빌드 산출물만 서명)
3. **SignPath 가입 & 신청**
   - https://app.signpath.io 가입 (GitHub 계정 연동)
   - Foundation 프로그램에 이 저장소(`oiehnow/oieh_QR_Capture`)로 신청
   - 사람 심사 → 보통 수일~수주 소요
4. **승인 후 설정**
   - SignPath에서 발급한 **API 토큰**을 저장소 `Settings > Secrets and variables > Actions`에
     `SIGNPATH_API_TOKEN` 이름으로 등록
   - `.github/workflows/build.yml`의 `organization-id` / `project-slug` /
     `signing-policy-slug` / `artifact-configuration-slug` 값을 SignPath 콘솔 값으로 교체
5. **태그 푸시** — `git tag v1.0.4 && git push origin v1.0.4` 하면 CI가 빌드→서명→릴리스를 자동 처리

> 시크릿이 없으면 서명 단계는 자동으로 건너뛰므로, 승인 전에도 워크플로 빌드/릴리스는 정상 동작합니다.
