export function normalizePost(source = {}) {
  return {
    id: String(source.id ?? source.post_id ?? ''),
    category: source.category || 'free',
    title: source.title || '',
    content: source.content || '',
    createdAt: source.created_at ?? source.createdAt ?? '',
    updatedAt: source.updated_at ?? source.updatedAt ?? '',
    views: Number(source.views ?? source.view_count ?? 0),
  }
}

export function normalizePostResponse(payload = {}) {
  const envelope = payload?.data && !Array.isArray(payload) ? payload.data : payload
  const sourceItems = Array.isArray(envelope) ? envelope : envelope?.items || envelope?.results || []
  const items = sourceItems.map(normalizePost)

  return {
    items,
    total: Number(envelope?.total ?? items.length),
    page: Number(envelope?.page ?? 1),
    size: Number(envelope?.size ?? items.length),
    totalPages: Number(envelope?.totalPages ?? envelope?.total_pages ?? 1),
  }
}
