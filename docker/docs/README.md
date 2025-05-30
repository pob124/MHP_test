# Morning Hiking Partner 데이터베이스 설정

이 프로젝트는 데이터베이스 설정을 위해 Alembic 마이그레이션 시스템을 사용합니다.

## Docker 환경에서 실행

### 서비스 시작
```bash
# 모든 서비스 시작
docker-compose up -d

# 특정 서비스만 재시작
docker-compose restart web
```

### 서비스 접속
- **API 문서**: http://localhost/docs
- **WebSocket 테스트**: http://localhost/static/websocket_test.html
- **PgAdmin**: http://localhost/pgadmin/

## 🌐 외부 접근 설정 (다른 컴퓨터에서 접근)

### 1. 로컬 네트워크 내에서 접근

같은 Wi-Fi 네트워크에 있는 다른 컴퓨터에서 접근하려면:

1. **서버 컴퓨터의 IP 주소 확인**
   ```bash
   # Windows
   ipconfig
   
   # 예시 결과: 192.168.1.100
   ```

2. **Windows 방화벽 설정**
   - Windows 방화벽 → 고급 설정 → 인바운드 규칙 → 새 규칙
   - 포트 80 (HTTP) 허용

3. **프론트엔드에서 API 주소 변경**
   ```javascript
   // 기존: localhost
   const API_BASE_URL = 'http://192.168.1.100/api';
   
   // 환경변수로 관리 (권장)
   const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost/api';
   ```

4. **접속 테스트**
   - 다른 컴퓨터에서 `http://192.168.1.100/docs` 접속
   - API 문서가 정상적으로 로드되면 성공

### 2. 환경변수 설정

`docker/env.example` 파일을 참고하여 `.env` 파일 생성:

```bash
# docker/.env 파일 생성
cp env.example .env

# 필요에 따라 설정 수정
# HOST_IP=192.168.1.100  # 서버 IP
# CORS_ORIGINS=http://192.168.1.101:3000  # 프론트엔드 주소
```

### 3. 보안 고려사항

프로덕션 환경에서는 CORS 설정을 제한하는 것이 좋습니다:

```bash
# 특정 도메인만 허용
CORS_ORIGINS=http://192.168.1.101:3000,http://192.168.1.102:3000
ALLOWED_HOSTS=192.168.1.100,localhost
```

## 채팅 시스템 테스트

### 1. Firebase 토큰 발급
```bash
# PowerShell에서 실행 (프로젝트 루트에서)
.\get_firebase_token.ps1
```

### 2. REST API 테스트
1. http://localhost/docs 접속
2. "Authorize" 버튼 클릭
3. 발급받은 Firebase ID 토큰 입력
4. 채팅 관련 API 테스트:
   - `POST /api/chat/{room_id}`: 메시지 전송
   - `GET /api/chat/{room_id}`: 메시지 조회
   - `GET /api/chat/search`: 메시지 검색

### 3. WebSocket 테스트
1. http://localhost/static/websocket_test.html 접속
2. 채팅방 ID 입력 (예: test-room)
3. Firebase ID 토큰 입력
4. "연결" 버튼 클릭
5. "인증 메시지 전송" 버튼 클릭
6. Ping/Pong 및 활성 사용자 조회 테스트

### 4. 실시간 채팅 테스트
1. 두 개의 브라우저 탭에서 WebSocket 테스트 페이지 열기
2. 같은 채팅방 ID로 연결
3. 한 탭에서 REST API로 메시지 전송: `POST /api/chat/{room_id}`
4. 다른 탭에서 WebSocket으로 실시간 메시지 수신 확인

## 로그 확인
```bash
# 웹 서비스 로그 확인
docker-compose logs -f web

# 모든 서비스 로그 확인
docker-compose logs -f
```

## 데이터베이스 설정 방법

### 사전 요구사항

- PostgreSQL이 설치되어 있어야 합니다.
- Python과 필요한 패키지가 설치되어 있어야 합니다.

### 데이터베이스 마이그레이션 실행

프로젝트 루트 디렉토리에서 다음 명령을 실행합니다:

```bash
# 모든 마이그레이션을 적용
alembic upgrade head
```

이 명령은 통합 마이그레이션 파일(`alembic/versions/unified_migration.py`)을 사용하여 필요한 모든 테이블을 생성합니다.

### 데이터베이스 연결 설정

데이터베이스 연결 정보는 `alembic.ini` 파일에서 설정할 수 있습니다:

```
sqlalchemy.url = postgresql://postgres:your_password@localhost:5432/mhp_db
```

예시:
```
sqlalchemy.url = postgresql://postgres:your_password@localhost:5432/mhp_db
```

## 스키마 구조

마이그레이션은 다음 테이블을 생성합니다:

1. `users` - 사용자 정보를 저장하는 테이블
2. `chatrooms` - 채팅방 정보를 저장하는 테이블
3. `messages` - 채팅 메시지를 저장하는 테이블

모든 테이블은 API 문서의 스키마에 맞게 설계되었습니다. 