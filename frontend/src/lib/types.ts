export interface ChatMessage {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  queryType?: 'cooking' | 'non_cooking';
  cookwareValidated?: boolean;
  reasoningChain?: string[];
}

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  response: string;
  query_type?: 'cooking' | 'non_cooking';
  reasoning_chain?: string[];
  cookware_validated?: boolean;
}