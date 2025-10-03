import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { MapPin, Eye, Calendar, Package, MessageSquare, Edit, Trash2 } from 'lucide-react'
import { productService } from '../../services/productService'
import { conversationService } from '../../services/conversationService'
import { Product } from '../../types'
import { useAuthStore } from '../../stores/authStore'
import LoadingSpinner from '../../components/Common/LoadingSpinner'
import toast from 'react-hot-toast'
import { format } from 'date-fns'

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { isAuthenticated, user } = useAuthStore()
  const [product, setProduct] = useState<Product | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [selectedImage, setSelectedImage] = useState(0)

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

  const handleContactSeller = async () => {
    if (!isAuthenticated) {
      toast.error('Please login to contact seller')
      navigate('/login')
      return
    }

    try {
      const conversation = await conversationService.createConversation(id!)
      navigate(`/messages/${conversation.id}`)
    } catch (error) {
      toast.error('Failed to start conversation')
    }
  }

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this product?')) return

    try {
      await productService.deleteProduct(id!)
      toast.success('Product deleted successfully')
      navigate('/my-products')
    } catch (error) {
      toast.error('Failed to delete product')
    }
  }

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-16">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!product) return null

  const isOwner = user?.id === product.seller_id
  const images = product.images.length > 0 ? product.images : [{ image_path: '/placeholder.png', is_primary: true }]

  return (
    <div className="bg-gray-50 min-h-screen py-8">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Images */}
          <div className="lg:col-span-2">
            <div className="card">
              <div className="aspect-[4/3] bg-gray-200 rounded-lg overflow-hidden mb-4">
                <img
                  src={images[selectedImage].image_path}
                  alt={product.title}
                  className="w-full h-full object-cover"
                />
              </div>

              {images.length > 1 && (
                <div className="grid grid-cols-6 gap-2">
                  {images.map((img, idx) => (
                    <button
                      key={idx}
                      onClick={() => setSelectedImage(idx)}
                      className={`aspect-square rounded-lg overflow-hidden border-2 ${
                        selectedImage === idx ? 'border-primary-600' : 'border-transparent'
                      }`}
                    >
                      <img src={img.image_path} alt="" className="w-full h-full object-cover" />
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Description */}
            <div className="card mt-6">
              <h2 className="text-xl font-semibold mb-4">Description</h2>
              <p className="text-gray-700 whitespace-pre-wrap">{product.description}</p>
            </div>

            {/* Specifications */}
            {product.specifications && Object.keys(product.specifications).length > 0 && (
              <div className="card mt-6">
                <h2 className="text-xl font-semibold mb-4">Specifications</h2>
                <dl className="grid grid-cols-2 gap-4">
                  {Object.entries(product.specifications).map(([key, value]) => (
                    <div key={key}>
                      <dt className="text-sm text-gray-600">{key}</dt>
                      <dd className="text-gray-900 font-medium">{value as string}</dd>
                    </div>
                  ))}
                </dl>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="card sticky top-20">
              <h1 className="text-2xl font-bold text-gray-900 mb-4">{product.title}</h1>

              {product.price ? (
                <div className="mb-4">
                  <p className="text-3xl font-bold text-gray-900">
                    ₹{product.price.toLocaleString()}
                  </p>
                  {product.price_negotiable && (
                    <span className="badge badge-warning">Negotiable</span>
                  )}
                </div>
              ) : (
                <p className="text-xl text-gray-600 mb-4">Contact for price</p>
              )}

              <div className="space-y-3 mb-6 text-sm">
                <div className="flex items-center text-gray-600">
                  <Package className="w-4 h-4 mr-2" />
                  <span>Condition: <strong className="text-gray-900">{product.condition}</strong></span>
                </div>
                <div className="flex items-center text-gray-600">
                  <Package className="w-4 h-4 mr-2" />
                  <span>Quantity: <strong className="text-gray-900">{product.quantity} {product.unit}</strong></span>
                </div>
                <div className="flex items-center text-gray-600">
                  <MapPin className="w-4 h-4 mr-2" />
                  <span>{product.location_city}, {product.location_state}</span>
                </div>
                <div className="flex items-center text-gray-600">
                  <Eye className="w-4 h-4 mr-2" />
                  <span>{product.views_count} views</span>
                </div>
                <div className="flex items-center text-gray-600">
                  <Calendar className="w-4 h-4 mr-2" />
                  <span>Listed {format(new Date(product.created_at), 'MMM dd, yyyy')}</span>
                </div>
              </div>

              {isOwner ? (
                <div className="space-y-2">
                  <button
                    onClick={() => navigate(`/products/${id}/edit`)}
                    className="btn-secondary w-full flex items-center justify-center space-x-2"
                  >
                    <Edit className="w-4 h-4" />
                    <span>Edit Product</span>
                  </button>
                  <button
                    onClick={handleDelete}
                    className="btn-danger w-full flex items-center justify-center space-x-2"
                  >
                    <Trash2 className="w-4 h-4" />
                    <span>Delete Product</span>
                  </button>
                </div>
              ) : (
                <button
                  onClick={handleContactSeller}
                  className="btn-primary w-full flex items-center justify-center space-x-2"
                >
                  <MessageSquare className="w-4 h-4" />
                  <span>Contact Seller</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}