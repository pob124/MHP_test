# FastAPI Firebase Authentication 프로젝트

FastAPI와 Firebase Authentication을 사용한 인증 시스템 구현 프로젝트입니다.

## 최근 업데이트 및 새로운 기능 (2023.09)

- **사용자 프로필 기능 추가**: 사용자 모델에 프로필 관련 필드 추가 (프로필 사진, 자기소개, 전화번호 등)
- **로그인 정보 추적 기능**: 마지막 로그인 시간 및 IP 추적 기능 구현
- **통합 프로필 정보 API**: `/api/users/me` 엔드포인트를 통한 사용자 프로필 정보 조회 기능
- **데이터베이스 마이그레이션 개선**: Alembic을 통한 자동 마이그레이션 스크립트 생성
- **프론트엔드 디버깅 개선**: 프론트엔드에서 API 호출 디버깅을 위한 상세 로깅 추가
- **CORS 설정 최적화**: 클라이언트-서버 간 안전한 통신을 위한 CORS 설정 개선
- **인증 로직 통합**: 인증 관련 코드를 API와 분리하여 재사용성 향상
- **템플릿 엔진 활용**: FastAPI의 Jinja2 템플릿 엔진을 활용한 HTML 서빙

## 주요 기능

- Firebase 기반 이메일/비밀번호 인증
- Google 소셜 로그인
- 보호된 API 엔드포인트
- JWT 토큰 기반 인증
- Docker 컨테이너화
- PostgreSQL 데이터베이스 연동

## 프로젝트 구조

```
project/
├── app/                    # 메인 애플리케이션 코드
│   ├── api/                # API 엔드포인트
│   ├── auth/               # 인증 관련 코드
│   ├── core/               # 핵심 설정 및 유틸리티
│   │   ├── config.py      # 앱 설정
│   │   ├── firebase.py    # Firebase 초기화
│   ├── models/             # 데이터 모델
│   ├── tests/              # 테스트 코드
│   └── main.py             # 앱 진입점
├── docker/                 # Docker 관련 파일
│   ├── Dockerfile          # 도커 이미지 정의
│   ├── docker-compose.yml  # Docker Compose 설정
│   └── firebase-adminsdk.json  # Firebase 서비스 계정 키
├── static/                 # 정적 파일 (CSS, JS)
│   └── css/
│       └── styles.css      # 스타일시트
├── templates/              # HTML 템플릿
│   └── index.html          # 로그인 테스트 페이지
├── requirements.txt        # Python 의존성
└── README.md               # 이 파일
```

## 시작하기

### 필수 조건

- Python 3.8+
- Docker와 Docker Compose
- Firebase 프로젝트

### Firebase 설정

1. [Firebase 콘솔](https://console.firebase.google.com)에서 새 프로젝트 생성
2. Authentication 서비스 활성화
   - 이메일/비밀번호 로그인 방식 활성화
   - 구글 로그인 방식 활성화
3. 웹 애플리케이션 등록
   - 제공된 Firebase 설정(apiKey, projectId 등)을 `templates/index.html` 파일의 `firebaseConfig` 객체에 복사
4. 서비스 계정 키 발급
   - 프로젝트 설정 > 서비스 계정 > Firebase Admin SDK > 새 비공개 키 생성
   - 다운로드된 JSON 파일을 `docker/firebase-adminsdk.json`로 저장

### PostgreSQL 데이터베이스 설정

현재 PostgreSQL 데이터베이스는 다음과 같이 설정되어 있습니다:
- **사용자**: hch3154
- **비밀번호**: admin
- **데이터베이스 이름**: mhp_db
- **포트**: 5432

### PGAdmin 접속 방법

1. 브라우저에서 다음 URL로 접속:
   ```
   http://localhost:5050
   ```

2. 다음 자격 증명으로 로그인:
   - 이메일: hch3154@gmail.com
   - 비밀번호: admin

3. 서버 등록하기:
   - "Servers" > 마우스 오른쪽 버튼 클릭 > "Create" > "Server..."
   - "General" 탭:
     - Name: MHP_DB (또는 원하는 이름)
   - "Connection" 탭:
     - Host name/address: localhost (또는 Docker 네트워크의 컨테이너 IP 주소)
     - Port: 5432
     - Maintenance database: mhp_db
     - Username: hch3154
     - Password: admin

4. PGAdmin을 통해 데이터베이스 스키마 및 데이터 관리가 가능합니다.

### 설치 및 실행

#### Docker 환경에서 실행 (권장)

1. 저장소 클론
   ```bash
   git clone [repository-url]
   cd [project-directory]
   ```

2. Firebase 설정 준비
   - Firebase 서비스 계정 키를 `docker/firebase-adminsdk.json`에 저장
   - `templates/index.html` 파일의 `firebaseConfig` 객체를 실제 Firebase 프로젝트 설정으로 업데이트

3. Docker Compose로 빌드 및 실행
   ```bash
   cd docker
   docker-compose build web
   docker-compose up
   ```

4. 브라우저에서 접속
   - API 서버: http://localhost:9090
   - PGAdmin: http://localhost:5050
   - API 문서: http://localhost:9090/docs

5. 데이터베이스 마이그레이션 실행
   ```bash
   # 새 터미널에서 실행
   docker-compose exec web alembic upgrade head
   ```

6. 로그 확인 (문제 해결)
   ```bash
   # 실시간 로그 확인
   docker-compose logs -f web
   ```

6. 컨테이너 종료
   ```bash
   # Ctrl+C로 종료 또는 다른 터미널에서
   docker-compose down
   docker-compose up
   ```

#### 로컬 개발 환경

1. 가상환경 생성 및 활성화
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```

3. 환경 변수 설정
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=docker/firebase-adminsdk.json
   ```

4. 앱 실행
   ```bash
   uvicorn app.main:app --reload
   ```

## 테스트

### Docker로 테스트 실행
```bash
cd docker
docker-compose build test
docker-compose up test
```

### 로컬에서 테스트 실행
```bash
pytest -v app/tests
```

## 구글 로그인 테스트

### Docker 환경에서 구글 로그인 테스트

1. Firebase 콘솔에서 필수 설정 확인
   - Authentication > Sign-in method > Google 로그인이 활성화되어 있는지 확인
   - Authentication > Settings > Authorized domains에 "localhost"가 추가되어 있는지 확인

2. Docker 컨테이너 실행
   ```bash
   cd docker
   docker-compose up web
   ```

3. 브라우저에서 테스트
   - http://localhost:9090 접속
   - "Google로 로그인" 버튼 클릭
   - 구글 계정으로 로그인
   - 로그인 성공 시 사용자 정보 표시
   - "보호된 API 호출" 버튼으로 인증된 API 요청 테스트

4. 문제 해결
   - Firebase 초기화 문제: Docker 로그 확인 (`docker-compose logs -f web`)
   - 브라우저 콘솔(F12) 확인으로 클라이언트 측 오류 디버깅
   - API 키 오류: `templates/index.html`의 Firebase 설정 값 확인

### 로컬 환경에서 구글 로그인 테스트

애플리케이션이 실행된 상태에서 동일한 단계로 테스트할 수 있습니다:
1. http://localhost:9090 접속
2. "Google로 로그인" 버튼 클릭
3. 구글 계정 선택 및 인증
4. 로그인 성공 시 사용자 정보 확인
5. "보호된 API 호출" 버튼으로 인증 테스트

## API 문서

- Swagger UI: http://localhost:9090/docs
- ReDoc: http://localhost:9090/redoc

## 새로운 엔드포인트

### 사용자 프로필 관련 엔드포인트

- `GET /api/users/me`: 현재 로그인한 사용자의 프로필 정보 조회
- `POST /api/users/me`: 현재 로그인한 사용자의 프로필 정보 업데이트
- `DELETE /api/users/me`: 현재 로그인한 사용자 계정 비활성화

### 데이터베이스 확인 엔드포인트

- `GET /api/db-check`: 데이터베이스 연결 상태 및 사용자 테이블 데이터 확인
- `GET /auth/check-users`: 데이터베이스에 저장된 사용자 목록 확인

### 시스템 정보 엔드포인트

- `GET /routes`: 등록된 모든 라우트 정보 확인
- `GET /api/test`: API 라우터 연결 테스트 (인증 불필요)

## 데이터베이스 스키마

사용자(User) 테이블에 다음 필드가 추가되었습니다:

| 필드명 | 타입 | 설명 |
|--------|------|------|
| profile_picture | String | 사용자 프로필 이미지 URL |
| bio | Text | 사용자 자기소개 |
| phone_number | String | 전화번호 |
| location | String | 위치 정보 |
| birth_date | DateTime | 생년월일 |
| gender | String | 성별 |
| last_login_at | DateTime | 마지막 로그인 시간 |
| last_login_ip | String | 마지막 로그인 IP 주소 |

## 보안 주의사항

- Firebase 서비스 계정 키(`firebase-adminsdk.json`)는 절대 공개 저장소에 커밋하지 마세요
- 테스트 목적이라도 가능한 Firebase Admin SDK 키는 환경 변수로 관리하세요
- 프로덕션 환경에서는 CORS 설정을 적절히 제한하세요

## 라이선스

MIT 

## MHP_TEST 사용 가능한 기능 및 절차

### 사용 가능한 기능

#### 1. 사용자 인증 및 관리
- 이메일/비밀번호 회원가입 및 로그인
- 구글 소셜 로그인
- 사용자 프로필 관리
- 비밀번호 재설정

#### 2. 데이터베이스 연동
- PostgreSQL 데이터베이스 연동
- Alembic을 통한 데이터베이스 마이그레이션 관리
- 사용자 데이터 CRUD 작업

#### 3. API 기능
- JWT 토큰 기반 인증된 API 엔드포인트
- Swagger 및 ReDoc을 통한 API 문서화
- API 버전 관리

#### 4. 배포 및 인프라
- Docker 컨테이너화
- Docker Compose를 통한 다중 서비스 관리
- Firebase Admin SDK 통합

### 사용 절차

#### 개발 환경 설정
1. 소스 코드 클론
   ```bash
   git clone [repository-url]
   cd MHP_TEST
   ```

2. 가상환경 설정
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```

4. Firebase 서비스 계정 키 설정
   - `docker/firebase-adminsdk.json` 파일 확인 또는 생성

#### 데이터베이스 마이그레이션
1. 마이그레이션 실행
   ```bash
   alembic upgrade head
   ```

2. 새 마이그레이션 생성 (스키마 변경 시)
   ```bash
   alembic revision --autogenerate -m "설명"
   ```

#### 로컬 서버 실행
1. FastAPI 서버 실행
   ```bash
   uvicorn app.main:app --reload
   ```

2. 서버 접속
   - API 서버: http://localhost:9090
   - API 문서: http://localhost:9090/docs

#### Docker 환경에서 실행
1. Docker 컨테이너 빌드 및 실행
   ```bash
   cd docker
   docker-compose up -d
   ```

2. 컨테이너 로그 확인
   ```bash
   docker-compose logs -f
   ```

#### 테스트 실행
1. 전체 테스트 실행
   ```bash
   pytest
   ```

2. 특정 테스트 파일 실행
   ```bash
   pytest app/tests/test_auth.py -v
   ```

### 문제 해결

- **Firebase 연결 오류**: Firebase 서비스 계정 키 파일이 올바른 위치에 있는지 확인하세요.
- **데이터베이스 연결 오류**: PostgreSQL 연결 문자열과 데이터베이스 서버 실행 여부를 확인하세요.
- **API 응답 오류**: 로그를 확인하고 JWT 토큰이 유효한지 확인하세요.
- **PGAdmin 연결 오류**: 올바른 호스트 이름/IP와 사용자 자격 증명을 사용하고 있는지 확인하세요.
  - Docker 네트워크 내에서 컨테이너 간 통신 문제가 있는 경우 `localhost` 대신 컨테이너 IP 주소를 사용해보세요. 

## 구글 로그인 테스트 방법

### 웹 인터페이스를 통한 테스트 (가장 간단한 방법)

1. Docker Compose로 서버 실행:
   ```bash
   cd docker
   docker-compose up
   ```

2. 웹 브라우저에서 접속:
   ```
   http://localhost:9090
   ```

3. 구글 로그인 진행:
   - "Google로 로그인" 버튼 클릭
   - 구글 계정으로 로그인
   - 로그인 성공 시 사용자 정보가 화면에 표시됨
   - "보호된 API 호출" 버튼으로 인증된 API 요청 테스트 가능

4. 개발자 도구에서 결과 확인:
   - 브라우저의 개발자 도구(F12) > 콘솔 탭에서 로그 확인
   - 로그인 성공 및 백엔드 응답 메시지 확인

### API 테스트 도구를 사용한 테스트 (Postman, curl 등)

1. 웹 인터페이스에서 먼저 구글 로그인을 수행합니다.

2. ID 토큰 가져오기:
   - 개발자 도구 콘솔에서 다음 코드 실행:
   ```javascript
   await firebase.auth().currentUser.getIdToken(true)
   ```
   - 출력된 토큰 문자열을 복사

3. Postman으로 테스트:
   - 구글 인증 API 테스트:
     - URL: `http://localhost:9090/auth/google-auth`
     - Method: POST
     - Headers: `Content-Type: application/json`
     - Body:
     ```json
     {
       "id_token": "복사한_ID_토큰",
       "name": "사용자_이름",
       "profile_picture": "프로필_사진_URL"
     }
     ```

   - 보호된 엔드포인트 테스트:
     - URL: `http://localhost:9090/auth/protected-endpoint`
     - Method: POST
     - Headers: 
       - `Content-Type: application/json`
       - `Authorization: Bearer 복사한_ID_토큰`

   - 사용자 정보 조회:
     - URL: `http://localhost:9090/api/users/me`
     - Method: GET
     - Headers: `Authorization: Bearer 복사한_ID_토큰`

4. curl로 테스트:
   ```bash
   # 구글 인증 API 테스트
   curl -X POST http://localhost:9090/auth/google-auth \
        -H "Content-Type: application/json" \
        -d '{"id_token":"복사한_ID_토큰","name":"사용자_이름","profile_picture":"프로필_사진_URL"}'

   # 보호된 엔드포인트 테스트
   curl -X POST http://localhost:9090/auth/protected-endpoint \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer 복사한_ID_토큰"

   # 사용자 정보 조회
   curl -X GET http://localhost:9090/api/users/me \
        -H "Authorization: Bearer 복사한_ID_토큰"
   ```

### 주의사항

1. 테스트 전 데이터베이스 마이그레이션 실행:
   ```bash
   docker-compose exec web alembic upgrade head
   ```

2. 인증 토큰 만료 시간:
   - Firebase ID 토큰은 일정 시간 후 만료됩니다 (보통 1시간).
   - 만료된 경우 다시 로그인하여 새 토큰을 얻어야 합니다.

3. 브라우저 호환성:
   - Chrome 또는 Firefox 브라우저 사용 권장
   - 팝업 차단을 비활성화해야 구글 로그인 팝업이 정상 작동합니다.

4. 네트워크 설정:
   - 방화벽이 9090 포트를 차단하지 않는지 확인
   - Docker 네트워크가 정상적으로 구성되어 있는지 확인

## 사용자 프로필 기능 사용 방법

새로 추가된 사용자 프로필 기능을 사용하는 방법은 다음과 같습니다:

### 사용자 프로필 정보 조회하기

1. **웹 인터페이스를 통한 방법**:
   - 로그인 페이지 (http://localhost:9090/login)에 접속
   - 'Google로 로그인' 버튼을 클릭하여 로그인
   - 로그인 후 "내 프로필 정보 가져오기" 버튼 클릭
   - 결과 영역에 JSON 형태로 프로필 정보 표시

2. **API 직접 호출 방법**:
   - 토큰 획득: 웹 인터페이스에서 로그인 후 개발자 도구 콘솔에서 다음 코드 실행
     ```javascript
     await firebase.auth().currentUser.getIdToken()
     ```
   - Postman이나 curl로 API 호출:
     ```bash
     curl -X GET http://localhost:9090/api/users/me \
          -H "Authorization: Bearer 복사한_토큰" \
          -H "Content-Type: application/json"
     ```

### 사용자 프로필 정보 업데이트하기

1. **API 호출 방법**:
   ```bash
   curl -X POST http://localhost:9090/api/users/me \
        -H "Authorization: Bearer 복사한_토큰" \
        -H "Content-Type: application/json" \
        -d '{
          "name": "새 이름",
          "bio": "자기소개",
          "profile_picture": "이미지URL",
          "phone_number": "전화번호",
          "location": "위치",
          "gender": "성별"
        }'
   ```

2. **응답 확인**:
   - 성공 시 업데이트된 사용자 정보가 JSON 형태로 반환됩니다.
   - 실패 시 오류 메시지와 함께 상태 코드가 반환됩니다.

### 프로필 정보 저장 및 관리

1. **데이터베이스 확인**:
   - PGAdmin(http://localhost:5050)에 접속하여 로그인
   - 등록된 서버에 연결하여 `mhp_db` 데이터베이스 선택
   - `users` 테이블을 조회하여 저장된 프로필 정보 확인

2. **사용자 목록 조회**:
   - 브라우저에서 `http://localhost:9090/auth/check-users` 접속
   - 데이터베이스에 저장된 모든 사용자 정보 확인

### 문제 해결

- **프로필 정보가 보이지 않는 경우**:
  1. 데이터베이스 마이그레이션이 제대로 실행되었는지 확인:
     ```bash
     cd docker
     docker-compose exec web alembic upgrade head
     ```
  2. 토큰이 유효한지 확인 (만료된 경우 재로그인)
  3. API 경로가 올바른지 확인 (`/api/users/me`)

- **업데이트가 적용되지 않는 경우**:
  1. 요청 헤더와 본문 형식이 올바른지 확인
  2. 서버 로그 확인:
     ```bash
     docker-compose logs -f web
     ```

### 사용자 계정 비활성화

1. **API 호출 방법**:
   ```bash
   curl -X DELETE http://localhost:9090/api/users/me \
        -H "Authorization: Bearer 복사한_토큰"
   ```

2. **계정 상태 확인**:
   - 비활성화 후 로그인 시도하면 오류 메시지 표시
   - 데이터베이스에서 해당 사용자의 `is_active` 필드가 `false`로 변경된 것 확인 가능 