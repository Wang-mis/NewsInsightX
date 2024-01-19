<!-- 这是前端页面展示的新闻文章模版 -->
<template>
    <el-card shadow="hover" @click="handleCardClick">
        <div style="border-bottom: 1px dashed #cccccc;">
            <el-icon class="new-item-icon"><Document /></el-icon>{{ data.title }}
        </div>

        <div class="new-item">
            <el-icon class="new-item-icon"><Avatar /></el-icon> {{ data.author }}
        </div>
        <div class="new-item" style="color: #aaaaaa">
            <el-icon class="new-item-icon"><Clock /></el-icon><span class="post-meta">{{ data.time }}</span>
        </div>
    </el-card>


    <el-dialog
        v-model="dialogVisible"
        :title="data.title"
        width="40%"
        class="custom-dialog"
        append-to-body
        @close="dialogVisible = false">

        <template #header>
            <div class="new-item" style="font-size: 20px; ">
                <el-icon class="new-item-icon"><Document /></el-icon>{{ data.title }}
            </div>
        </template>

        <div style="display: flex;">
            <div class="new-item" style="margin-right: 1rem;">
                <el-icon class="new-item-icon"><Avatar /></el-icon> {{ data.author }}
            </div>
            <div class="new-item" style="color: #aaaaaa">
                <el-icon class="new-item-icon"><Clock /></el-icon><span class="post-meta">{{ data.time }}</span>
            </div>
        </div>

        <div class="new-item" style="color: #67C23A">
            <el-icon class="new-item-icon"><Link /></el-icon>
                <el-link type="success" :href="data.url" target="_blank">{{ data.url }}</el-link>
        </div>

        <div style="margin-top: 1rem;">
            这是前端页面展示的新闻文章模版
            这是前端页面展示的新闻文章模版
            这是前端页面展示的新闻文章模版
            这是前端页面展示的新闻文章模版
            这是前端页面展示的新闻文章模版
        </div>

    </el-dialog>

</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Avatar, Clock, Document, Link } from '@element-plus/icons-vue'
const props = defineProps(['data'])
const data = ref(props.data)

const dialogVisible = ref(false)
const handleCardClick = () => {
    console.log('Card clicked!')
    // 在这里执行你想要的点击事件逻辑
    // 点击之后向后端要数据展示

    dialogVisible.value = true
}
</script>

<style lang="scss" scoped>

.new-item-icon {
    margin-right: 0.2rem;
}
.new-item {
    display: flex;
    align-items: center;
}
.post-meta {
    font-size: 14px;
    display: inline-block;
    line-height: 20px;
}
.dialog-footer {
    display: flex;
    justify-content: flex-end;
}
</style>

<style>
/* 注意使用了全局样式 */
.custom-dialog {
    .el-dialog__body {
        padding-top: 0px;
    }
}
</style>