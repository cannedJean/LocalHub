import apiClient from './client'

export function postChat(message, history = []) {
  return apiClient.post('/chat', { message, history }).then((res) => res.data)
}
