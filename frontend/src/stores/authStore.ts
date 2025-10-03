import { create } from 'zustand'
import { User } from '../types'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (user: User, accessToken: string, refreshToken: string) => void
  logout: () => void
  updateUser: (user: User) => void
  setLoading: (loading: boolean) => void
}

export const useAuthStore = create<AuthState>((set) => {
  // Initialize from localStorage
  const storedUser = localStorage.getItem('user')
  const storedToken = localStorage.getItem('access_token')

  return {
    user: storedUser ? JSON.parse(storedUser) : null,
    isAuthenticated: !!storedToken,
    isLoading: false,

    login: (user, accessToken, refreshToken) => {
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('access_token', accessToken)
      localStorage.setItem('refresh_token', refreshToken)
      set({ user, isAuthenticated: true })
    },

    logout: () => {
      localStorage.removeItem('user')
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      set({ user: null, isAuthenticated: false })
    },

    updateUser: (user) => {
      localStorage.setItem('user', JSON.stringify(user))
      set({ user })
    },

    setLoading: (loading) => set({ isLoading: loading }),
  }
})