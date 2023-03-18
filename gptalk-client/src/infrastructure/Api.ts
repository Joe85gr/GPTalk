import { Configuration } from "../global";

export async function LoadModels() {
    try {
      const response = await fetch(`${Configuration.API_BASE_URL}/models/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });

      const data = await response.json()
      const m = data.models
        .filter((model: string) => { return model.includes("gpt")})
        .map((model: string) => { return{ label: model, value: model } })
      console.log("models loaded");

      return m;
    } 
    catch (error) {
      console.log(error);
      return [];
    }
  }

export interface Message {
    role: string;
    content: string;
}

export interface ModelReply {
    messages: Message[];
    total_tokens: string;
}

export async function GetReply(messages: Message[], model: string) {
    try {
        const requestContent = { "messages": messages, "model": model };
  
        const response = await fetch(`${Configuration.API_BASE_URL}/messages/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(requestContent)
        });
  
        const data = await response.json() as ModelReply;

        return data;
    }
    catch (error) {
        return { 
            messages: [...messages, { "role": "error", "content": "Error! Unable to connect to chatgpt server." }], 
            total_tokens: ""  
        } as ModelReply;
      }
}