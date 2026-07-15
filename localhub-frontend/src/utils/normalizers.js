import { LOCATION_TYPE_MAP } from './constants'

const FALLBACK_TYPE = { label: '기타', emoji: '📍' }

// mapx(경도)/mapy(위도) arrive as strings. Return a finite in-range float or null.
function parseCoordinate(value, min, max) {
  if (value === '' || value === null || value === undefined) return null
  const parsed = Number.parseFloat(value)
  return Number.isFinite(parsed) && parsed >= min && parsed <= max ? parsed : null
}

// Normalize a raw TourAPI item. Never invents data; tolerates missing fields.
export function normalizeLocation(source = {}, index = 0) {
  const contentId = String(source.contentid ?? '')
  const typeId = String(source.contenttypeid ?? '')
  const type = LOCATION_TYPE_MAP.get(typeId) ?? FALLBACK_TYPE
  const latitude = parseCoordinate(source.mapy, -90, 90)
  const longitude = parseCoordinate(source.mapx, -180, 180)
  const image = String(source.firstimage || source.firstimage2 || '').replace(/^http:/, 'https:')

  return {
    contentId,
    typeId,
    typeLabel: type.label,
    emoji: type.emoji,
    title: source.title || '이름 없는 장소',
    address: [source.addr1, source.addr2].filter(Boolean).join(' ') || '주소 정보 없음',
    telephone: source.tel || '',
    image,
    latitude,
    longitude,
    hasValidCoordinates: latitude !== null && longitude !== null,
    tintIndex: index % 4,
  }
}

// Accepts several pagination envelope shapes and returns a consistent structure.
export function normalizePage(payload = {}, mapper = (value) => value) {
  const envelope = payload?.data ?? payload
  const sourceItems = Array.isArray(envelope)
    ? envelope
    : (envelope?.items ?? envelope?.results ?? [])

  const items = sourceItems.map(mapper)

  return {
    items,
    total: Number(envelope?.total ?? envelope?.pagination?.total_items ?? items.length),
    page: Number(envelope?.page ?? envelope?.pagination?.page ?? 1),
    size: Number(envelope?.size ?? items.length),
    totalPages: Number(
      envelope?.totalPages ?? envelope?.total_pages ?? envelope?.pagination?.total_pages ?? 1,
    ),
  }
}
