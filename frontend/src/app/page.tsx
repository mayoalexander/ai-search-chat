'use client';

import { useState, useRef, useEffect } from 'react';
import { ChatMessage } from '@/components/ChatMessage';
import { ChatInput } from '@/components/ChatInput';
import { LoadingMessage } from '@/components/LoadingMessage';
import { sendChatMessage } from '@/lib/api';
import { ChatMessage as ChatMessageType } from '@/lib/types';
import { ChefHat } from 'lucide-react';

export default function Home() {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Add welcome message on first load
  useEffect(() => {
    const welcomeMessage: ChatMessageType = {
      id: 'welcome',
      content: `Hello! I'm your AI Recipe Assistant. I can help you with:

🍳 Recipe suggestions and cooking instructions
🔍 Finding recipes based on your ingredients
🍴 Checking if you have the right cookware for recipes

I have access to these cookware items:
• Spatula • Frying Pan • Little Pot • Stovetop
• Whisk • Knife • Ladle • Spoon

What would you like to cook today?`,
      isUser: false,
      timestamp: new Date(),
      queryType: 'cooking'
    };
    setMessages([welcomeMessage]);
  }, []);

  const handleSendMessage = async (messageContent: string) => {
    // Add user message
    const userMessage: ChatMessageType = {
      id: Date.now().toString(),
      content: messageContent,
      isUser: true,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendChatMessage(messageContent);
      
      // Add assistant response
      const assistantMessage: ChatMessageType = {
        id: (Date.now() + 1).toString(),
        content: response.response,
        isUser: false,
        timestamp: new Date(),
        queryType: response.query_type,
        cookwareValidated: response.cookware_validated,
        reasoningChain: response.reasoning_chain
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);
      
      const errorMessage: ChatMessageType = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error while processing your request. Please try again.',
        isUser: false,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto">
      {/* Header */}
      <header className="flex items-center gap-3 p-4 border-b bg-white">
        <ChefHat className="w-8 h-8 text-orange-600" />
        <div>
          <h1 className="text-xl font-bold text-gray-900">AI Recipe Assistant</h1>
          <p className="text-sm text-gray-600">Your cooking companion with cookware validation</p>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        {isLoading && <LoadingMessage />}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  );
}
