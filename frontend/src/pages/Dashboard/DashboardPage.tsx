import { useAuthStore } from '../../stores/authStore'

export default function DashboardPage() {
  const { user } = useAuthStore()

  return (
    <div className="bg-gray-50 min-h-screen py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-bold mb-4">
          Welcome, {user?.company_name}!
        </h1>
        {!user?.is_verified && (
          <div className="bg-warning-50 border border-warning-200 rounded-lg p-4 mb-6">
            <p className="text-warning-800">
              Your account is pending verification.
            </p>
          </div>
        )}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Dashboard</h2>
          <p className="text-gray-600">Your dashboard content here...</p>
        </div>
      </div>
    </div>
  )
}