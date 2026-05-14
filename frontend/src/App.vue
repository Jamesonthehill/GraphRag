<template>
  <div class="page">
    <div class="chat-card">
      <header class="chat-header">
        <h1>GraphRAG Chatbot</h1>
        <p>Ask questions based on your Neo4j graph.</p>
      </header>

      <main class="messages">
        <div
            v-for="(message, index) in messages"
            :key="index"
            :class="['message', message.role]"
        >
          <div class="bubble">
            {{ message.content }}
          </div>
        </div>

        <div v-if="loading" class="message assistant">
          <div class="bubble">Thinking...</div>
        </div>
      </main>

      <form class="input-area" @submit.prevent="sendMessage">
        <input
            v-model="input"
            type="text"
            placeholder="Ask something like: What does GraphRAG use?"
        />
        <button type="submit" :disabled="loading || !input.trim()">
          Send
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

type Message = {
  role: "user" | "assistant";
  content: string;
};

const input = ref("");
const loading = ref(false);

const messages = ref<Message[]>([
  {
    role: "assistant",
    content: "Hi, I’m your GraphRAG chatbot. Ask me something about your graph.",
  },
]);

async function sendMessage() {
  const question = input.value.trim();

  if (!question) return;

  messages.value.push({
    role: "user",
    content: question,
  });

  input.value = "";
  loading.value = true;

  try {
    const res = await fetch("http://127.0.0.1:8000/api/graphrag/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    if (!res.ok) {
      throw new Error(`API error: ${res.status}`);
    }

    const data = await res.json();

    messages.value.push({
      role: "assistant",
      content: data.answer ?? "No answer returned.",
    });
  } catch (error) {
    messages.value.push({
      role: "assistant",
      content: "Sorry, I could not connect to the GraphRAG backend.",
    });

    console.error(error);
  } finally {
    loading.value = false;
  }
}
</script>