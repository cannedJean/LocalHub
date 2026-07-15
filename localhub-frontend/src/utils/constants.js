// TourAPI content-type IDs → Korean label + emoji (대전·충청권 dataset).
export const LOCATION_TYPES = [
  { id: '12', label: '관광지', emoji: '🏰' },
  { id: '14', label: '문화시설', emoji: '🎨' },
  { id: '15', label: '축제·공연', emoji: '🎉' },
  { id: '25', label: '여행코스', emoji: '🧭' },
  { id: '28', label: '레포츠', emoji: '🚴' },
  { id: '32', label: '숙박', emoji: '🏨' },
  { id: '38', label: '쇼핑', emoji: '🛍️' },
  { id: '39', label: '음식점', emoji: '🍜' },
]

export const LOCATION_TYPE_MAP = new Map(LOCATION_TYPES.map((t) => [t.id, t]))

// Home screen shows 6 shortcuts: 관광지 · 음식점 · 축제·공연 · 문화시설 · 레포츠 · 쇼핑.
export const HOME_CATEGORY_IDS = ['12', '39', '15', '14', '28', '38']

export const HOME_CATEGORIES = HOME_CATEGORY_IDS.map((id) => LOCATION_TYPE_MAP.get(id)).filter(
  Boolean,
)

// Per-type counts for the 데이터 출처 page (한국관광공사 TourAPI 4.0, 총 1,365건).
export const LOCATION_TYPE_COUNTS = [
  { label: '관광지', count: 335 },
  { label: '문화시설', count: 82 },
  { label: '축제공연행사', count: 26 },
  { label: '여행코스', count: 28 },
  { label: '레포츠', count: 68 },
  { label: '숙박', count: 52 },
  { label: '쇼핑', count: 258 },
  { label: '음식점', count: 516 },
]

export const TOTAL_LOCATION_COUNT = 1365

// Region cities (대전·충청권). id = backend query value, label = display.
export const CITIES = [
  { id: 'daejeon', label: '대전' },
  { id: 'sejong', label: '세종' },
  { id: 'gyeryong', label: '계룡' },
  { id: 'gongju', label: '공주' },
  { id: 'nonsan', label: '논산' },
  { id: 'okcheon', label: '옥천' },
]

// Community post categories. `id` is the single source of truth shared with the backend.
export const POST_CATEGORIES = [
  { id: 'tour', label: '관광지', color: 'cat-badge-tour' },
  { id: 'food', label: '맛집', color: 'cat-badge-food' },
  { id: 'festival', label: '축제', color: 'cat-badge-festival' },
  { id: 'free', label: '자유게시판', color: 'cat-badge-free' },
]

const POST_CATEGORY_MAP = new Map(POST_CATEGORIES.map((c) => [c.id, c]))

export function getCategoryLabel(id) {
  return POST_CATEGORY_MAP.get(id)?.label || '분류없음'
}

export function getCategoryColor(id) {
  return POST_CATEGORY_MAP.get(id)?.color || 'cat-badge-free'
}

function pad(value) {
  return String(value).padStart(2, '0')
}

// "2026.07.14 21:30" — tolerant of missing/invalid dates.
export function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return String(iso)
  return `${d.getFullYear()}.${pad(d.getMonth() + 1)}.${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

// "2026.07.14"
export function formatDateShort(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return String(iso)
  return `${d.getFullYear()}.${pad(d.getMonth() + 1)}.${pad(d.getDate())}`
}
