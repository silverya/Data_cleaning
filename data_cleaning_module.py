import re

# 검토할 텍스트
text = """(단독공개)  「제휴 서비스」 
          ※제휴 가능※ 【사진 찍어주세요】
          인기제품의 할인정보를 비교해보세요
          (기자 파티) 댓글 30개
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

# 언론 블로그 인스타그램 트위터 커뮤니티 지식인
channel_name = '인스타그램'


# 노이즈 문구 인덱스 추출
def extrackNoiseIndex(text, channel_name) :
    
    
  sIndex = []                       # 시작 인덱스 list
  eIndex = []                       # 끝 인덱스 list
  noise_sentences = []              # 도출한 noise list
  
  
  # 공통 조건
  common_condition = r"""
  \d{2,3}-\d{3,4}-\d{4}|                                                                                                # 전화번호   
  ([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)|                                                                                     # 이메일
  (http|https|ftp|ftps)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?|                                                   # url
  [△ⓒ■◇▲◆□◇▶]|                                                                                                     # 특수기호
  """
  
  # 언론 채널 조건
  news_condition =  r"""
  (\[|\(|\<|\【)[\w\s]*(데일리|KBS|the300|데일리|TV|경제|기사입니다|기자|끝|뉴스|구독|뉴시스|닷컴|미디어|사진|상보|속보|스포츠|DB|신문|앵커|영상|원문|인사이트|자료|자세한 내용|저작권|제공|제작|종합|출고일시|출연자|출처|취재|편집|캡처|코리아|토론)[\w\s]*(\]|\)|\>|\】)|
  ([0-9]{1,2}시)\s?(뉴스)\s?(마칩니다.)\s?(시청해주신)\s?(여러분)\s?(고맙습니다.)|
  ([0-9]{1,2}시)\s?(뉴스)|
  ([0-9]{1,2}월)\s?([0-9]{1,2}일)\s?('뉴스)\s?([0-9]{1,2}')\s?(클로징)|
  (※자세한)\s?(내용은)\s?(뉴스TOP10에서)\s?(확인하실)\s?(수)\s?(있습니다.)|
  (CBS)\s?(Radio)\s?(표준FM)\s?(98.1MHz)\s?(주요뉴스)|
  (위)\s?(사진은)\s?(기사)\s?(내용과)\s?(직접적인)\s?(관련이)\s?(없습니다.)|
  (다음)\s?(링크를)\s?(통해)\s?('다시보기'를)\s?(시청할 수 있다.)|
  (※)\s?(뉴스)\s?(영상은)\s?(저작권)\s?(관계로)\s?(TV조선)\s?(뉴스)\s?(홈페이지에서)\s?(보실)\s?(수)\s?(있습니다)|
  (※)\s?(저작권)\s?(관계로)\s?(다음에서)\s?(서비스하지)\s?(않는)\s?(영상입니다.)|
  (재판매)\s?(및)\s?(DB)\s?(금지)|
  (라이온봇)\s?(기자)\s?(-한국경제TV※)\s?(본)\s?(기사는)\s?(한국경제TV와)\s?(`금융)\s?(AI)\s?(전문기업)\s?(씽크풀`이)\s?(실시간으로)\s?(작성한)\s?(기사입니다.)|
  (해당)\s?(내용은)\s?(관련)\s?(동영상)\s?(참고)|
  (카카오톡)\s?(:)\s?('KBS제보')\s?(검색)
  """
  
  # 블로그 채널 조건
  blog_condition = r"""
  (\[|\(|\<|\【|∇|※|「)[\w\s]*(제휴|광고|섭외|문의|개월|설명|사진|기자|셀럽미디어|매경이코노미|기사|엑스포츠뉴스|TV조선|방송|기사공유|텐아시아|이데일리|파이낸셜|파트너스|커미션|국민지원금|포장)[\w\s]*(\]|\)|\>|\】|∇|※|」)|
  (댓글)\s?[0-9]{1,}(개)|
  (인기제품의)\s?(할인정보를)\s?(비교해보세요)|
  (후기와)\s?(사용자)\s?(평점을)\s?(꼭)\s?(확인하세요)|
  (제품)\s?(정보는)\s?(날짜/시간)\s?(기준으로),\s?(구매)\s?(시)\s?(변동이)\s?(있을)\s?(수)\s?(있습니다.)|
  (판매정보는)\s?(아래)\s?(링크를)\s?(확인하세요.)|
  (구매에)\s?(도움되는)\s?(판매후기와)\s?(평점도)\s?(참고하세요.)|
  (본)\s?(코멘트는)\s?(제휴)\s?(마케팅의)\s?(일환으로),\s?(금전적)\s?(소득을)\s?(얻을)\s?(수)\s?(있습니다.)|
  (사람들이)\s?(좋아한)\s?(인기)\s?(포스팅)|
  (사진)\s?(설명을)\s?(입력하세요)|
  (PC로)\s?(보시면)\s?(원본화질로)\s?(감상하실수)\s?(있습니다)|
  (뉴스퀘스트)\s?(관련기사)\s?(내용보기)|
  (사진을)\s?(클릭하면)\s?(해당)\s?(내용으로)\s?(연결됩니다.)|
  (PC버전에서)\s?(감상하실)\s?(경우)\s?(사진을)\s?(클릭하시면)\s?(더욱)\s?(좋은)\s?(화질로)\s?(감상하실)\s?(수)\s?(있습니다.)
  """
  
  # 인스타그램 채널 조건
  instagram_condition = r"""
  (\[|\(|\<|\【|「)[\w\s]*(론칭|행사|프로젝트|단독공개|스토리|COVER|소재|컬러|릴리|하루|모임|EVENT|이벤트|안내)[\w\s]*(\]|\)|\>|\】|」)|
  @[a-zA-Z0-9_]{2,}|
  (\#(팔로우|팔로미|팔로잉|선팔|맞팔|선팔하면맞팔|선팔맞팔|인친환영|디엠|좋아요테러|소통|소통환영|선팔하면맞팔가요|맞팔100|좋튀|좋아요그램|좋반|좋튀|좋아요램|fff|likeforlikes|liker|첫줄반사|댓글|좋아요테러|맞좋아요|좋반댓|좋아요반사테러|첫줄좋반))|
  (수강문의:)\s?(DM,카카오톡,전화)|
  (프로필)\s?(상단)\s?(바로가기)
  """
  
  # 트위터 채널 조건
  twitter_condition = r"""
  @[a-zA-Z0-9_]{2,}
  """
  
  # 커뮤니티 채널 조건
  community_condition = r"""
  (\[|\(|\<|\【)[\w\s]*(스포티비뉴스|스포츠조선|email protected|베프리포트|기자|사진|인스타그램|저작권자|재배포|무단전재|신고하기|가입|법적 책임|복사등록|저작권법)[\w\s]*(\]|\)|\>|\】)|
  \|(.*?)\||
  (스포츠)\s?(기사)\s?(섹션)(\(종목\))\s?(정보는)\s?(언론사)\s?(분류와)\s?(기술)\s?(기반의)\s?(자동)\s?(분류)\s?(시스템을)\s?(따르고)\s?(있습니다.)\s?(오분류에)\s?(대한)\s?(건은)\s?(네이버스포츠로)\s?(제보)\s?(부탁드립니다.)
  (Copyright)\s?(ⓒ)\s?(스포츠조선.)\s?(All)\s?(rights)\s?(reserved.)\s?(무단)\s?(전재)\s?(및)\s?(재배포)\s?(금지.)|
  (기자의)\s?(구독을)\s?(취소하시겠습니까?)|
  (구독에서)\s?(해당)\s?(기자의)\s?(기사가)\s?(제외됩니다.)|
  (Copyrightsⓒ)\s?(스포츠조선)(\(http://sports.chosun.com/\),)\s?(무단)\s?(전재)\s?(및)\s?(재배포)\s?(금지)|
  (BEST)\s?(Entertainment)\s?(\/)\s?(Football)\s?(Friends)\s?(글이)\s?(주는)\s?(감동.)\s?(베프리포트)|
  (죄송합니다,)\s?(회원에게만)\s?(공개된)\s?(글입니다)|
  (로그인)\s?(후)\s?(이용해)\s?(주세요)\s?(\(즉시\s?가입\s?가능\))\s?(관심)\s?(장소를)\s?(MY플레이스에)\s?(저장할)\s?(수)\s?(있어요.)|
  ('내)\s?(장소')\s?(폴더에)\s?(저장했습니다.)|
  (빈공간을)\s?(더블탭)\s?(해보세요)|
  (권한이)\s?(없거나)\s?(삭제되었습니다.)
  """
  
  # 지식인 채널 조건
  qna_condition = r"""
  (내공)\s?[0-9]{1,}|
  (추천인\s?코드)\s?(:)\s?\[(.*)\]|
  (게시물이)\s?(삭제되어)\s?(요청하신)\s?(페이지를)\s?(표시할)\s?(수)\s?(없습니다.)|
  (\[|\(|\<|\【|「)[\w\s]*(캐시백|보기|특징|서론|출력|Web발신|UNISEX|기자|아이뉴스24|서울=|뉴시스)[\w\s]*(\]|\)|\>|\】|」)|
  (\#[\w]{1,})
  """

  if channel_name == '언론' :
    p = re.compile(common_condition+news_condition, re.VERBOSE|re.MULTILINE)
  elif channel_name == '블로그' :
    p = re.compile(common_condition+blog_condition, re.VERBOSE|re.MULTILINE)
  elif channel_name == '인스타그램' :
    p = re.compile(common_condition+instagram_condition, re.VERBOSE|re.MULTILINE)
  elif channel_name == '트위터' :
    p = re.compile(common_condition+twitter_condition, re.VERBOSE|re.MULTILINE)
  elif channel_name == '커뮤니티' :
    p = re.compile(common_condition+community_condition, re.VERBOSE|re.MULTILINE)
  else  :
    p = re.compile(common_condition+qna_condition, re.VERBOSE|re.MULTILINE)      

  all_m = p.finditer(text)
  
  if p.search(text) is not None :
    for m in all_m :
      startNum = m.start()
      endNum = m.end()
      noise_sentence = m.group()
      #print("{0}, {1}".format(startNum,endNum))
      sIndex.append(startNum)
      eIndex.append(endNum)
      noise_sentences.append(noise_sentence) 
  else :
      print("nothing")   

  return sIndex, eIndex, noise_sentences


# 노이즈 문구 출력
def extrackNoiseSentence(sIndex, eIndex, noise_sentences) :
      
  for i in range(len(sIndex)) :
    print("sIndex : %s" %sIndex[i])
    print("eIndex : %s" %eIndex[i])
    print("noise_sentence : ", noise_sentences[i])
    #print(text[sIndex[i]:eIndex[i]+1])
    
    
if __name__ == '__main__':
    
  sIndex, eIndex, noise_sentences = extrackNoiseIndex(text, channel_name)
  extrackNoiseSentence(sIndex, eIndex, noise_sentences)    