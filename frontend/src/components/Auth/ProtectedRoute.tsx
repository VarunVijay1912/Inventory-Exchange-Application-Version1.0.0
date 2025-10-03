import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'

interface ProtectedRouteProps {
  requireVerified?: boolean
}

export default function ProtectedRoute({ requireVerified = false }: ProtectedRouteProps) {
  const { isAuthenticated, user } = useAuthStore()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (requireVerified && !user?.is_verified) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          Account Verification Required
        </h1>
        <p className="text-gray-600 mb-8">
          Your account is pending verification. Please wait for admin approval.
        </p>
        <Navigate to="/dashboard" replace />
      </div>
    )
  }

  return <Outlet />
}