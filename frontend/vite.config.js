import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
      imports: ['vue', 'vue-router', 'pinia']
    }),
    Components({
      resolvers: [ElementPlusResolver()]
    })
  ],
  // 禁用缓存，解决 WSL 与 Windows 文件系统时间戳同步问题
  cacheDir: false,
  server: {
    port: 3000,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      }
    },
    // 使用轮询代替 fsnotify，解决 WSL 文件监听问题
    watch: {
      usePolling: true,
      interval: 1000
    }
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})
