import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },
    //本地运行配置，以及反向代理配置
    server: {
        // host: "localhost",
        host: "0.0.0.0",
        https: false,//是否启用 http 2
        cors: true,//为开发服务器配置 CORS , 默认启用并允许任何源
        // open: true,//服务启动时自动在浏览器中打开应用
        open: false,
        port: "5173",
        strictPort: false, //设为true时端口被占用则直接退出，不会尝试下一个可用端口
        force: true,//是否强制依赖预构建
        hmr: false,//禁用或配置 HMR 连接
        // 传递给 chockidar 的文件系统监视器选项
        watch: {
            ignored: ["!**/node_modules/your-package-name/**"]
        },
        // 反向代理配置
        proxy: {
            "/api": {
                // target: "http://localhost:14449",
                target: "http://0.0.0.0:14451",
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ""),
            },
        },
    },
    //打包配置
    build: {
        //浏览器兼容性  "esnext"|"modules"
        target: "modules",
        //指定输出路径
        outDir: "dist",
        //生成静态资源的存放路径
        assetsDir: "assets",
        //小于此阈值的导入或引用资源将内联为 base64 编码，以避免额外的 http 请求。设置为 0 可以完全禁用此项
        assetsInlineLimit: 4096,
        //启用/禁用 CSS 代码拆分
        cssCodeSplit: true,
        //构建后是否生成 source map 文件
        sourcemap: false,
        //自定义底层的 Rollup 打包配置
        rollupOptions: {},
    }
})
