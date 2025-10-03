import { Link } from 'react-router-dom'
import { MapPin, Eye } from 'lucide-react'
import { ProductListItem } from '../../types'
import { formatDistanceToNow } from 'date-fns'

interface ProductCardProps {
  product: ProductListItem
}

export default function ProductCard({ product }: ProductCardProps) {
  const imageUrl = product.primary_image || '/placeholder-product.png'

  return (
    <Link to={`/products/${product.id}`} className="card hover:shadow-lg transition group">
      <div className="aspect-[4/3] bg-gray-200 rounded-lg overflow-hidden mb-4">
        <img
          src={imageUrl}
          alt={product.title}
          className="w-full h-full object-cover group-hover:scale-105 transition"
        />
      </div>

      <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-primary-600">
        {product.title}
      </h3>

      <div className="flex items-center justify-between mb-2">
        {product.price ? (
          <div>
            <p className="text-2xl font-bold text-gray-900">₹{product.price.toLocaleString()}</p>
            {product.price_negotiable && (
              <span className="badge badge-warning text-xs">Negotiable</span>
            )}
          </div>
        ) : (
          <p className="text-gray-600">Contact for price</p>
        )}
      </div>

      <div className="flex items-center text-sm text-gray-600 mb-2">
        <MapPin className="w-4 h-4 mr-1" />
        <span>{product.location_city}, {product.location_state}</span>
      </div>

      <div className="flex items-center justify-between text-xs text-gray-500 pt-2 border-t">
        <span className="flex items-center">
          <Eye className="w-3 h-3 mr-1" />
          {product.views_count} views
        </span>
        <span>{formatDistanceToNow(new Date(product.created_at), { addSuffix: true })}</span>
      </div>
    </Link>
  )
}