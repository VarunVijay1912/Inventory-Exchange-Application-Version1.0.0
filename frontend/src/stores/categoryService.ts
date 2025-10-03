import axios from '../lib/axios'
import { Category, Material } from '../types'

export const categoryService = {
  async getCategories(): Promise<Category[]> {
    const response = await axios.get<Category[]>('/categories/')
    return response.data
  },

  async getMaterials(): Promise<Material[]> {
    const response = await axios.get<Material[]>('/categories/materials')
    return response.data
  },
}