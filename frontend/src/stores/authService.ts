import axios from '../lib/axios'
import { LoginCredentials, RegisterData, AuthResponse, User } from '../types'

export const authService = {
  async login(credentials: LoginCredentials): Promise<{ user: User } & AuthResponse> {
    const response = await axios.post<AuthResponse>('/auth/login', credentials)
    const { access_token } = response.data
    
    // Get user profile
    const userResponse = await axios.get<User>('/users/me', {
      headers: { Authorization: `Bearer ${access_token}` }
    })
    
    return {
      ...response.data,
      user: userResponse.data
    }
  },

  async register(data: RegisterData): Promise<User> {
    const response = await axios.post<User>('/auth/register', data)
    return response.data
  },

  async getCurrentUser(): Promise<User> {
    const response = await axios.get<User>('/users/me')
    return response.data
  },

  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await axios.put<User>('/users/me', data)
    return response.data
  },
}