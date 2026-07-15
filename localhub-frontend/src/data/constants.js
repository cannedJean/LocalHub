export const CONTENT_TYPES = [
  { id: '', label: '전체', emoji: '🧭', count: 1365 },
  { id: '12', label: '관광지', emoji: '🏰', count: 335 },
  { id: '39', label: '음식점', emoji: '🍜', count: 516 },
  { id: '14', label: '문화시설', emoji: '🎨', count: 82 },
  { id: '15', label: '축제·공연', emoji: '🎉', count: 26 },
  { id: '25', label: '여행코스', emoji: '🧭', count: 28 },
  { id: '28', label: '레포츠', emoji: '🚴', count: 68 },
  { id: '32', label: '숙박', emoji: '🏨', count: 52 },
  { id: '38', label: '쇼핑', emoji: '🛍️', count: 258 },
]

export const HOME_CATEGORIES = CONTENT_TYPES.filter((type) =>
  ['12', '39', '15', '14', '28', '38'].includes(type.id),
)

export const CITIES = [
  { id: '', label: '전체' },
  { id: 'daejeon', label: '대전' },
  { id: 'sejong', label: '세종' },
  { id: 'gyeryong', label: '계룡' },
  { id: 'gongju', label: '공주' },
  { id: 'nonsan', label: '논산' },
  { id: 'okcheon', label: '옥천' },
]

export const POST_CATEGORIES = [
  { id: '', label: '전체' },
  { id: 'tour', label: '관광지' },
  { id: 'food', label: '맛집' },
  { id: 'festival', label: '축제' },
  { id: 'free', label: '자유게시판' },
]

export const POST_CATEGORY_LABELS = Object.fromEntries(
  POST_CATEGORIES.filter((category) => category.id).map((category) => [category.id, category.label]),
)

export const CHAT_SUGGESTIONS = [
  '대전 관광지를 추천해줘',
  '이번 주말 축제를 알려줘',
  '유성구 맛집 위치를 알려줘',
  '축제 관련 게시글을 찾아줘',
  '오늘은 실내와 실외 중 어디가 좋아?',
]

export const LICENSE_TEXT =
  '출처: 한국관광공사 | 데이터: TourAPI 4.0 국문 관광정보 | 라이선스: 공공누리 제3유형 (출처표시-변경금지)'
