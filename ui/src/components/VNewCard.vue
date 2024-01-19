<!-- 这是前端页面展示的新闻文章模版 -->
<template>
    <el-card shadow="hover">
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
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Avatar, Clock, Document } from '@element-plus/icons-vue'
const props = defineProps(['data'])
const data = ref(props.data)

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
</style>