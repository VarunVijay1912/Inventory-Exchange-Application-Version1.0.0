import { Link, useNavigate } from 'react-router-dom'
import { Search, User, MessageSquare, Menu, LogOut, Package } from 'lucide-react'
import { useAuthStore } from '../../stores/authStore'
import { useState } from 'react'

export default function Header() {
  const { isAuthenticated, user, logout } = useAuthStore()
  const navigate = useNavigate()
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [showMobileMenu, setShowMobileMenu] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <Package className="w-8 h-8 text-primary-600" />
            <span className="text-xl font-bold text-gray-900">
              Manufacturing Marketplace
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link to="/browse" className="text-gray-600 hover:text-primary-600 transition">
              Browse Products
            </Link>
            
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="text-gray-600 hover:text-primary-600 transition">
                  Dashboard
                </Link>
                <Link to="/my-products" className="text-gray-600 hover:text-primary-600 transition">
                  My Products
                </Link>
                <Link to="/messages" className="text-gray-600 hover:text-primary-600 transition relative">
                  <MessageSquare className="w-5 h-5" />
                </Link>
                
                {/* User Menu */}
                <div className="relative">
                  <button
                    onClick={() => setShowUserMenu(!showUserMenu)}
                    className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition"
                  >
                    <User className="w-5 h-5" />
                    <span className="text-sm">{user?.company_name}</span>
                  </button>

                  {showUserMenu && (
                    <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2">
                      <Link
                        to="/profile"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        onClick={() => setShowUserMenu(false)}
                      >
                        Profile
                      </Link>
                      <Link
                        to="/settings"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        onClick={() => setShowUserMenu(false)}
                      >
                        Settings
                      </Link>
                      {user?.is_verified && (
                        <Link
                          to="/admin"
                          className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                          onClick={() => setShowUserMenu(false)}
                        >
                          Admin Panel
                        </Link>
                      )}
                      <hr className="my-2" />
                      <button
                        onClick={handleLogout}
                        className="w-full text-left px-4 py-2 text-sm text-error-600 hover:bg-gray-100 flex items-center space-x-2"
                      >
                        <LogOut className="w-4 h-4" />
                        <span>Logout</span>
                      </button>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-600 hover:text-primary-600 transition">
                  Login
                </Link>
                <Link to="/register" className="btn-primary">
                  Register
                </Link>
              </>
            )}
          </nav>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setShowMobileMenu(!showMobileMenu)}
            className="md:hidden text-gray-600"
          >
            <Menu className="w-6 h-6" />
          </button>
        </div>

        {/* Mobile Menu */}
        {showMobileMenu && (
          <div className="md:hidden py-4 border-t border-gray-200">
            <nav className="flex flex-col space-y-4">
              <Link to="/browse" className="text-gray-600">Browse Products</Link>
              {isAuthenticated ? (
                <>
                  <Link to="/dashboard" className="text-gray-600">Dashboard</Link>
                  <Link to="/my-products" className="text-gray-600">My Products</Link>
                  <Link to="/messages" className="text-gray-600">Messages</Link>
                  <Link to="/profile" className="text-gray-600">Profile</Link>
                  <button onClick={handleLogout} className="text-error-600 text-left">
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="text-gray-600">Login</Link>
                  <Link to="/register" className="btn-primary">Register</Link>
                </>
              )}
            </nav>
          </div>
        )}
      </div>
    </header>
  )
}
