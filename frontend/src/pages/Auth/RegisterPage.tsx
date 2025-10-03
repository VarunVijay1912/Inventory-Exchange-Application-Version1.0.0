import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import toast from 'react-hot-toast'
import { UserPlus } from 'lucide-react'
import { authService } from '../../services/authService'
import LoadingSpinner from '../../components/Common/LoadingSpinner'

const registerSchema = z.object({
  email: z.string().email('Invalid email address'),
  phone: z.string().regex(/^(\+91|91)?[6-9]\d{9}$/, 'Invalid Indian phone number'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  company_name: z.string().min(2, 'Company name is required'),
  contact_person: z.string().min(2, 'Contact person name is required'),
  gst_number: z.string().regex(/^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/, 'Invalid GST number'),
  city: z.string().optional(),
  state: z.string().optional(),
  pincode: z.string().regex(/^\d{6}$/, 'Invalid PIN code').optional(),
  user_type: z.enum(['seller', 'buyer', 'both']),
})

type RegisterFormData = z.infer<typeof registerSchema>

export default function RegisterPage() {
  const navigate = useNavigate()
  const [isLoading, setIsLoading] = useState(false)

  const { register, handleSubmit, formState: { errors } } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      user_type: 'both',
    },
  })

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true)
    try {
      await authService.register(data)
      toast.success('Registration successful! Please login.')
      navigate('/login')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Registration failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <UserPlus className="mx-auto h-12 w-12 text-primary-600" />
          <h2 className="mt-6 text-3xl font-bold text-gray-900">Create your account</h2>
          <p className="mt-2 text-sm text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="text-primary-600 hover:text-primary-700 font-medium">
              Sign in
            </Link>
          </p>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Account Information */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Account Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email Address *
                  </label>
                  <input
                    {...register('email')}
                    type="email"
                    className={`input ${errors.email ? 'input-error' : ''}`}
                    placeholder="your@email.com"
                  />
                  {errors.email && (
                    <p className="mt-1 text-sm text-error-500">{errors.email.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Phone Number *
                  </label>
                  <input
                    {...register('phone')}
                    type="tel"
                    className={`input ${errors.phone ? 'input-error' : ''}`}
                    placeholder="+91 9876543210"
                  />
                  {errors.phone && (
                    <p className="mt-1 text-sm text-error-500">{errors.phone.message}</p>
                  )}
                </div>

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Password *
                  </label>
                  <input
                    {...register('password')}
                    type="password"
                    className={`input ${errors.password ? 'input-error' : ''}`}
                    placeholder="Minimum 8 characters"
                  />
                  {errors.password && (
                    <p className="mt-1 text-sm text-error-500">{errors.password.message}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Company Details */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Company Details</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Company Name *
                  </label>
                  <input
                    {...register('company_name')}
                    className={`input ${errors.company_name ? 'input-error' : ''}`}
                    placeholder="Your Company Pvt Ltd"
                  />
                  {errors.company_name && (
                    <p className="mt-1 text-sm text-error-500">{errors.company_name.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Contact Person *
                  </label>
                  <input
                    {...register('contact_person')}
                    className={`input ${errors.contact_person ? 'input-error' : ''}`}
                    placeholder="John Doe"
                  />
                  {errors.contact_person && (
                    <p className="mt-1 text-sm text-error-500">{errors.contact_person.message}</p>
                  )}
                </div>

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    GST Number *
                  </label>
                  <input
                    {...register('gst_number')}
                    className={`input ${errors.gst_number ? 'input-error' : ''}`}
                    placeholder="27AAAAA0000A1Z5"
                  />
                  {errors.gst_number && (
                    <p className="mt-1 text-sm text-error-500">{errors.gst_number.message}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Location */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Location</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
                  <input {...register('city')} className="input" placeholder="Mumbai" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
                  <input {...register('state')} className="input" placeholder="Maharashtra" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">PIN Code</label>
                  <input
                    {...register('pincode')}
                    className={`input ${errors.pincode ? 'input-error' : ''}`}
                    placeholder="400001"
                  />
                  {errors.pincode && (
                    <p className="mt-1 text-sm text-error-500">{errors.pincode.message}</p>
                  )}
                </div>
              </div>
            </div>

            {/* User Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                I am a *
              </label>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input {...register('user_type')} type="radio" value="seller" className="mr-2" />
                  <span>Seller - I want to list products</span>
                </label>
                <label className="flex items-center">
                  <input {...register('user_type')} type="radio" value="buyer" className="mr-2" />
                  <span>Buyer - I want to purchase products</span>
                </label>
                <label className="flex items-center">
                  <input {...register('user_type')} type="radio" value="both" className="mr-2" />
                  <span>Both - I want to buy and sell</span>
                </label>
              </div>
            </div>

            <div className="pt-4">
              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary w-full flex items-center justify-center space-x-2"
              >
                {isLoading ? <LoadingSpinner size="sm" /> : <span>Create Account</span>}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}