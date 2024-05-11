<template>
  <v-footer 
    app
  >
    <div
      class="w-100"
    >
      <v-row 
        style="width: 800px"
        class="ma-auto"
      >
        <v-col
          lg="6"
        >
          <v-card
            class="rounded-lg h-100"
            variant="outlined"
            text="为什么SQL语句不能写1=1？"
            @click="userChat('为什么SQL语句不能写1=1？')"
          >
          </v-card>
        </v-col>
        <v-col
          lg="6"
        >
          <v-card
            class="rounded-lg"
            variant="outlined"
            text="如何利用现代CPU和GPU的高速ALU运算能力来优化矩阵-向量乘法和注意力计算？"
            @click="userChat('如何利用现代CPU和GPU的高速ALU运算能力来优化矩阵-向量乘法和注意力计算？')"
          >
          </v-card>
        </v-col>
        <v-col
          lg="6"
        >
          <v-card
            class="rounded-lg h-100"
            variant="outlined"
            text="JSP 中的域有哪些？它们的作用范围是怎样的？"
            @click="userChat('JSP 中的域有哪些？它们的作用范围是怎样的？')"
          >
          </v-card>
        </v-col>
        <v-col
          lg="6"
        >
          <v-card
            class="rounded-lg"
            variant="outlined"
            text="如何通过 Prompt Engineering 提高与大语言模型的对话效率？"
            @click="userChat('如何通过 Prompt Engineering 提高与大语言模型的对话效率？')"
          >
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-footer>
</template>

<script setup>
import { defineProps } from "vue"

defineProps({
  userChat: Function
})
  
</script>

<style scoped lang="sass">
  
</style>
