import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Plus, Package } from 'lucide-react'
import { productService } from '../../services/productService'
import { ProductListItem } from '../../types'
import ProductCard from '../../components/Product/ProductCard'
import LoadingSpinner from '../../components/Common/LoadingSpinner'
import EmptyState from '../../components/Common/EmptyState'

export default function MyProductsPage() {
  const [products, setProducts] = useState<ProductListItem[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadProducts()
  }, [])

  const loadProducts = async () => {
    try {
      const data = await productService.getMyProducts()
      setProducts(data)
    } catch (error) {
      console.error('Failed to load products', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="bg-gray-50 min-h-screen py-8">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">My Products</h1>
          <Link to="/products/create" className="btn-primary flex items-center space-x-2">
            <Plus className="w-4 h-4" />
            <span>Add Product</span>
          </Link>
        </div>

        {isLoading ? (
          <div className="py-16">
            <LoadingSpinner size="lg" />
          </div>
        ) : products.length === 0 ? (
          <EmptyState
            icon={Package}
            title="No products yet"
            description="Start by creating your first product listing"
            action={{
              label: 'Create Product',
              onClick: () => window.location.href = '/products/create'
            }}
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}