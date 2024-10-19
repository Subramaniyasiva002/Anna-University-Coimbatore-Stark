<template>
  <div class="chatbot-container">
    <div class="chatbox">
      <div class="messages" ref="messagesContainer">
        <div v-for="(message, index) in chatHistory" :key="index" 
             :class="['message', message.role.toLowerCase()]">
          <strong>{{ message.role }}:</strong> {{ message.text }}
        </div>
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </div>
      <div class="input-area">
        <input 
          v-model="userMessage" 
          @keyup.enter="sendMessage" 
          placeholder="Ask about stock market trends..." 
          :disabled="loading"
        />
        <button 
          @click="sendMessage" 
          :disabled="loading || !userMessage.trim()"
        >
          {{ loading ? 'Sending...' : 'Send' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Chatbot',
  data() {
    return {
      userMessage: '',
      chatHistory: [],
      error: null,
      loading: false
    }
  },
  methods: {
    async sendMessage() {
      if (!this.userMessage.trim() || this.loading) return;

      this.error = null;
      this.loading = true;
      
      // Store the message
      const message = this.userMessage.trim();
      this.chatHistory.push({ role: 'You', text: message });
      this.userMessage = ''; // Clear input immediately

      try {
        console.log('Sending request to chatbot...');
        const response = await fetch('http://localhost:5000/chatbot', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message })
        });

        console.log('Response status:', response.status);
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => null);
          throw new Error(errorData?.error || `Server error: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
          throw new Error(data.error);
        }

        this.chatHistory.push({ 
          role: 'Bot', 
          text: data.response || 'Sorry, I received an empty response.'
        });

      } catch (error) {
        console.error('Chat error:', error);
        this.error = error.message;
        this.chatHistory.push({ 
          role: 'System', 
          text: 'Sorry, I encountered an error. Please try again.' 
        });
      } finally {
        this.loading = false;
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    scrollToBottom() {
      if (this.$refs.messagesContainer) {
        this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
      }
    }
  }
}
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 350px;
  background-color: #ffffff;
  border: 1px solid #e1e1e1;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.chatbox {
  display: flex;
  flex-direction: column;
  height: 400px;
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.message {
  padding: 8px 12px;
  border-radius: 8px;
  max-width: 85%;
  word-wrap: break-word;
}

.message.you {
  align-self: flex-end;
  background-color: #007bff;
  color: white;
}

.message.bot {
  align-self: flex-start;
  background-color: #f1f1f1;
  color: #333;
}

.message.system {
  align-self: center;
  background-color: #fff3cd;
  color: #856404;
  font-style: italic;
}

.error-message {
  padding: 8px 12px;
  background-color: #fff3cd;
  color: #856404;
  border-radius: 8px;
  margin: 8px 0;
  text-align: center;
}

.input-area {
  display: flex;
  padding: 15px;
  gap: 8px;
  border-top: 1px solid #e1e1e1;
}

.input-area input {
  flex-grow: 1;
  padding: 8px 12px;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  outline: none;
  font-size: 14px;
}

.input-area input:focus {
  border-color: #007bff;
}

.input-area button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.input-area button:hover:not(:disabled) {
  background-color: #0056b3;
}

.input-area button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>