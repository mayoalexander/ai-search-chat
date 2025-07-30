import { ChatMessage as ChatMessageType } from '@/lib/types';
import { CheckCircle, XCircle, User, Bot } from 'lucide-react';

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  return (
    <div className={`flex gap-3 p-4 ${message.isUser ? 'bg-blue-800' : 'bg-gray-800'} rounded-lg`}>
      <div className="flex-shrink-0">
        {message.isUser ? (
          <User className="w-6 h-6 text-blue-600" />
        ) : (
          <Bot className="w-6 h-6 text-green-600" />
        )}
      </div>
      
      <div className="flex-1 space-y-2">
        <div className="prose prose-sm max-w-none">
          <div className="whitespace-pre-wrap">{message.content}</div>
        </div>
        
        {!message.isUser && message.cookwareValidated !== undefined && (
          <div className="flex items-center gap-2 text-sm">
            {message.cookwareValidated ? (
              <>
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span className="text-green-700">All required cookware available</span>
              </>
            ) : (
              <>
                <XCircle className="w-4 h-4 text-red-500" />
                <span className="text-red-700">Missing some required cookware</span>
              </>
            )}
          </div>
        )}
        
        {!message.isUser && message.queryType && (
          <div className="text-xs text-gray-500">
            Query type: {message.queryType}
          </div>
        )}
        
        <div className="text-xs text-gray-400">
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}