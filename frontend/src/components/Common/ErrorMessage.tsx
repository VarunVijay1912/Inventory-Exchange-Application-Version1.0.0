import { AlertCircle } from 'lucide-react'

interface ErrorMessageProps {
  message: string
}

export default function ErrorMessage({ message }: ErrorMessageProps) {
  return (
    <div className="bg-error-50 border border-error-200 rounded-lg p-4 flex items-start space-x-3">
      <AlertCircle className="w-5 h-5 text-error-500 flex-shrink-0 mt-0.5" />
      <p className="text-sm text-error-700">{message}</p>
    </div>
  )
}
