import { Configuration } from "../global";
import { FilterMessages } from '../Utilities'




export interface ApiResponse { 
  data: string[];
  message?: string;
 }

export async function GetModels(): Promise<ApiResponse> {
    try {
      const response = await fetch(`${Configuration.API_BASE_URL}/models/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });

      const data = await response.json();

      if (data.data.reply === "success") {
        const models = data.data.models;
        return { data: models } as ApiResponse;
      }

      return  { message: data.data.reply, data: [] } as ApiResponse;
    } 
    catch (error) {
      console.log(error);
      return { message: "error", data: [] } as ApiResponse; 
    };
  }

export interface Message {
    role: string;
    content: string;
}

export interface ModelReply {
    messages: Message[];
    total_tokens: number;
    chat_id?: string;
    model: string;
    chat_description: string;
}

export async function GetReply(modelReply: ModelReply) {

    const requestContent: ModelReply = {
      messages: modelReply.messages.filter((message) => FilterMessages(message, "error")),
      total_tokens: modelReply.total_tokens,
      chat_id: modelReply.chat_id,
      model: modelReply.model,
      chat_description: modelReply.chat_description
    }
    try {
          const response = await fetch(`${Configuration.API_BASE_URL}/handle_conversation/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(requestContent)
        });

        const statusCode = response.status;

        if (statusCode === 200) {
            const data = await response.json();
            return data as ModelReply;
        }

        throw new Error(response.statusText);
    }
    catch (error) {
        const message: Message = { role:"error", content: "Error! Unable to connect to chatgpt server." };
        requestContent.messages.push(message)

        return requestContent;
      }
}

export async function GetConversation(chatId: number): Promise<ModelReply | undefined>  {

  try {
      const response = await fetch(`${Configuration.API_BASE_URL}/conversations/${chatId}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        },
      });

      if (response.status === 200) {
          const data = await response.json();
          return data as ModelReply;
      } else {
        console.log(response.status);
        return undefined;
      }
  }
  catch (error) {
      const message: Message = { role:"error", content: "Error! Unable to connect to chatgpt server." };
      const reply: ModelReply = { 
        messages: [message], 
        total_tokens: 0, 
        chat_id: String(chatId), 
        model: "" ,
        chat_description: "new chat"};

      return reply;
    }
}

export async function GetConversations() {

  try {
      const response = await fetch(`${Configuration.API_BASE_URL}/conversations/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        },
      });

      if (response.status === 200) {
          const data = await response.json();
          return data as ModelReply[];
      }

      return [];
      
  }
  catch (error) {
      console.log(error);
      return [];
    }
}

export async function CreateChat() {
  try {
      const response = await fetch(`${Configuration.API_BASE_URL}/new_chat/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
      });


      if (response.status === 200) {
        const data = await response.json();
        return data as ModelReply;
    }

    return { 
        messages: [{ "role": "error", "content": "Error! Unable to connect to chatgpt server." }], 
        total_tokens: 0  
    } as ModelReply;

  }
  catch (error) {
      return { 
          messages: [{ "role": "error", "content": "Error! Unable to connect to chatgpt server." }], 
          total_tokens: 0  
      } as ModelReply;
    }
}

export async function DeleteConversation(chat_id: string) {

  try {
      const response = await fetch(`${Configuration.API_BASE_URL}/conversations/${chat_id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json"
        },
      });
  }
  catch (error) {
    console.log("DeleteConversation Error:",error);
      return { } 
    }
}