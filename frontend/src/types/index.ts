export interface User {
  id: string
  email: string
  company_name: string
  is_verified: boolean
  is_active: boolean
}

export interface Product {
  id: string
  title: string
  description: string
  price?: number
  status: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  phone: string
  password: string
  company_name: string
  contact_person: string
  gst_number: string
  city?: string
  state?: string
  pincode?: string
  user_type: 'seller' | 'buyer' | 'both'
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
}