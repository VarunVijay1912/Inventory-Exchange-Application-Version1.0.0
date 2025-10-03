import axios from '../lib/axios'
import { Product, ProductListItem } from '../types'

interface SearchParams {
  query?: string
  category_id?: string
  material_id?: string
  city?: string
  state?: string
  min_price?: number
  max_price?: number
  condition?: string
  sort_by?: string
  sort_order?: string
  skip?: number
  limit?: number
}

export const productService = {
  async searchProducts(params: SearchParams): Promise<ProductListItem[]> {
    const response = await axios.get<ProductListItem[]>('/products/', { params })
    return response.data
  },

  async getProduct(id: string): Promise<Product> {
    const response = await axios.get<Product>(`/products/${id}`)
    return response.data
  },

  async createProduct(data: any): Promise<Product> {
    const response = await axios.post<Product>('/products/', data)
    return response.data
  },

  async updateProduct(id: string, data: any): Promise<Product> {
    const response = await axios.put<Product>(`/products/${id}`, data)
    return response.data
  },

  async deleteProduct(id: string): Promise<void> {
    await axios.delete(`/products/${id}`)
  },

  async uploadImages(productId: string, files: File[], isPrimary: boolean = false): Promise<any> {
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))
    formData.append('is_primary', isPrimary.toString())

    const response = await axios.post(`/products/${productId}/images`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  async getMyProducts(): Promise<ProductListItem[]> {
    const response = await axios.get<ProductListItem[]>('/products/user/my-products')
    return response.data
  },
}