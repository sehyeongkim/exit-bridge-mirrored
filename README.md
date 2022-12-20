# Exit-Bridge
### 프로젝트 설명
투자조합 매칭 플랫폼. GP(General Partner)와 LP(Limited Partner)를 매칭해주고, GP가 조합을 운용하면서 필요했던 관리들을 한 곳에서 모아서 관리할 수 있도록 합니다.

### 서버 실행방법
1. 프로젝트 최상단에 dev.env.sample 내용 참고하여 dev.env config 파일 신규 작성
2. `/app` 디렉토리의 `start.sh` 쉘 스크립트 실행 (파일 실행권한 필요할 수도 있음 chmod 755)
3. `start.sh` 설정 
- ENV: 현재 개발환경
- log-config: 로그 형식 yaml 파일으로 설정
- host: 서버 호스트
- port: 서버 포트
- workers: fastapi app 프로세스 개수

### 프로젝트 구조

- Transaction Script Pattern
- Async SQLAlchemy session
- Top-level Dependency


### 라이브러리

- fastapi v0.78
- pydantic v1.9.1
- SQLAlchemy v1.4.37
- starlette v0.19.1
