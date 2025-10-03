import axios from '../lib/axios'
import { Conversation, Message } from '../types'

export const conversationService = {
  async getConversations(): Promise<Conversation[]> {
    const response = await axios.get<Conversation[]>('/conversations/')
    return response.data
  },

  async getConversation(id: string): Promise<Conversation> {
    const response = await axios.get<Conversation>(`/conversations/${id}`)
    return response.data
  },

  async createConversation(productId: string): Promise<Conversation> {
    const response = await axios.post<Conversation>('/conversations/', {
      product_id: productId
    })
    return response.data
  },

  async sendMessage(conversationId: string, data: {
    message: string
    message_type?: 'text' | 'contact_share' | 'offer'
    offer_price?: number
  }): Promise<Message> {
    const response = await axios.post<Message>(
      `/conversations/${conversationId}/messages`,
      data
    )
    return response.data
  },
}