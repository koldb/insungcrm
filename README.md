
SCM 웹 사이트 개발

주소 : myscm.kro.kr
테스트 아이디 : admin
테스트 비밀번호 : 1234


1. 목적
  B2B 업체에서 사용할 목적으로 고객들이 자유롭게 견적 / 문의사항 / 출고 제품 정보 조회 / AS 접수 가능하도록 구현
  
2. 특징
  초기 계획에서는 고객사 아이디는 직접 만들어서 배포하기로 하였으나 자유롭게 가입 가능하도록 회원가입 기능을 추후에 추가
  
  본사는 견적 접수건에 대한 발주 / 견적, 발주 데이터 조회, 관리 / AS 대응 / 문의사항 응대 업무 가능
  회원 가입시 특정 업체명(insung) 기입 여부에 따라 메뉴 구성이 달라지고 접근 권한이 달라지도록 개발
  
3. 개발 툴
  Python 3.10.4
  MySql 8.0.28
  Django 4.0.4
  
  AWS 
  ubuntu server 20.04 LTS
  Python 3.8.10
  MySql 8.0.30
  
4. 메뉴
  a. 회원 가입 / 로그인 / 로그아웃
  b. 견적 / 발주 리스트 
     - 견적 문의 등록 / 리스트 / 첨부 파일 업로드 / 발주 등록(수량, 단가)
  c. 제품 조회 / 출고 관리
     - 리스트 / 발주 제품 입력(시리얼, 제품 정보)
  d. AS 접수
     - AS 글 등록 / 리스트 / AS 처리 내역 입력
  e. 기타 문의 목록
     - 문의 글 등록 / 리스트 / 댓글 기능
  f. 관리 기능
     - 공지사항 입력 / 제품명 DB 리스트, 입력 / 제품 DB 리스트, 입력
  g. 메인페이지
     - 공지사항 확인 / 주간, 월간 데이터 대쉬보드
     
5. 개발시 중점 사항
  - CSS / 디자인은 다른 직원이 맡을 예정으로 기능 구현 작업만 맡아 진행 함
  - 기존 엑셀로 이루어지던 모든 작업을 웹 사이트에서 진행 할 수 있도록 필요한 기능 구현에 초점을 맞춤
  - 첨부 파일 업로드 / 내역 엑셀 다운로드 / 제품 DB 엑셀 업로드 기능 구현이 필수였기에 추가
  - 엑셀로 진행되던 업무를 웹 사이트에서 진행할 예정 이였기에 단순하고 빠르게 입력 가능하도록 최대한 단순화하여 구현
  
