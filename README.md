# Exit-Bridge

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
