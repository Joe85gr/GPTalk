import { GetModels, GetConversation, GetConversations, ModelReply, CreateChat, GetReply, DeleteConversation } from "./infrastructure/client";

export interface ChatHadlerParams {
    setStoredConversations: (modelReply: ModelReply[]) => void;
    setChatId: (chat_id: string) => void;
    setChatLog: (response: ModelReply) => void;
}

export class ChatHadler {
    setStoredConversations: (modelReply: ModelReply[]) => void;
    setChatId: (chat_id: string) => void;
    setChatLog: (response: ModelReply) => void;
   
    constructor(params: ChatHadlerParams) {
      this.setStoredConversations = params.setStoredConversations.bind(this);
      this.setChatId = params.setChatId.bind(this);
      this.setChatLog = params.setChatLog.bind(this);
    }
   
    async GetModels() {
        const models = await GetModels();
        return models;
    }

    async LoadChats() { 
      const storedConversations = await GetConversations();
      return storedConversations;
    }

    async LoadChat(chatId: string) {
      const response = await GetConversation(Number(chatId));
      
      if(response && response.chat_id){

        return response;
      }
    }

    async HandleChat(request: ModelReply) { 

      const data = await GetReply(request);
      return data;
   }

   async GetNewChat(){
    const response = await CreateChat();
    return response;
  }

  async GetChatLog(chatId: string) {
    const storedConversation = await GetConversation(Number(chatId));
    return storedConversation;

  }

  async DeleteChat(chatId: string) {
    const response = await DeleteConversation(chatId);
    return response;
  }
}

export const DefaultModeLReply: ModelReply = {
  messages: [],
  total_tokens: 0,
  chat_id: "",
  model: "",
  chat_description: ""
}