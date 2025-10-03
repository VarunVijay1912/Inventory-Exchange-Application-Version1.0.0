import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { MapPin, Eye, Calendar, Package, MessageSquare } from 'lucide-react'
import { productService } from '../../services/productService'
import { Product } from '../../types'
import { useAuthStore } from '../../stores/authStore'
import LoadingSpinner from '../../components/Common/LoadingSpinner'
import toast from 'react-hot-toast'

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { isAuthenticated } = useAuthStore()
  const [product, setProduct] = useState<Product | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (id) {
      loadProduct()
    }
  }, [id])

  const loadProduct = async () => {
    try {
      const data = await productService.getProduct(id!)
      setProduct(data)
    } catch (error) {
      toast.error('Failed to load product')
      navigate('/browse')
    } finally {
      setIsLoading(false)
    }
  }

  const handleContactSeller = () => {
    if (!isAuthenticated) {
      toast.error('Please login to contact seller')
      navigate('/login')
      return
    }
    toast.success('Contact seller feature coming soon!')
  }

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-16">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!product) return null

  return (
    <div className="bg-gray-50 min-h-screen py-8">
      <div className="container mx-auto px-4">
        <div className="card">
          <h1 className="text-3xl font-bold mb-4">{product.title}</h1>
          <p className="text-gray-700 mb-4">{product.description}</p>
          
          <div className="flex items-center space-x-4 mb-4">
            {product.price && (
              <p className="text-2xl font-bold">₹{product.price.toLocaleString()}</p>
            )}
            <span className="badge badge-info">{product.condition}</span>
          </div>

          <div className="space-y-2 text-sm text-gray-600 mb-6">
            <div className="flex items-center">
              <Package className="w-4 h-4 mr-2" />
              <span>Quantity: {product.quantity} {product.unit}</span>
            </div>
            <div className="flex items-center">
              <MapPin className="w-4 h-4 mr-2" />
              <span>{product.location_city}, {product.location_state}</span>
            </div>
            <div className="flex items-center">
              <Eye className="w-4 h-4 mr-2" />
              <span>{product.views_count} views</span>
            </div>
          </div>

          <button
            onClick={handleContactSeller}
            className="btn-primary flex items-center space-x-2"
          >
            <MessageSquare className="w-4 h-4" />
            <span>Contact Seller</span>
          </button>
        </div>
      </div>
    </div>
  )
}