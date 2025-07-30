import { Bot } from 'lucide-react';

export function LoadingMessage() {
  return (
    <div className="flex gap-3 p-4 bg-gray-500 rounded-lg">
      <div className="flex-shrink-0">
        <Bot className="w-6 h-6 text-green-600" />
      </div>
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          </div>
          <span className="text-gray-500 text-sm">Thinking...</span>
        </div>
      </div>
    </div>
  );
}