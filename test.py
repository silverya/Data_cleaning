import data_cleaning_module

# 검토할 텍스트
text = """(단독공개)  「제휴 서비스」 
          ※제휴 가능※ 【사진 참조】
          인기제품의 할인정보를 비교해보세요
          (김지현 기자) 댓글 30개
          재판매 및 DB 금지
          인기제품의할인정보를비교해보세요
          프로필 상단 바로가기
          @jennyrubyjane @fff_dd
          @나나나 
          #팔로우 #맞팔 #좋아요테러
          #fdsfsdfsf
          추천인코드 : [ㅓㅁㄴ아ㅣdsad]
          내공 500
          게시물이 삭제되어 요청하신 페이지를 표시할 수 없습니다.
          권한이 없거나 삭제되었습니다.
          |작성자 |
          이재명 전 경기도 시장이 대선에 출마하였습니다. 9시 뉴스  9시뉴스 동아일보 김상현 기자 http://www.youtu.be/-ZClicWm0zM shking456@gmail.com  #sdf #화이팅 #제니 #아이유 01-456-4567 
          010-4567-8756 """

# 언론(DN) 블로그(BL) 인스타그램(IG) 트위터(TW) 커뮤니티(DC) 지식인(QA)
channel = 'DN'

data_clean = data_cleaning_module.dataClean(text, channel)
result = data_clean.main()
print(result)


''' result

[['36' '43' '【사진 참조】']
 ['83' '91' '(김지현 기자)']
 ['109' '120' '재판매 및 DB 금지']
 ['436' '441' '9시 뉴스']
 ['443' '447' '9시뉴스']
 ['460' '491' 'http://www.youtu.be/-ZClicWm0zM']
 ['492' '511' 'shking456@gmail.com']
 ['532' '543' '01-456-4567']
 ['555' '568' '010-4567-8756']]

'''