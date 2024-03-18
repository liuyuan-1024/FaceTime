import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    base: './',
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src')
        }
    },
    server: {
        // 解决跨域问题
        proxy: {
            // 代理Java后端
            '/api': {
                target: 'http://localhost:8080', // 代理的地址(实际请求地址)
                changeOrigin: true, // 允许跨域
                secure: false, // 如果是不是https接口，可以不配置这个参数
                ws: true, //代理 web socked
                rewrite: (path) => path.replace(/^\/api/, '')
            }
        }
    }
})
