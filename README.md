# Simple Log Pipeline

## 1. 프로젝트 개요

이 프로젝트는 랜덤 이벤트 로그를 생성하고, 이를 PostgreSQL에 저장한 뒤 SQL 기반 분석과 시각화를 수행하는 간단한 로그 파이프라인입니다.

과제의 필수 요구사항인 **이벤트 생성 → 저장 → 분석 → 시각화 → Docker Compose 기반 실행** 흐름을 하나의 구조로 구현하는 데 초점을 맞췄습니다.

이벤트는 `page_view`, `purchase`, `error`의 세 가지 유형으로 구성했으며, 각 이벤트를 필드 단위로 분리하여 저장하도록 설계했습니다. 이를 통해 단순 로그 저장에 그치지 않고, 이후 SQL 집계와 시각화까지 자연스럽게 이어질 수 있도록 구성했습니다.

또한 이번 구현에서는 복잡한 기술을 과도하게 추가하기보다, 데이터 파이프라인의 기본 동작을 **재현 가능하고 명확한 형태로 완성하는 것**을 우선했습니다.

## 2. 기술 스택

- Python 3.11
- PostgreSQL 15
- SQLAlchemy
- psycopg2-binary
- pandas
- matplotlib
- Docker
- Docker Compose

## 3. 프로젝트 구조

```text
simple-log-pipeline/
├─ app/
│  ├─ main.py
│  ├─ generator.py
│  ├─ db.py
│  ├─ analysis.py
│  ├─ visualize.py
│  ├─ requirements.txt
│  └─ init.sql
├─ output/
│  ├─ event_type_counts.png
│  └─ hourly_event_trend.png
├─ Dockerfile
├─ docker-compose.yml
└─ README.md
```

## 4. 실행 방법

### 필요한 도구

- Docker
- Docker Compose

### 사전 준비

- Docker와 Docker Compose가 설치되어 있어야 합니다.

### 실행 명령어

프로젝트 루트 폴더에서 아래 명령어를 실행합니다.

```bash
docker compose up --build
```

실행이 완료되면 다음 작업이 자동으로 수행됩니다.

1. PostgreSQL 컨테이너 실행
2. `events` 테이블 생성
3. 랜덤 이벤트 1000건 생성
4. 이벤트를 PostgreSQL에 저장
5. SQL 분석 수행
6. 시각화 이미지 파일 저장

생성된 결과 이미지는 `output/` 폴더에서 확인할 수 있습니다.

## 5. 이벤트 설계

이벤트 타입은 아래 3가지로 구성했습니다.

- `page_view`
- `purchase`
- `error`

### 설계 이유

- `page_view`: 가장 기본적인 사용자 행동 로그를 표현하기 위해 추가했습니다.
- `purchase`: 사용자 행동 중 비즈니스적으로 의미가 큰 이벤트를 포함하기 위해 추가했습니다.
- `error`: 단순 행동 분석뿐 아니라 품질 모니터링 관점도 반영하기 위해 추가했습니다.

모든 이벤트가 동일한 속성을 가지는 것은 아니므로, 공통 필드와 nullable 필드를 함께 사용했습니다.

## 6. 스키마 설명

이번 과제에서는 이벤트 생성부터 저장, 분석까지의 흐름을 단순하고 명확하게 보여주기 위해 단일 `events` 테이블로 설계했습니다.

이벤트를 JSON 형태로 통째로 저장하지 않고, `event_type`, `event_time`, `user_id` 등 주요 필드를 분리해서 저장하도록 구성했습니다. 이렇게 하면 SQL 기반 집계와 분석이 쉬워지고, 과제 요구사항에도 더 잘 맞는다고 판단했습니다.

```sql
CREATE TABLE IF NOT EXISTS events (
    event_id UUID PRIMARY KEY,
    user_id INT NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    event_time TIMESTAMP NOT NULL,
    page_url VARCHAR(255),
    product_id VARCHAR(50),
    amount NUMERIC(10, 2),
    error_code VARCHAR(50)
);
```

## 7. 분석 항목

다음 3가지 분석을 수행했습니다.

### 7-1. 이벤트 타입별 발생 횟수

각 이벤트 타입이 몇 번 발생했는지 집계합니다. 이를 통해 어떤 유형의 이벤트가 가장 많이 발생했는지 확인할 수 있습니다.

### 7-2. 시간대별 이벤트 추이

이벤트 발생 시간을 hour 단위로 묶어서 집계했습니다. 이를 통해 특정 시간대에 이벤트가 몰리는지 확인할 수 있습니다.

### 7-3. 에러 비율

전체 이벤트 대비 `error` 이벤트 비율을 계산했습니다. 이를 통해 단순 행동 로그뿐 아니라 품질 관점의 지표도 함께 확인할 수 있도록 했습니다.

## 8. 시각화 결과

분석 결과를 아래 이미지 파일로 저장했습니다.

- `output/event_type_counts.png`
- `output/hourly_event_trend.png`

### 8-1. 이벤트 타입별 건수

이벤트 종류별 발생 횟수를 막대그래프로 저장했습니다.

### 8-2. 시간대별 이벤트 추이

시간 흐름에 따른 이벤트 수 변화를 선그래프로 저장했습니다.

## 9. 구현하면서 고민한 점

처음에는 이벤트를 더 복잡하게 나누거나 여러 테이블로 분리하는 방법도 생각했지만, 과제 범위를 고려했을 때 오히려 구조가 불필요하게 복잡해질 수 있다고 판단했습니다. 그래서 먼저 필수 요구사항을 안정적으로 충족하는 방향으로 범위를 제한했습니다.

또한 로컬 개발 환경과 Docker 실행 환경에서 DB 연결 방식이 달라질 수 있다는 점을 고려해, DB 접속 정보를 환경변수 기반으로 처리했습니다. 그리고 Docker Compose 실행 시 DB가 완전히 올라오기 전에 앱이 먼저 실행될 수 있어, DB 연결 재시도 로직을 추가해 이를 해결했습니다.

추가로 시각화 부분에서는 웹 대시보드까지 확장하는 대신, 과제 요구사항에 맞게 이미지 파일 저장 방식으로 구현했습니다. 복잡한 도구를 더하는 것보다, 실행 가능성과 결과 확인이 명확한 형태가 더 적절하다고 판단했습니다.

## 10. 한계와 개선 방향

### 한계

- 이벤트가 모두 랜덤 생성 데이터입니다.
- 중복 실행 시 데이터 누적이 발생할 수 있습니다.
- 배치 실행 기준으로 동작하며, 실시간 스트리밍 구조는 아닙니다.
- 시각화 결과가 PNG 파일 저장 수준에 머물러 있습니다.

### 개선 방향

- 이벤트 중복 방지 로직 추가
- 실행 시 기존 데이터 초기화 여부 옵션화
- 실시간 메시지 큐(Kafka 등) 기반 구조로 확장
- Airflow 등을 활용한 스케줄링 추가
- BI 대시보드 또는 웹 기반 시각화로 확장
- AWS 환경(EC2, RDS, S3, CloudWatch) 기준 운영 구조 설계
