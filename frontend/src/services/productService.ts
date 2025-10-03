import axios from '../lib/axios'

export const productService = {
  async getMyProducts(): Promise<any[]> {
    const response = await axios.get('/products/user/my-products')
    return response.data
  },
}