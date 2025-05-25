import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true, // 监听所有地址，包括局域网和公网地址
    port: 5173, // 默认端口
  }
})
