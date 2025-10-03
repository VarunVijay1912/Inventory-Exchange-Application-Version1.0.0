import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { productService } from '../../services/productService'
import LoadingSpinner from '../../components/Common/LoadingSpinner'

export default function CreateProductPage() {
  const navigate = useNavigate()
  const [isLoading, setIsLoading] = useState(false)
  const { register, handleSubmit, formState: { errors } } = useForm()

  const onSubmit = async (data: any) => {
    setIsLoading(true)
    try {
      await productService.createProduct(data)
      toast.success('Product created successfully!')
      navigate('/my-products')
    } catch (error) {
      toast.error('Failed to create product')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="bg-gray-50 min-h-screen py-8">
      <div className="container mx-auto px-4 max-w-2xl">
        <h1 className="text-3xl font-bold mb-6">Create Product</h1>
        
        <div className="card">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Product Title *
              </label>
              <input
                {...register('title', { required: true })}
                className="input"
                placeholder="Enter product title"
              />
              {errors.title && <p className="text-error-500 text-sm mt-1">Title is required</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description *
              </label>
              <textarea
                {...register('description', { required: true })}
                rows={4}
                className="input"
                placeholder="Describe your product"
              />
              {errors.description && <p className="text-error-500 text-sm mt-1">Description is required</p>}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Quantity *
                </label>
                <input
                  {...register('quantity', { required: true })}
                  type="number"
                  className="input"
                  placeholder="100"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Price
                </label>
                <input
                  {...register('price')}
                  type="number"
                  className="input"
                  placeholder="10000"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full"
            >
              {isLoading ? <LoadingSpinner size="sm" /> : 'Create Product'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}