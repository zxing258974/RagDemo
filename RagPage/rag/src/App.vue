<template>
  <v-app>
    <v-main 
      style="width: 800px;"
      class="ma-auto mt-5"
    >
      <v-alert
        v-for="m, index in messages"
        :key="index"
        density="compact"
        :icon="m.role === 'user' ? 'mdi-account' : 'mdi-robot-outline'"
        variant="text"
      >
        <v-md-preview :text="m.content"></v-md-preview>
        <v-skeleton-loader
          type="list-item-two-line"
          v-if="m.role === 'ai' && m.content === ''"
        >
        </v-skeleton-loader>
      </v-alert>
    </v-main>

    <AppFooter 
      :userChat="userChat"
    />
  </v-app>
</template>

<script setup>
import { fetchEventSource } from '@microsoft/fetch-event-source'
import { ref } from "vue"


const messages = ref([])

const userChat = (question) => {
  messages.value.push({
    "role": "user",
    "content": question
  })
  messages.value.push({
    "role": "ai",
    "content": ''
  })
  fetchEventSource(`/sse_stream/chat?question=${question}`,{
    method: 'GET',
    onmessage(ev) {
      try {
        const eventData = JSON.parse(ev.data)
        const subscript = messages.value.length - 1
        if (eventData.end) {
          messages.value[subscript].content = eventData.output
        } else {
          messages.value[subscript].content = messages.value[subscript].content + eventData.output
        }
      } catch (err) {
        console.log(ev)
      }

    },
    onclose() {
      // if the server closes the connection unexpectedly, retry:
      console.log("流式输出关闭")
    },
    onerror(err) {
      throw err;
    }
  })
}
</script>
