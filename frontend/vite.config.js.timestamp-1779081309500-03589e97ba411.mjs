// vite.config.js
import { defineConfig } from "file:///mnt/c/Users/rs8568/Desktop/Project/project-quote-system/frontend/node_modules/.pnpm/vite@5.4.21_sass@1.99.0/node_modules/vite/dist/node/index.js";
import vue from "file:///mnt/c/Users/rs8568/Desktop/Project/project-quote-system/frontend/node_modules/.pnpm/@vitejs+plugin-vue@5.2.4_vite@5.4.21_sass@1.99.0__vue@3.5.34/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import AutoImport from "file:///mnt/c/Users/rs8568/Desktop/Project/project-quote-system/frontend/node_modules/.pnpm/unplugin-auto-import@0.17.5_@vueuse+core@14.3.0_vue@3.5.34__rollup@4.60.3/node_modules/unplugin-auto-import/dist/vite.js";
import Components from "file:///mnt/c/Users/rs8568/Desktop/Project/project-quote-system/frontend/node_modules/.pnpm/unplugin-vue-components@0.26.0_@babel+parser@7.29.3_rollup@4.60.3_vue@3.5.34/node_modules/unplugin-vue-components/dist/vite.js";
import { ElementPlusResolver } from "file:///mnt/c/Users/rs8568/Desktop/Project/project-quote-system/frontend/node_modules/.pnpm/unplugin-vue-components@0.26.0_@babel+parser@7.29.3_rollup@4.60.3_vue@3.5.34/node_modules/unplugin-vue-components/dist/resolvers.js";
var vite_config_default = defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
      imports: ["vue", "vue-router", "pinia"]
    }),
    Components({
      resolvers: [ElementPlusResolver()]
    })
  ],
  // 禁用缓存，解决 WSL 与 Windows 文件系统时间戳同步问题
  cacheDir: false,
  server: {
    port: 3e3,
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true
      }
    },
    // 使用轮询代替 fsnotify，解决 WSL 文件监听问题
    watch: {
      usePolling: true,
      interval: 1e3
    }
  },
  resolve: {
    alias: {
      "@": "/src"
    }
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvbW50L2MvVXNlcnMvcnM4NTY4L0Rlc2t0b3AvUHJvamVjdC9wcm9qZWN0LXF1b3RlLXN5c3RlbS9mcm9udGVuZFwiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9maWxlbmFtZSA9IFwiL21udC9jL1VzZXJzL3JzODU2OC9EZXNrdG9wL1Byb2plY3QvcHJvamVjdC1xdW90ZS1zeXN0ZW0vZnJvbnRlbmQvdml0ZS5jb25maWcuanNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfaW1wb3J0X21ldGFfdXJsID0gXCJmaWxlOi8vL21udC9jL1VzZXJzL3JzODU2OC9EZXNrdG9wL1Byb2plY3QvcHJvamVjdC1xdW90ZS1zeXN0ZW0vZnJvbnRlbmQvdml0ZS5jb25maWcuanNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tICd2aXRlJ1xuaW1wb3J0IHZ1ZSBmcm9tICdAdml0ZWpzL3BsdWdpbi12dWUnXG5pbXBvcnQgQXV0b0ltcG9ydCBmcm9tICd1bnBsdWdpbi1hdXRvLWltcG9ydC92aXRlJ1xuaW1wb3J0IENvbXBvbmVudHMgZnJvbSAndW5wbHVnaW4tdnVlLWNvbXBvbmVudHMvdml0ZSdcbmltcG9ydCB7IEVsZW1lbnRQbHVzUmVzb2x2ZXIgfSBmcm9tICd1bnBsdWdpbi12dWUtY29tcG9uZW50cy9yZXNvbHZlcnMnXG5cbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyh7XG4gIHBsdWdpbnM6IFtcbiAgICB2dWUoKSxcbiAgICBBdXRvSW1wb3J0KHtcbiAgICAgIHJlc29sdmVyczogW0VsZW1lbnRQbHVzUmVzb2x2ZXIoKV0sXG4gICAgICBpbXBvcnRzOiBbJ3Z1ZScsICd2dWUtcm91dGVyJywgJ3BpbmlhJ11cbiAgICB9KSxcbiAgICBDb21wb25lbnRzKHtcbiAgICAgIHJlc29sdmVyczogW0VsZW1lbnRQbHVzUmVzb2x2ZXIoKV1cbiAgICB9KVxuICBdLFxuICAvLyBcdTc5ODFcdTc1MjhcdTdGMTNcdTVCNThcdUZGMENcdTg5RTNcdTUxQjMgV1NMIFx1NEUwRSBXaW5kb3dzIFx1NjU4N1x1NEVGNlx1N0NGQlx1N0VERlx1NjVGNlx1OTVGNFx1NjIzM1x1NTQwQ1x1NkI2NVx1OTVFRVx1OTg5OFxuICBjYWNoZURpcjogZmFsc2UsXG4gIHNlcnZlcjoge1xuICAgIHBvcnQ6IDMwMDAsXG4gICAgcHJveHk6IHtcbiAgICAgICcvYXBpJzoge1xuICAgICAgICB0YXJnZXQ6ICdodHRwOi8vbG9jYWxob3N0OjUwMDAnLFxuICAgICAgICBjaGFuZ2VPcmlnaW46IHRydWVcbiAgICAgIH1cbiAgICB9LFxuICAgIC8vIFx1NEY3Rlx1NzUyOFx1OEY2RVx1OEJFMlx1NEVFM1x1NjZGRiBmc25vdGlmeVx1RkYwQ1x1ODlFM1x1NTFCMyBXU0wgXHU2NTg3XHU0RUY2XHU3NkQxXHU1NDJDXHU5NUVFXHU5ODk4XG4gICAgd2F0Y2g6IHtcbiAgICAgIHVzZVBvbGxpbmc6IHRydWUsXG4gICAgICBpbnRlcnZhbDogMTAwMFxuICAgIH1cbiAgfSxcbiAgcmVzb2x2ZToge1xuICAgIGFsaWFzOiB7XG4gICAgICAnQCc6ICcvc3JjJ1xuICAgIH1cbiAgfVxufSlcbiJdLAogICJtYXBwaW5ncyI6ICI7QUFBcVgsU0FBUyxvQkFBb0I7QUFDbFosT0FBTyxTQUFTO0FBQ2hCLE9BQU8sZ0JBQWdCO0FBQ3ZCLE9BQU8sZ0JBQWdCO0FBQ3ZCLFNBQVMsMkJBQTJCO0FBRXBDLElBQU8sc0JBQVEsYUFBYTtBQUFBLEVBQzFCLFNBQVM7QUFBQSxJQUNQLElBQUk7QUFBQSxJQUNKLFdBQVc7QUFBQSxNQUNULFdBQVcsQ0FBQyxvQkFBb0IsQ0FBQztBQUFBLE1BQ2pDLFNBQVMsQ0FBQyxPQUFPLGNBQWMsT0FBTztBQUFBLElBQ3hDLENBQUM7QUFBQSxJQUNELFdBQVc7QUFBQSxNQUNULFdBQVcsQ0FBQyxvQkFBb0IsQ0FBQztBQUFBLElBQ25DLENBQUM7QUFBQSxFQUNIO0FBQUE7QUFBQSxFQUVBLFVBQVU7QUFBQSxFQUNWLFFBQVE7QUFBQSxJQUNOLE1BQU07QUFBQSxJQUNOLE9BQU87QUFBQSxNQUNMLFFBQVE7QUFBQSxRQUNOLFFBQVE7QUFBQSxRQUNSLGNBQWM7QUFBQSxNQUNoQjtBQUFBLElBQ0Y7QUFBQTtBQUFBLElBRUEsT0FBTztBQUFBLE1BQ0wsWUFBWTtBQUFBLE1BQ1osVUFBVTtBQUFBLElBQ1o7QUFBQSxFQUNGO0FBQUEsRUFDQSxTQUFTO0FBQUEsSUFDUCxPQUFPO0FBQUEsTUFDTCxLQUFLO0FBQUEsSUFDUDtBQUFBLEVBQ0Y7QUFDRixDQUFDOyIsCiAgIm5hbWVzIjogW10KfQo=
