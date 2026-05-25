# 가상화 개발 환경 구성

이 프로젝트는 Docker Compose와 VS Code Dev Containers를 기준으로 개발 환경을 격리합니다.

## 현재 상태

현재 Windows 환경에서 확인된 내용:

- Docker CLI: 설치되지 않음 또는 PATH 미등록
- Docker Compose: 설치되지 않음 또는 PATH 미등록
- WSL: 설치되지 않음

## 1. WSL2 설치

관리자 PowerShell에서 실행합니다.

```powershell
wsl --install
```

설치가 끝나면 Windows를 재시작합니다.

설치 확인:

```powershell
wsl --version
wsl --list --verbose
```

## 2. Docker Desktop 설치

winget을 사용할 수 있다면 관리자 PowerShell에서 실행합니다.

```powershell
winget install Docker.DockerDesktop
```

설치 후 Docker Desktop을 실행하고 다음 설정을 확인합니다.

- Settings > General > Use the WSL 2 based engine
- Settings > Resources > WSL Integration > 사용하는 Ubuntu 배포판 활성화

설치 확인:

```powershell
docker --version
docker compose version
```

## 3. 개발 컨테이너 빌드 및 실행

프로젝트 루트에서 실행합니다.

```powershell
docker compose up -d --build
```

컨테이너 접속:

```powershell
docker compose exec dev bash
```

컨테이너 안에서 확인:

```bash
java -version
mvn -v
node -v
npm -v
```

## 4. VS Code Dev Container로 열기

VS Code에서 `Dev Containers` 확장을 설치한 뒤 다음 명령을 실행합니다.

```text
Dev Containers: Reopen in Container
```

## 포트

- Spring Boot: `http://localhost:8080`
- Vue/Vite: `http://localhost:5173`
