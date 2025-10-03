import { Link } from 'react-router-dom'
import { Package } from 'lucide-react'

export default function HomePage() {
  return (
    <div>
      <section className="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">
            Manufacturing Marketplace
          </h1>
          <p className="text-xl mb-8">
            B2B marketplace for manufacturing surplus
          </p>
          <div className="flex gap-4 justify-center">
            <Link to="/register" className="btn bg-white text-primary-600 hover:bg-gray-100">
              Get Started
            </Link>
            <Link to="/browse" className="btn border-2 border-white text-white hover:bg-white hover:text-primary-600">
              Browse Products
            </Link>
          </div>
        </div>
      </section>

      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <Package className="w-16 h-16 text-primary-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Register & Verify</h3>
              <p className="text-gray-600">Create your account with GST verification</p>
            </div>
            <div>
              <Package className="w-16 h-16 text-primary-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">List or Browse</h3>
              <p className="text-gray-600">Post products or find inventory</p>
            </div>
            <div>
              <Package className="w-16 h-16 text-primary-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Connect & Trade</h3>
              <p className="text-gray-600">Negotiate and close deals</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}